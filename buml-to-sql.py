import sys
from generators.sql.sql_generator import SQLGenerator
from generators.django.django_generator import DjangoGenerator

from sample_model import library_model

a = DjangoGenerator(model=library_model)
a.generate()

b = SQLGenerator(model=library_model)
b.generate()
