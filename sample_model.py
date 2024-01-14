from BUML.metamodel.structural.structural import Association, Class, Multiplicity, Property, BinaryAssociation, PrimitiveDataType, DomainModel
from BUML.metamodel.structural.structural import Association, Class, Multiplicity, Property, BinaryAssociation,\
PrimitiveDataType, DomainModel, Generalization

person_name: Property = Property(
    name="name", owner=None, property_type=PrimitiveDataType('str'))

person_class: Class = Class(name="Person", attributes=set(
    [person_name]), is_abstract=True)

author_natonality: Property = Property(
    name="nationality", owner=None, property_type=PrimitiveDataType('str'))

author_class: Class = Class(name="Author", attributes=set(
    [author_natonality]))

author_from_person: Generalization = Generalization(general=person_class, specific=author_class)

book_title: Property = Property(
    name="title", owner=None, property_type=PrimitiveDataType('str'))
book_genre: Property = Property(
    name="genre", owner=None, property_type=PrimitiveDataType('str'))
book_price: Property = Property(
    name="price", owner=None, property_type=PrimitiveDataType('float'))

book_class: Class = Class(name="Book", attributes=set(
    [book_title, book_genre, book_price]))

customer_login: Property = Property(
    name="login", owner=None, property_type=PrimitiveDataType('str'))
customer_email: Property = Property(
    name="email", owner=None, property_type=PrimitiveDataType('str'))

customer_class: Class = Class(name="Customer", attributes=set(
    [customer_login, customer_email]))

customer_from_person: Generalization = Generalization(general=person_class, specific=customer_class)

order_date: Property = Property(
    name="date", owner=None, property_type=PrimitiveDataType('datetime'))

order_class: Class = Class(name="Orders", attributes=set(
    [order_date]))

details_quantity: Property = Property(
    name="quantity", owner=None, property_type=PrimitiveDataType('int'))

details_class: Class = Class(name="OrderDetails", attributes=set(
    [details_quantity]))

# Ends definition
# one Author - many Books
author_writes: Property = Property(
    name="writes", owner=None, property_type=author_class, multiplicity=Multiplicity(1, 1))
book_writes: Property = Property(
    name="writes", owner=None, property_type=book_class, multiplicity=Multiplicity(0, "*"))

# One customer - many orders
customer_places: Property = Property(
    name="places", owner=None, property_type=customer_class, multiplicity=Multiplicity(1, 1))
order_places: Property = Property(
    name="places", owner=None, property_type=order_class, multiplicity=Multiplicity(0, "*"))

# Many Order - Many Books => intermediate table OrderDetails

# One Order - many OrderDetails
order_contains: Property = Property(
    name="contains", owner=None, property_type=order_class, multiplicity=Multiplicity(1, 1))
details_contains: Property = Property(
    name="contains", owner=None, property_type=details_class, multiplicity=Multiplicity(1, "*"))

# One book - many OrderDetails
book_included: Property = Property(
    name="included", owner=None, property_type=book_class, multiplicity=Multiplicity(1, 1))
details_included: Property = Property(
    name="included", owner=None, property_type=details_class, multiplicity=Multiplicity(0, "*"))

# BinaryAssociation definition
relation_writes: BinaryAssociation = BinaryAssociation(
    name="writes", ends={author_writes, book_writes})
relation_places: BinaryAssociation = BinaryAssociation(
    name="places", ends={order_places, customer_places})
relation_contains: BinaryAssociation = BinaryAssociation(
    name="contains", ends={order_contains, details_contains})
relation_included: BinaryAssociation = BinaryAssociation(
    name="included", ends={book_included, details_included})


library_model: DomainModel = DomainModel(name="BookStore", types={
    person_class, author_class, book_class, customer_class, order_class, details_class}, 
    associations={relation_writes, relation_places, relation_contains, relation_included}, 
    generalizations={author_from_person, customer_from_person}, packages=None, constraints=None)


########
# CINEMA MODEL


movie_year: Property = Property(
    name="year", owner=None, property_type=PrimitiveDataType('int'))
movie_length: Property = Property(
    name="length", owner=None, property_type=PrimitiveDataType('int'))
movie_title: Property = Property(
    name="title", owner=None, property_type=PrimitiveDataType('str'))

studio_name: Property = Property(
    name="name", owner=None, property_type=PrimitiveDataType('str'))
studio_address: Property = Property(
    name="address", owner=None, property_type=PrimitiveDataType('str'))

star_name: Property = Property(
    name="name", owner=None, property_type=PrimitiveDataType('str'))
star_age: Property = Property(
    name="age", owner=None, property_type=PrimitiveDataType('int'))

# Classes definition
movie_class: Class = Class(name="movie", attributes=set(
    [movie_length, movie_year, movie_title]))
studio_class: Class = Class(
    name="studio", attributes=set([studio_name, studio_address]))
star_class: Class = Class(name="star", attributes=set([star_name, star_age]))


# Ends definition
# One star can play in many movies, in one movie there are many stars
movie_starring: Property = Property(
    name="starring", owner=None, property_type=movie_class, multiplicity=Multiplicity(0, "*"))
star_starred_in: Property = Property(
    name="starredIn", owner=None, property_type=star_class, multiplicity=Multiplicity(0, "*"))

# Movie can be owned only by one studio
movie_owned_by: Property = Property(
    name="ownedBy", owner=None, property_type=movie_class, multiplicity=Multiplicity(0, "*"))
studio_owns: Property = Property(
    name="owns", owner=None, property_type=studio_class, multiplicity=Multiplicity(1, 1))

star_contract: Property = Property(
    name="star_contract", owner=None, property_type=star_class, multiplicity=Multiplicity(0, "*"))
studio_contract: Property = Property(
    name="studio_contract", owner=None, property_type=studio_class, multiplicity=Multiplicity(1, 1))
movie_contract: Property = Property(
    name="movie_contract", owner=None, property_type=movie_class, multiplicity=Multiplicity(0, "*"))

# BinaryAssociation definition
relation_stars: BinaryAssociation = BinaryAssociation(
    name="stars", ends={movie_starring, star_starred_in})
relation_owns: BinaryAssociation = BinaryAssociation(
    name="owns", ends={movie_owned_by, studio_owns})

# Association definition
relation_contracts: Association = Association(
    name="contract", ends={star_contract, studio_contract, movie_contract})

model_cinema: DomainModel = DomainModel(name="Cinema", types={
    movie_class, studio_class, star_class}, associations={relation_owns, relation_stars, relation_contracts}, generalizations=None, packages=None, constraints=None)
