import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from api import api_router
from core.config import uvicorn_options
from sqlalchemy import text

from core.logger import LOGGING_CONFIG
from db.db import db_dependency


logger = logging.getLogger("my_app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/openapi"
)

app.include_router(api_router)


class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"CustomException: {exc.name} at {request.url}")
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a custom error."},
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise CustomException(name="Item 3")
    return {"item_id": item_id}


@app.get('/ping')
async def ping():
    logging.basicConfig(level="INFO")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")




if __name__ == '__main__':
    # print для отображения настроек в терминале при локальной разработке
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
