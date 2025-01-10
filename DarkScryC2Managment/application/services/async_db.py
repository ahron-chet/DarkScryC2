# application/services/database/dbmanager.py
# from .table_managers.users.manager import UserManager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class DBManager:
    def __init__(self, connection_string: str) -> None:
        self.engine = create_async_engine(connection_string, echo=False)
        self.SessionLocal = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )
        # self.user_manager = UserManager(self.SessionLocal)
