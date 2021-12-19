from typing import List

from fastapi import APIRouter, HTTPException, status

from ch3_restful_api.chapter3_project.models.user import *  # User, UserCreate
from ch3_restful_api.chapter3_project.db import *  # db

router = APIRouter()

# @router.get("/")
# async def all() -> List[User]:
#     return list(db.users.values())
