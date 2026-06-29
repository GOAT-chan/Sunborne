from interactions import ButtonStyle
from messages.template import MessageTemplate
from api.endpoints.user import BasicUser
from utils.country import get_country_emoji, get_country_name
from utils.time import to_discord_date

class ProfileLinkPromptMessage(MessageTemplate):
    user: BasicUser
    def __init__(self, user: BasicUser):
        self.user = user
        super().__init__()
    def _template(self):
        self.insert_text("## Profile Linking")
        self.insert_text("Please confirm your profile information.")
        self.insert_separator()
        detail_text = f"""• **Country**: {get_country_emoji(self.user.country)} {get_country_name(self.user.country)}
• **Joined at**: {to_discord_date(self.user.registered_date)}
• **Preferred Game Mode**: {self.user.default_gamemode.name}
• **Description**:
"""
        self.insert_section(texts=[self.build_text(f"### {self.user.name}"),
                                   self.build_text(detail_text),
                                   self.build_text(f"```\n{self.user.description}\n```")],
                            image_url=self.user.avatar_url)
        self.insert_action_row(buttons=[self.build_button(id="accept_link_button",
                                                          label="Link",
                                                          style=ButtonStyle.SECONDARY)])
        self.insert_text("-# This prompt will expire after 2 minutes.")
    @classmethod
    def new(cls, user: BasicUser):
        return cls(user).construct()

class UserPreferenceMessage(MessageTemplate):
    def _template(self):
        self.insert_text("## Preferences")
        self.insert_text("You can change various bot settings here.")
        self.insert_separator()
        self.insert_text("### Score Post")
        self.insert_text("Change how your scores are posted to #scores")
        self.insert_action_row(component=self.build_selector(options=[self.build_selector_option("All scores", "all_score", "Post all new scores that you set.", True),
                                                                      self.build_selector_option("New top plays only", "only_top_plays", "Only post new top plays that you set."),
                                                                      self.build_selector_option("Disable", "no_posting", "Do not post any scores at all.")],
                                                             id="score_post_preference_selector"))