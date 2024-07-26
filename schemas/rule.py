from datetime import datetime
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel


class Method(str, Enum):
    GET= "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


class RuleBasic(BaseModel):
    method: Method
    status_code: int
    message_code: str
    description: str
    account_user: list[str]
    account_group: list[str]


class Rule(RuleBasic):
    id: int
    url_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RuleCreate(RuleBasic):
    url_id: int
    account_user: list[str] | None = list()
    account_group: list[str] | None = list()

class RuleUpdateBasic(RuleBasic):
    method: Method | None = None
    status_code: int | None = None
    message_code: str | None = None
    description: str | None = None
    account_user: list[str] | None = None
    account_group: list[str] | None = None


class RuleUpdate(RuleUpdateBasic):
    url_id: int | None = None

class RuleMultipleUpdate(RuleUpdate):
    id: int
