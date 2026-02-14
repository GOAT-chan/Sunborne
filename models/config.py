from turtle import st
from pydantic import BaseModel, Field

class Config(BaseModel):
    health_check_interval: int
    event_query_interval: int
    only_send_health_check_embed_when_failed: bool
    embed_colors: EmbedColors
    channels: Channels
    emojis: Emojis
    privileged_users: list[int]

class EmbedColors(BaseModel):
    success: str
    error: str
    info: str
    privileged: str
    new_score: str
    beatmap_status_change: str

class BeatmapRankingTag(BaseModel):
    ranked: str
    loved: str
    approved: str

class BeatmapGamemodeTag(BaseModel):
    std: str = Field(alias="Standard")
    mania: str = Field(alias="Mania")
    taiko: str = Field(alias="Taiko")
    ctb: str = Field(alias="CatchTheBeat")

class BeatmapTag(BaseModel):
    status: BeatmapRankingTag
    gamemode: BeatmapGamemodeTag

class Channels(BaseModel):
    beatmap_status: int | None
    score_submission: int | None
    health_check: int | None
    beatmap_status_post_tags: BeatmapTag

class Emojis(BaseModel):
    xh_rank: str
    x_rank: str
    sh_rank: str
    s_rank: str
    a_rank: str
    b_rank: str
    c_rank: str
    d_rank: str
    judge_300: str = Field(alias="300")
    judge_100: str = Field(alias="100")
    judge_50: str = Field(alias="50")
    judge_miss: str = Field(alias="miss")
    dev_role: str
    admin_role: str
    bat_role: str
    ranked: str
    approved: str
    qualified: str
    loved: str
    pending: str
    wip: str
    graveyard: str
    ar: str
    cs: str
    od: str
    bpm: str
    hp: str
    sr: str
    std_gm: str
    mania_gm: str
    taiko_gm: str
    ctb_gm: str