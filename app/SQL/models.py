from datetime import datetime

from general_operator.app.SQL.database import Base
from sqlalchemy import Column, Integer, JSON, DateTime, Enum, String, ForeignKey, UniqueConstraint
from enum import Enum as PyEnum

from sqlalchemy.orm import relationship


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module = Column(String(256), nullable=False)
    submodule = Column(String(256), nullable=False)
    item = Column(String(256), nullable=False)
    path = Column(String(256), nullable=False)

    rules = relationship("Rule", cascade="all, delete", lazy="joined")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 最後更新時間

    __table_args__ = (
        UniqueConstraint('module', 'submodule', 'item', name='_module_submodule_item_uc'),
    )

class Method(PyEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    TRACE = "TRACE"

class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    url_id = Column(Integer, ForeignKey("url.id", ondelete="CASCADE"), nullable=False)
    method = Column(Enum(Method), nullable=False)
    status_code = Column(Integer, nullable=False)
    message_code = Column(String(256), default="", nullable=False)
    description = Column(String(256))
    account_user = Column(JSON)
    account_group = Column(JSON)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 最後更新時間