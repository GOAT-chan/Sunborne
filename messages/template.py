from loguru import logger
from interactions import ContainerComponent, BaseComponent, SeparatorComponent, TextDisplayComponent, Color, SectionComponent, ThumbnailComponent, InteractiveComponent, ActionRow, Button, ButtonStyle, StringSelectMenu, StringSelectOption

class MessageTemplate:
    _components: list[BaseComponent]
    _color: int
    def __init__(self):
        self._components = []
        self._color = None
        self._template()
    def _add_component(self, component: BaseComponent):
        self._components.append(component)
    def _template(self):
        pass
    def set_accent_color(self, color_code: str):
        self._color = Color.from_hex(color_code).value
    def build_text(self, text: str) -> TextDisplayComponent:
        if text == "":
            logger.error("build_text failed: text must not be empty")
        return TextDisplayComponent(text)
    def build_button(self, id: str, label: str, style: ButtonStyle, url: str = None) -> Button:
        return Button(label=label,
                      style=style,
                      custom_id=id,
                      url=url)
    def build_selector_option(self, label: str, value: str, description: str = None, is_default: bool = False) -> StringSelectOption:
        option = StringSelectOption(label=label,
                                    value=value,
                                    default=is_default)
        if description:
            option.description = description
        return option
    def build_selector(self, id: str, options: list[StringSelectOption], placeholder_text: str = None, allow_multiple_selections: bool = False, min_selection: int = 1, max_selection: int = 1) -> StringSelectMenu:
        if len(options) < 1:
            logger.error("build_selector failed: at least one option is required")
            return
        if len(options) > 25:
            logger.error(f"build_selector failed: there can be no more than 25 unique options ({len(options)} currently)")
            return
        menu = StringSelectMenu(options,
                                custom_id=id)
        if placeholder_text:
            menu.placeholder = placeholder_text
        if allow_multiple_selections:
            menu.min_values = min_selection
            menu.max_values = max_selection
        return menu
    def insert_section(self, texts: list[TextDisplayComponent], image_url: str = None):
        if len(texts) < 1:
            logger.error("insert_section failed: at least one text display component is required")
            return
        if len(texts) > 3:
            logger.error(f"insert_section failed: there can be no more than 3 text components ({len(texts)} currently)")
            return
        section = SectionComponent(accessory=None)
        section.components = texts.copy()
        if image_url:
            section.accessory = ThumbnailComponent(image_url)
        self._add_component(section)
    def insert_separator(self):
        self._add_component(SeparatorComponent(divider=True))
    def insert_text(self, text: str):
        self._add_component(self.build_text(text))
    def insert_action_row(self, buttons: list[Button] = [], component: InteractiveComponent = None):
        if len(buttons) > 0 and component:
            logger.error("insert_action_row failed: there can only be 5 buttons, or one interactive component")
            return
        if len(buttons) > 5:
            logger.error(f"insert_action_row failed: there can be no more than 5 buttons ({len(buttons)} currently)")
            return
        row = ActionRow()
        if len(buttons) > 0:
            for button in buttons:
                row.add_component(button)
        elif component:
            row.add_component(component)
        self._add_component(row)
    def construct(self) -> ContainerComponent:
        container = ContainerComponent()
        container.accent_color = self._color
        for component in self._components:
            container.append(component)
        return container
    @classmethod
    def new(cls):
        return cls().construct()