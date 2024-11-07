from datetime import datetime

from pydantic import Field

from schemas.rule import RuleBasic, RuleUpdateBasic
from schemas.url import UrlBasic, UrlCreate, UrlUpdate


class APIRule(RuleBasic):
    id: int
    created_at: datetime
    updated_at: datetime


class APIUrl(UrlBasic):
    id: int
    rules: list[APIRule]

    created_at: datetime
    updated_at: datetime

class APIRuleCreate(RuleBasic):
    account_user: list[str] | None = Field(default_factory=list)
    account_group: list[str] | None = Field(default_factory=list)


class APIUrlCreate(UrlCreate):
    rules: list[APIRuleCreate]

class APIRuleUpdate(RuleUpdateBasic):
    id: int | None = None


class APIUrlUpdate(UrlUpdate):
    rules: list[APIRuleUpdate]


class APIUrlMultipleUpdate(APIUrlUpdate):
    id: int