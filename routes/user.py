from fastapi import APIRouter, Response, status
from sqlalchemy import select, insert, delete, update
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
import logging
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Key generation should be done once and stored securely in a real app
key = Fernet.generate_key()  # Consider using a fixed key stored in a config
f = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    result = conn.execute(select(users)).fetchall()
    # Convert the SQLAlchemy Row objects to dictionaries
    users_list = [dict(row._mapping) for row in result]  # Use _mapping to get a dict representation
    return users_list

@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: int):
    result = conn.execute(users.select().where(users.c.id == id)).first()

    if result is None:
        return {"error": "User not found"}, 404

    # Attempt to convert to dictionary using _mapping or manual method
    user_data = dict(result._mapping)
    
    return user_data

@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: int, user: User):
    # Check if the user exists
    existing_user = conn.execute(users.select().where(users.c.id == id)).first()

    if existing_user is None:
        return {"error": "User not found"}, 404

    # Proceed with the update
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    
    conn.commit()
    logger.info(f"User updated with ID: {id}")
    return {"message": "User updated successfully"}

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int):
    # Check if the user exists
    existing_user = conn.execute(users.select().where(users.c.id == id)).first()

    if existing_user is None:
        return {"error": "User not found"}, 404
    
    # Proceed with the deletion
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    logger.info(f"User deleted with ID: {id}")

    return Response(status_code=HTTP_204_NO_CONTENT)

@user.post("/users", response_model=User, tags=["users"])
def create_users(user: User):
    logger.info(f"Creating user: {user}")
    
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": f.encrypt(user.password.encode("utf-8"))
    }
    
    result = conn.execute(users.insert().values(new_user))
    conn.commit() 
    logger.info(f"User created with ID: {result.lastrowid}")

    created_user = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    
    if created_user:
        logger.info(f"Retrieved user: {created_user}")
        return {
            "id": created_user[0],
            "name": created_user[1],
            "email": created_user[2],
            "password": created_user[3]  # Be cautious about returning passwords in plaintext.
        }

    else:
        logger.error("User not found after creation")
        return {"error": "User not found"}, 404