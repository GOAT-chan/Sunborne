from datetime import datetime

class UserGrades:
    rank_xh: int
    rank_x: int
    rank_sh: int
    rank_s: int
    rank_a: int
    rank_b: int
    rank_c: int
    rank_d: int
    def __init__(self):
        self.rank_xh = 0
        self.rank_x = 0
        self.rank_sh = 0
        self.rank_s = 0
        self.rank_a = 0
        self.rank_b = 0
        self.rank_c = 0
        self.rank_d = 0

class UserGameModeStats:
    gamemode: str
    global_rank: int
    country_rank: int
    total_score: int
    ranked_score: int
    accuracy: float
    total_pp: int
    grades: UserGrades
    max_combo: int
    play_time: int
    play_count: int
    peak_global_rank: int
    peak_global_rank_date: datetime
    peak_country_rank: int
    peak_country_rank_date: datetime
    medals: int
    def __init__(self):
        self.gamemode = ""
        self.global_rank = 0
        self.country_rank = 0
        self.total_score = 0
        self.ranked_score = 0
        self.accuracy = 0
        self.total_pp = 0
        self.grades = UserGrades()
        self.max_combo = 0
        self.play_time = 0
        self.play_count = 0
        self.peak_country_rank = 0
        self.peak_global_rank_date = datetime.now()
        self.peak_country_rank = 0
        self.peak_country_rank_date = datetime.now()
        self.medals = 0

class UserProfile:
    user_name: str
    user_id: int
    avatar_url: str
    banner_url: str
    description: str
    country_code: str
    registration_date: datetime
    last_online: datetime
    default_gamemode: str
    restricted: bool
    badges: list[str]
    status: str
    followers: int
    following: int
    stats: UserGameModeStats
    def __init__(self):
        self.user_name = ""
        self.user_id = 0
        self.avatar_url = ""
        self.banner_url = ""
        self.description = ""
        self.country_code = ""
        self.registration_date = datetime.now()
        self.last_online = datetime.now()
        self.default_gamemode = ""
        self.restricted = False
        self.badges = []
        self.status = ""
        self.followers = 0
        self.following = 0
        self.stats = UserGameModeStats()
