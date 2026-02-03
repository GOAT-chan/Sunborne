from utils.logger import Logger
from database.manager import DbSession
from database.models.user import User
from sqlmodel import select

def find_linked_profile(discord_id: int) -> User:
    statement = select(User).where(User.discord_id == discord_id)
    session = DbSession()
    results = session.execute_sql(statement)
    session.close()
    return results.one_or_none()