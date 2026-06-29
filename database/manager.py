from loguru import logger
from aiosqlite import Connection, connect, Cursor
from utils.environ import get_database_file_path
from constants.database import MIGRATIONS
from database.objects import UserLinkData, UserPreferencesData

class Database:
    _connection: Connection
    async def _migrate(self):
        async with self._connection.cursor() as cursor:
            version_query = await cursor.execute("PRAGMA user_version")
            version = await version_query.fetchone()
            version = version[0]
            for ver, script in enumerate(MIGRATIONS, start=1):
                if version >= ver:
                    continue
                logger.info(f"Applying database migration {ver} / {len(MIGRATIONS)}...")
                await cursor.executescript(script)
                await cursor.execute(f"PRAGMA user_version = {ver}")
                await self._connection.commit()
                version = ver
    async def get_user(self, discord_id: int) -> tuple[UserLinkData, UserPreferencesData] | None:
        async with self._connection.cursor() as cursor:
            query = await cursor.execute("SELECT * FROM user_link WHERE discord_id = ?", (discord_id,))
            user = await query.fetchone()
            if not user:
                return None
        async with self._connection.cursor() as cursor:
            query = await cursor.execute("SELECT * FROM user_preferences WHERE discord_id = ?", (discord_id,))
            pref = await query.fetchone()
        return UserLinkData.from_sql_row(user), UserPreferencesData.from_sql_row(pref)
    async def add_user(self, discord_id: int, server_id: int):
        user = UserLinkData.new(discord_id, server_id)
        preferences = UserPreferencesData.new(discord_id)
        logger.debug(f"Linking user {server_id} to discord profile {discord_id}...")
        async with self._connection.cursor() as cursor:
            user_data = user.to_sql()
            pref_data = preferences.to_sql()
            await cursor.execute(user_data[0], user_data[1])
            await cursor.execute(pref_data[0], pref_data[1])
            await self._connection.commit()
    async def delete_user(self, discord_id):
        async with self._connection.cursor() as cursor:
            await cursor.execute("DELETE FROM user_link WHERE discord_id = ?", (discord_id,))
            await cursor.execute("DELETE FROM user_preferences WHERE discord_id = ?", (discord_id,))
            await self._connection.commit()
    @classmethod
    async def init(cls):
        db = cls()
        db._connection = await connect(get_database_file_path())
        await db._migrate()
        return db
    
database: Database = None