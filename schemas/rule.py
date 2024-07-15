import datetime

from pydantic import BaseModel


class RuleBasic(BaseModel):
    status_code: int
    account_user: list[str] | None = None
    account_group: list[str] | None = None
    email: list[str] | None = None


class Rule(RuleBasic):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class RuleCreate(RuleBasic):
    pass


class RuleUpdate(RuleBasic):
    status_code: int | None = None


class RuleMultipleUpdate(RuleUpdate):
    id: int
