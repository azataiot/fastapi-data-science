# models.py

from datetime import datetime
from typing import Optional
import sqlalchemy
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


""" metadata object: It's role is to keep all the information of a database schema together.
This is why you should create it only once in your whole project and always use the same one throughout.
"""
metadata = sqlalchemy.MetaData()

# we will define a table using the Table class
posts = sqlalchemy.Table(
    #  first argument is the name of the table, followed by the metadata object.
    "posts",
    metadata,
    # we list all the columns that should be defined in our table
    # name of the column, followed by its type and a certain number of options.
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text(), nullable=False)
)
