import os

from utils.config import get_config
from utils.logger import Logger
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import ScalarResult
from database.models.user import User

DATABASE_PATH = os.path.join(os.getcwd(), "data", "sunborne.db")
SQL_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(SQL_URL)

def create_db():
    if not os.path.isfile(DATABASE_PATH):
        Logger.info("no exiting database found, generating one...")
        SQLModel.metadata.create_all(engine)
        Logger.success("database generated!")
    else:
        Logger.verbose("database already exists, loading that...")

class DbSession:
    session: Session
    def __init__(self):
        self.session = Session(engine)
    def add_or_update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user
    def remove(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
    def execute_sql(self, statement: str) -> ScalarResult:
        return self.session.exec(statement)
    def close(self):
        self.session.close()