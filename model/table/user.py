from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime

from model.table import metadata

# 用户表
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), comment="名字"),
    Column("age", Integer, comment="年龄"),
    Column("sex", Integer, comment="性别"),
    Column("create_time", DateTime, default=datetime.now, comment="创建时间"),
    Column(
        "update_time",
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    ),
)
