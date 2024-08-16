from datetime import datetime
from pydantic import BaseModel

from schemas.rule import Rule


class UrlBasic(BaseModel):
    module: str
    submodule: str
    item: str
    path: str

class Url(UrlBasic):
    id: int
    rules: list[Rule]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UrlCreate(UrlBasic):
    pass

class UrlUpdate(UrlBasic):
    module: str | None = None
    submodule: str | None = None
    item: str | None = None
    path: str | None = None

class UrlMultipleUpdate(UrlUpdate):
    id: int
