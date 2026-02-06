from utils.logger import Logger
from database.manager import DbSession
from database.models.user import User
from sqlmodel import select

async def find_linked_profile(discord_id: int) -> User | None:
    statement = select(User).where(User.discord_id == discord_id)
    session = DbSession()
    results = await session.execute_sql(statement)
    await session.close()
    return results.one_or_none()

async def check_if_user_id_is_claimed(user_id: int) -> bool:
    statement = select(User).where(User.user_id == user_id)
    session = DbSession()
    result = await session.execute_sql(statement)
    await session.close()
    if not result.first():
        return False
    return True