from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
from sqlalchemy import text
import os 

# Creating a FastAPI server
server = FastAPI(title='User API')

# Creating a connection to the database
mysql_url = os.environ.get("MYSQL_URL")  # Update with your environment variable name
mysql_user = 'root'
mysql_password = os.environ.get("MYSQL_PASSWORD")  # Update with your environment variable name
database_name = 'Main'

# Recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Creating the connection
mysql_engine = create_engine(connection_url)

# Creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'

@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1

@server.get('/users')
async def get_users():
    try:
        with mysql_engine.connect() as connection:
            query = text('SELECT * FROM Users;')
            results = connection.execute(query)

        results = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
                ) for i in results.fetchall()]
        return results
    except Exception as e:
        # Handle the exception and return an HTTP 500 response
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    try:
        with mysql_engine.connect() as connection:
            q=f'SELECT * FROM Users WHERE Users.id = {user_id}'
            query = text(q)
            results = connection.execute(query)
              
        results = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
                ) for i in results.fetchall()]

        if len(results) == 0:
            raise HTTPException(
                status_code=404,
                detail='Unknown User ID')
        else:
            return results[0]
    except Exception as e:
        # Handle the exception and return an HTTP 500 response
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )