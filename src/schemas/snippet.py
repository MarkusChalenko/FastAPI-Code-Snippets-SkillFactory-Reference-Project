from pydantic import BaseModel, HttpUrl
from datetime import datetime

from typing import Optional


class UrlBase(BaseModel):
    origin: HttpUrl


class UrlCreate(UrlBase):
    pass


class UrlUpdate(UrlBase):
    origin: Optional[HttpUrl] = None
    shorted_url: Optional[str] = None


class ShortedUrl(UrlBase):
    id: int
    shorted_url: str
    created_at: Optional[datetime] = None
