from enum import Enum

from pydantic import BaseModel


class Log(BaseModel):
    timestamp: float
    module: str
    submodule: str
    item: str
    method: str
    status_code: str
    message_code: str | None = None
    message: str | None = None
    response_size: str | None = None
    account: str | None = None
    ip: str | None = None
    api_url: str | None = None
    web_path: str | None = None
