from interactions import Embed, Color, EmbedAttachment, EmbedAuthor, EmbedFooter, EmbedField

class EmbedBuilder:
    header: str
    header_image_url: str
    header_url: str
    thumbnail_image_url: str
    image_url: str
    title: str
    title_url: str
    contents: str
    color: str
    footer: str
    footer_image_url: str
    fields: list[EmbedField]
    def __init__(self):
        self.header = ""
        self.header_image_url = ""
        self.header_url = ""
        self.thumbnail_image_url = ""
        self.image_url = ""
        self.title = ""
        self.title_url = ""
        self.contents = ""
        self.color = ""
        self.footer = ""
        self.footer_image_url = ""
        self.fields = []
    def build(self) -> Embed:
        return Embed(
            title=self.title,
            description=self.contents,
            color=Color.from_hex(self.color),
            author=EmbedAuthor(
                name=self.header,
                icon_url=self.header_image_url,
                url=self.header_url
            ),
            thumbnail=self.thumbnail_image_url,
            images=[
                EmbedAttachment(self.image_url)
            ],
            footer=EmbedFooter(
                text=self.footer,
                icon_url=self.footer_image_url
            ),
            fields=self.fields
        )
    def set_header(self, text: str, image_url: str = None, url: str = None):
        self.header = text
        self.header_image_url = image_url
        self.header_url = url
    def set_footer(self, text: str, image_url: str = None):
        self.footer = text
        self.footer_image_url = image_url
    def set_thumbnail_image(self, url: str):
        self.thumbnail_image_url = url
    def set_image(self, url: str):
        self.image_url = url
    def set_title(self, title: str, url: str = None):
        self.title = title
        self.title_url = url
    def set_color(self, color: str):
        self.color = color
    def add_content(self, msg: str):
        self.contents += msg + "\n"
    def clear_content(self):
        self.contents = ""
    def add_field(self, title: str, content: str, inline: bool = False):
        self.fields.append(EmbedField(
            name=title,
            value=content,
            inline=inline
        ))