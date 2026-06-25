from datetime import datetime
from enum import StrEnum

class TimeFormat(StrEnum):
    HHMMSS = "%H:%M:%S"
    DDMMYYYY = "%d/%m/%Y"
    MMDDYYYY = "%m/%d/%Y"
    LOG_FILE_TIMESTAMP = "%Y-%m-%d"

def get_current_time(format: TimeFormat) -> str:
    return datetime.now().strftime(format.value)

def from_iso8601(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)

def to_discord_date(time: datetime) -> str:
    return f"<t:{int(time.timestamp())}:D>"