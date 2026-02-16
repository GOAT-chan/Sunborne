import os

from utils.logger import Logger
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy import ScalarResult
from database.models.user import User

DATABASE_PATH = os.path.join(os.getcwd(), "data", "sunborne.db")
SQL_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

engine = create_async_engine(SQL_URL)

async def create_db():
    if not os.path.isfile(DATABASE_PATH):
        Logger.info("no exiting database found, generating one...")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        Logger.success("database generated!")
    else:
        Logger.verbose("database already exists, loading that...")

class DbSession:
    session: AsyncSession
    def __init__(self):
        self.session = AsyncSession(engine)
    async def add_or_update(self, user: User):
        self.session.add(user)
        await self.session.commit()
    async def remove(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
    async def execute_sql(self, statement: str) -> ScalarResult:
        return await self.session.exec(statement)
    async def close(self):
        await self.session.close()