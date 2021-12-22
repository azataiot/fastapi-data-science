import sqlalchemy
from databases import Database

# database.py

# database engine, followed by authentication information and the hostname of the database server.
DATABASE_URL = "sqlite:///./db.data"
# we instantiate a Database instance using this URL.
# This is the connection layer provided by databases that will allow us to perform asynchronous queries.
database = Database(DATABASE_URL)
# We also define sqlalchemy_engine, which is the standard synchronous connection object provided by SQLAlchemy
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


# we define a simple function whose role is to simply return the database instance.
def get_database() -> Database:
    return database
