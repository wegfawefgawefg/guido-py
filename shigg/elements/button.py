from ._element_event import ElementEvent
from ._element import Element


class ButtonReleased(ElementEvent):
    def __init__(self, tag) -> None:
        super().__init__(tag)


class ButtonPressed(ElementEvent):
    def __init__(self, tag) -> None:
        super().__init__(tag)


class Button(Element):
    def __init__(
        self,
        position,
        scale,
        color=(200, 200, 200),
        text=None,
        texture=None,
        label=None,
        label_color=None,
        image=None,
        pressed_tag=None,
        released_tag=None,
    ) -> None:
        super().__init__()
        self.position = position
        self.scale = scale
        self.color = color
        self.text = text
        self.texture = texture
        self.label = label
        self.label_color = label_color
        self.image = image

        self.pressed_tag = pressed_tag
        self.released_tag = released_tag

        self.hovered = False
        self.pressed = False
        self.was_pressed = False

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        if not mouse_pressed and self.was_pressed:
            event = ButtonReleased(self.released_tag)
            self.was_pressed = False

        if (
            mouse_position.x > self.position.x
            and mouse_position.x < self.position.x + self.scale.x
            and mouse_position.y > self.position.y
            and mouse_position.y < self.position.y + self.scale.y
        ):
            self.hovered = True
        else:
            self.hovered = False

        if mouse_pressed and self.hovered:
            if self.pressed == False:
                event = ButtonPressed(self.pressed_tag)
            self.pressed = True
            self.was_pressed = True
        else:
            self.pressed = False

        return event
