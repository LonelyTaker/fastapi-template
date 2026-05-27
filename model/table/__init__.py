from sqlalchemy import MetaData

metadata = MetaData()

from .account import account_table
from .user import user_table

__all__ = ["metadata", "account_table", "user_table"]
