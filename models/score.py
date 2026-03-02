from datetime import datetime
from models.beatmap import Beatmap
from models.user import UserProfile

class Score:
    user: UserProfile
    beatmap: Beatmap
    score_id: int
    date: datetime
    mods: str | None
    score: int
    accuracy: float
    pp: float
    grade: str
    count_300: int
    count_100: int
    count_50: int
    count_miss: int
    gamemode: str
    max_combo: int
    def __init__(self):
        self.user = UserProfile()
        self.beatmap = Beatmap()
        self.score_id = 0
        self.date = datetime.now()
        self.mods = ""
        self.score = 0
        self.pp = 0
        self.grade = ""
        self.count_300 = 0
        self.count_100 = 0
        self.count_50 = 0
        self.count_miss = 0
        self.gamemode = ""
        self.max_combo = 0