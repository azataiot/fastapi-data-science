from typing import List, Tuple

from databases import Database

from fastapi import Depends, FastAPI, HTTPException, Query, status

from .database import get_database, sqlalchemy_engine
from .models import metadata, posts, PostDB, PostCreate, PostPatch

app = FastAPI()


# Decorating functions with the on_event decorators allows us to trigger some useful logic when FastAPI starts or stops.
@app.on_event("startup")
async def startup():
    # This will ensure that the database connection is open and ready to process requests.
    await get_database().connect()
    # The goal of this method is to create the table's schema inside our database.
    # This method is designed to work with a standard SQLAlchemy engine; this is why we instantiated it earlier.
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def get_pagination(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=10)
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return skip, capped_limit


async def get_post_or_404(
        post_id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == post_id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
        pagination: Tuple[int, int] = Depends(get_pagination),
        database: Database = Depends(get_database),
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    results = [PostDB(**row) for row in rows]
    return results


@app.get("/posts/{id}")
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
        post: PostCreate,
        database: Database = Depends(get_database),
) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)
    post_db = await get_post_or_404(post_id, database)
    return post_db


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
        post_update: PostPatch,
        post: PostDB = Depends(get_post_or_404),
        database: Database = Depends(get_database)
) -> PostDB:
    update_query = (
        posts.update().where(posts.id == id).values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)
    post_db = await get_post_or_404(post_id, database)
    return post_db


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)):
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)
