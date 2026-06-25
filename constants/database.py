MIGRATIONS = [
    """
    CREATE TABLE IF NOT EXISTS user_link (
        discord_id INTEGER NOT NULL,
        server_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        PRIMARY KEY (discord_id, server_id)
    );

    CREATE TABLE IF NOT EXISTS user_preferences (
        discord_id INTEGER PRIMARY KEY NOT NULL,
        last_changed INTEGER NOT NULL
    );
    """
]