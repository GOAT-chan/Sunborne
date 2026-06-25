from config.config import Config

class AppConfig(Config):
    def _get_template(self):
        return {
            "health_check_interval": 120,
            "event_query_interval": 5,
            "channels": {
                "new_score_submission": [],
                "beatmap_ranking_changes": {
                    "ids": [],
                    "forum_tags": {
                        "mode_standard": "",
                        "mode_mania": "",
                        "mode_taiko": "",
                        "mode_catch": "",
                        "status_ranked": "",
                        "status_loved": "",
                        "status_approved": "",
                        "status_qualified": ""
                    }
                },
                "bot_health_reports": []
            }
        }
    
class EmojiConfig(Config):
    def _get_template(self):
        return {
        }