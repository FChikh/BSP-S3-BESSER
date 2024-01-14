from jinja2 import Environment, FileSystemLoader
from sample_model import library_model


template_dir = '.'
env = Environment(loader=FileSystemLoader(template_dir),
                  trim_blocks=True, lstrip_blocks=True)

# Load the template
template = env.get_template('streamlit-template.py.j2')

# Define the data to fill in the placeholders
data = {
    "host": "localhost",
    "database": "streamlit-test",
    "user": "postgres",
    "password": "p@ssw0rd",
    "page_title": "Testing",
    "model": library_model
}

# Render the template with the data
generated_code = template.render(data)

# Print or save the generated code
with open("generated.py", "w") as f:
  f.write(generated_code)
