from datetime import datetime

class Beatmap:
    set_id: int
    diff_id: int
    title: str
    mapper: str
    artist: str
    diff: str
    length: int
    mode_id: int
    mode_name: str
    last_updated: datetime
    sr: float
    status: str
    max_combo: int
    circle_count: int
    slider_count: int
    spinner_count: int
    ar: int
    cs: int
    hp_drain: int
    acc: int
    bpm: int
    def __init__(self):
        self.set_id = 0
        self.diff_id = 0
        self.title = ""
        self.mapper = ""
        self.artist = ""
        self.diff = ""
        self.length = 0
        self.mode_id = 0
        self.mode_name = ""
        self.last_updated = datetime.now()
        self.sr = 0
        self.status = ""
        self.max_combo = 0
        self.circle_count = 0
        self.slider_count = 0
        self.spinner_count = 0
        self.ar = 0
        self.cs = 0
        self.hp_drain = 0
        self.acc = 0
        self.bpm = 0