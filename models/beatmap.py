from datetime import datetime

class BeatmapStats:
    sr: float
    max_combo: int
    circle_count: int
    slider_count: int
    spinner_count: int
    ar: float
    cs: float
    drain: float
    od: float
    bpm: float
    pp: float
    pp_acc: float
    pp_aim: float
    pp_speed: float
    def __init__(self):
        self.sr = 0
        self.max_combo = 0
        self.circle_count = 0
        self.slider_count = 0
        self.spinner_count = 0
        self.ar = 0
        self.cs = 0
        self.drain = 0
        self.od = 0
        self.bpm = 0
        self.pp = 0
        self.pp_acc = 0
        self.pp_aim = 0
        self.pp_speed = 0

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
    status: str
    stats: BeatmapStats
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
        self.status = ""
        self.stats = BeatmapStats()