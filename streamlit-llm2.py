import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

# Database Connection


def connect_to_db():
    try:
        conn = psycopg2.connect(host="localhost", 
                                database="streamlit-test",
                                user="postgres",
                                password="p@ssw0rd",)

        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Query Function


def run_query(conn, query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

# Visualization Functions


def plot_books_per_author(conn):
    query = """
    SELECT Person.name, COUNT(Book.Book_id) AS book_count
    FROM Author
    JOIN Person ON Author.Person_id = Person.Person_id
    JOIN Book ON Author.Author_id = Book.Author_id
    GROUP BY Person.name
    """
    df = run_query(conn, query)
    if df is not None and not df.empty:
        fig, ax = plt.subplots()
        sns.barplot(x='name', y='book_count', data=df, ax=ax)
        ax.set_title('Number of Books per Author')
        ax.set_xlabel('Author Name')
        ax.set_ylabel('Number of Books')
        plt.xticks(rotation=90)
        st.pyplot(fig)


def plot_average_price_by_genre(conn):
    query = """
    SELECT genre, AVG(price) AS avg_price
    FROM Book
    GROUP BY genre
    """
    df = run_query(conn, query)
    if df is not None and not df.empty:
        fig, ax = plt.subplots()
        sns.barplot(x='genre', y='avg_price', data=df, ax=ax)
        ax.set_title('Average Book Price by Genre')
        ax.set_xlabel('Genre')
        ax.set_ylabel('Average Price')
        plt.xticks(rotation=90)
        st.pyplot(fig)


def plot_orders_per_customer(conn):
    query = """
    SELECT Person.name, COUNT(Orders.Orders_id) AS order_count
    FROM Customer
    JOIN Person ON Customer.Person_id = Person.Person_id
    JOIN Orders ON Customer.Customer_id = Orders.Customer_id
    GROUP BY Person.name
    """
    df = run_query(conn, query)
    if df is not None and not df.empty:
        fig, ax = plt.subplots()
        sns.barplot(x='name', y='order_count', data=df, ax=ax)
        ax.set_title('Number of Orders per Customer')
        ax.set_xlabel('Customer Name')
        ax.set_ylabel('Number of Orders')
        plt.xticks(rotation=90)
        st.pyplot(fig)

def plot_sales_over_time(conn):
    query = """
    SELECT DATE(orders.date) AS order_date, SUM(orderdetails.quantity) AS books_sold
    FROM orders
    JOIN orderdetails ON orders.orders_id = orderdetails.orders_id
    GROUP BY order_date
    ORDER BY order_date
    """
    df = run_query(conn, query)
    if df is not None and not df.empty:
        fig, ax = plt.subplots()
        sns.lineplot(x='order_date', y='books_sold', data=df, ax=ax)
        ax.set_title('Sales Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Books Sold')
        plt.xticks(rotation=90)
        st.pyplot(fig)

# Streamlit UI


def main():
    st.title("BUML Model Data Visualization")

    conn = connect_to_db()
    if not conn:
        st.stop()

    st.sidebar.title("Navigation")
    choices = ["Tables View", "Join Combinations", "Visualizations"]
    choice = st.sidebar.selectbox("Choose View", choices)

    if choice == "Tables View":
        st.subheader("Available Tables")
        tables = ["Person", "Author", "Book", "Customer", "Orders", "OrderDetails"]
        table_choice = st.selectbox("Choose a table", tables)
        query = f"SELECT * FROM {table_choice}"
        df = run_query(conn, query)
        if df is not None:
            st.dataframe(df)

    elif choice == "Join Combinations":
        st.subheader("Join Table Combinations")
        join_choices = ["Author-Book", "Customer-Orders",
                        "Orders-OrderDetails", "Customer-Orders-OrderDetails"]
        join_choice = st.selectbox("Choose a join", join_choices)

        if join_choice == "Author-Book":
            query = """
            SELECT Person.name, Author.nationality, Book.title, Book.genre, Book.price
            FROM Author
            JOIN Person ON Author.Person_id = Person.Person_id
            JOIN Book ON Author.Author_id = Book.Author_id"""
        elif join_choice == "Customer-Orders":
            query = """
            SELECT Customer.Customer_id, Person.name, Customer.email, Orders.Orders_id, Orders.date
            FROM Customer
            JOIN Person ON Customer.Person_id = Person.Person_id
            JOIN Orders ON Customer.Customer_id = Orders.Customer_id"""
        elif join_choice == "Orders-OrderDetails":
            query = """
            SELECT Orders.Orders_id, Orders.date, OrderDetails.quantity, Book.title
            FROM Orders
            JOIN OrderDetails ON Orders.Orders_id = OrderDetails.Orders_id
            JOIN Book ON OrderDetails.Book_id = Book.Book_id"""
        elif join_choice == "Customer-Orders-OrderDetails":
            query = """
            SELECT Customer.Customer_id, Person.name, Customer.email, Orders.Orders_id, Orders.date, OrderDetails.quantity, Book.title
            FROM Customer
            JOIN Person ON Customer.Person_id = Person.Person_id
            JOIN Orders ON Customer.Customer_id = Orders.Customer_id
            JOIN OrderDetails ON Orders.Orders_id = OrderDetails.Orders_id
            JOIN Book ON OrderDetails.Book_id = Book.Book_id"""
        df = run_query(conn, query)
        if df is not None:
            st.dataframe(df)

    elif choice == "Visualizations":
        st.subheader("Data Visualizations")
        vis_choices = ["Books per Author", "Average Price by Genre",
                       "Orders per Customer", "Sales Over Time"]
        vis_choice = st.selectbox("Choose a visualization", vis_choices)

        if vis_choice == "Books per Author":
            plot_books_per_author(conn)
        elif vis_choice == "Average Price by Genre":
            plot_average_price_by_genre(conn)
        elif vis_choice == "Orders per Customer":
            plot_orders_per_customer(conn)
        elif vis_choice == "Sales Over Time":
            plot_sales_over_time(conn)


if __name__ == "__main__":
    main()
