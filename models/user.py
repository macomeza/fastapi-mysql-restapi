# Importar las clases y tipos desde SQLAlchemy 
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

# definir tabla users
users = Table(
    "users", meta, 
    Column("id", Integer, primary_key=True), 
    Column("name", String(255)), 
    Column("email", String(255), unique=True), #el email no puede ser repetido 
    Column("password", String(255))
)

meta.create_all(engine)