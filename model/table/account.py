from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Index

from model.table import metadata

# 账号表
account_table = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("account", String(50), comment="账号"),
    Column("password", String(255), comment="密码"),
    Column("create_time", DateTime, default=datetime.now, comment="创建时间"),
    Column(
        "update_time",
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    ),
    Index("uk_account", "account", unique=True),
)
