import datetime

from general_operator.app.SQL.database import Base
from sqlalchemy import Column, Integer, JSON, DateTime


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status_code = Column(Integer, nullable=False)
    account_user = Column(JSON)
    account_group = Column(JSON)
    email = Column(JSON)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 最後更新時間