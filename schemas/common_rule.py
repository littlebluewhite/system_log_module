from datetime import datetime
from pydantic import BaseModel, Field


class CommonRuleBasic(BaseModel):
    status_code: int
    message_code: str | None = None
    description: str | None = None
    account_group: list[str]
    account_user: list[str]


class CommonRule(CommonRuleBasic):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommonRuleCreate(CommonRuleBasic):
    account_user: list[str] | None = Field(default_factory=list)
    account_group: list[str] | None = Field(default_factory=list)

class CommonRuleUpdate(CommonRuleBasic):
    status_code: int | None = None
    message_code: str | None = None
    description: str | None = None
    account_user: list[str] | None = None
    account_group: list[str] | None = None

class CommonRuleUpdateMultipleUpdate(CommonRuleUpdate):
    id: int
