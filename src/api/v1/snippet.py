from datetime import datetime
import uuid

from fastapi import HTTPException, APIRouter
from starlette import status

from schemas.shorted_url import UrlCreate, ShortedUrl, UrlUpdate

url_router = APIRouter(prefix="/url", tags=['url'])


# Хранилище данных
urls = {
    1: {"id": 1, "shorted_url": "test1", "origin": "https://skillfactory.ru", "created_at": datetime.utcnow()},
    2: {"id": 2, "shorted_url": "test2", "origin": "https://example.com", "created_at": datetime.utcnow()},
}

# ---------------------------------------------------------------------------- #
# GET
# Нет типов, нет обработки ошибок


# @url_router.get("/")
# async def read_url(url_id):
#     url = urls[url_id]
#     return url


# ---------------------------------------------------------------------------- #
# GET c простой типизацией параметра и обработкой ошибок
# Нет схемы ответа.


# @url_router.get("/")
# async def read_url(url_id: int):
#     try:
#         url = urls[url_id]
#     except KeyError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
#     return url


# ---------------------------------------------------------------------------- #
# GET


@url_router.get("/{short_url}", responses={
    200: {"model": ShortedUrl},
    404: {"description": "URL not found"}
})
async def read_url(url_id: int):
    try:
        url = urls[url_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return url



# # ---------------------------------------------------------------------------- #
# POST


@url_router.post("/", response_model=ShortedUrl)
async def create_url(url: UrlCreate):
    new_id = max(urls)+1
    short_url = {
        "id": new_id,
        "origin": url.origin,
        "shorted_url": uuid.uuid4().hex,
        "created_at": datetime.utcnow()
    }

    urls.update({
        new_id: short_url
    })

    return short_url


# ---------------------------------------------------------------------------- #
# PUT


@url_router.put("/",responses={
    200: {"model": ShortedUrl},
    404: {"description": "URL not found"}
})
async def update_url(url: ShortedUrl):
    if url.id not in urls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    urls[url.id] = url.model_dump()
    return urls[url.id]


# ---------------------------------------------------------------------------- #
# PATCH


@url_router.patch("/{url_id}", responses={
    200: {"model": ShortedUrl},
    404: {"description": "URL not found"}
})
def update_url(url_id: int, url_update: UrlUpdate):
    if url_id not in urls:
        raise HTTPException(status_code=404, detail="URL not found")

    if url_update.shorted_url is not None:
        urls[url_id]["shorted_url"] = url_update.shorted_url

    if url_update.origin is not None:
        urls[url_id]["origin"] = url_update.origin

    return urls[url_id]


# ---------------------------------------------------------------------------- #
# DELETE


@url_router.delete("/", responses={
    200: {"description": "URL deleted successfully"},
    404: {"description": "URL not found"}
})
async def delete_url(url_id: int):
    if url_id not in urls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    del urls[url_id]
    return {"msg": "URL deleted successfully"}





















# from typing import List
#
# from db.db import db_dependency
# from services.shorted_url import get_url_by_id, get_url_by_shorted_url, get_urls, create_url, update_url, delete_url
#
#
# @url_router.post("/urls/", response_model=Url)
# async def create_url_view(url: UrlCreate, db: db_dependency):
#     db_url = await get_url_by_shorted_url(db, shorted_url=url.shorted_url)
#     if db_url:
#         raise HTTPException(status_code=400, detail="Shorted URL already exists")
#     return await create_url(db=db, origin=url.origin, shorted_url=url.shorted_url)
#
#
# @url_router.get("/urls/{url_id}", response_model=Url)
# async def read_url(url_id: int, db: db_dependency):
#     db_url = await get_url_by_id(db, url_id=url_id)
#     if db_url is None:
#         raise HTTPException(status_code=404, detail="URL not found")
#     return db_url
#
#
# @url_router.get("/urls/", response_model=List[Url])
# async def read_urls(db: db_dependency, skip: int = 0, limit: int = 10):
#     urls = await get_urls(db, skip=skip, limit=limit)
#     return urls
#
#
# @url_router.put("/urls/{url_id}", response_model=Url)
# async def update_url_view(url_id: int, url: UrlCreate, db: db_dependency):
#     db_url = await update_url(db, url_id=url_id, origin=url.origin, shorted_url=url.shorted_url)
#     if db_url is None:
#         raise HTTPException(status_code=404, detail="URL not found")
#     return db_url
#
#
# @url_router.delete("/urls/{url_id}", response_model=Url)
# async def delete_url_view(url_id: int, db: db_dependency):
#     db_url = await delete_url(db, url_id=url_id)
#     if db_url is None:
#         raise HTTPException(status_code=404, detail="URL not found")
#     return db_url
