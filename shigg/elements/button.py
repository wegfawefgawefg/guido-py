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
        tag=None,
    ) -> None:
        super().__init__(tag)

        self.position = position
        self.scale = scale
        self.color = color
        self.text = text
        self.texture = texture
        self.label = label
        self.label_color = label_color
        self.image = image

        self.hovered = False
        self.pressed = False
        self.was_pressed = False

    def step(self, mouse_position, mouse_pressed, resolution):
        event = None
        absolute_position = resolution * self.position
        absolute_dimensions = resolution * self.scale

        if not mouse_pressed and self.was_pressed:
            event = ButtonReleased(self.tag)
            self.was_pressed = False

        if (
            mouse_position.x > absolute_position.x
            and mouse_position.x < absolute_position.x + absolute_dimensions.x
            and mouse_position.y > absolute_position.y
            and mouse_position.y < absolute_position.y + absolute_dimensions.y
        ):
            self.hovered = True
        else:
            self.hovered = False

        if mouse_pressed and self.hovered:
            if self.pressed == False:
                event = ButtonPressed(self.tag)
            self.pressed = True
            self.was_pressed = True
        else:
            self.pressed = False

        return event
