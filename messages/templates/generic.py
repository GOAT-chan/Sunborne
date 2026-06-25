from messages.template import MessageTemplate

class SimpleMessage(MessageTemplate):
    title: str
    message: str
    color: str
    def __init__(self, title: str, message: str, color: str):
        self.title = title
        self.message = message
        self.color = color
        super().__init__()
    def _template(self):
        self.set_accent_color(self.color)
        self.insert_text(self.title)
        self.insert_separator()
        self.insert_text(self.message)
    @classmethod
    def new(cls, title: str, content: str, color: str):
        return cls(title, content, color).construct()
    
class ErrorMessage(SimpleMessage):
    @classmethod
    def new(cls, content: str):
        return cls("## Error", content, "#b31e46").construct()
    
class SuccessMessage(SimpleMessage):
    @classmethod
    def new(cls, content: str):
        return cls("## Success", content, "#4fb35f").construct()