from ._element_event import ElementEvent
from ._element import Element


class Label(Element):
    def __init__(
        self,
        position,
        scale,
        color=(200, 200, 200),
        text=None,
        text_color=(0, 0, 0),
        background_texture=None,
        label_color=None,
        image=None,
        no_background=False,
    ) -> None:
        super().__init__()
        self.position = position
        self.scale = scale
        self.color = color
        self.text = text
        self.text_color = text_color
        self.background_texture = background_texture
        self.label_color = label_color
        self.image = image
        self.no_background = no_background

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        pass
