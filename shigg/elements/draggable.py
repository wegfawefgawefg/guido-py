from ._element_event import ElementEvent
from ._element import Element


class DraggableReleased(ElementEvent):
    def __init__(self, tag) -> None:
        super().__init__(tag)


class DraggablePressed(ElementEvent):
    def __init__(self, tag) -> None:
        super().__init__(tag)


class DraggableMoved(ElementEvent):
    def __init__(self, tag) -> None:
        super().__init__(tag)


class Draggable(Element):
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
        moved_tag=None,
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
        self.moved_tag = moved_tag

        self.hovered = False
        self.being_dragged = True
        self.mouse_last_position = None
        self.was_pre_hovered = False
        self.pre_hover_countdown = 0

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        """For the section below, order of these clauses does matter.
        """

        # check hovered
        if (
            mouse_position.x > self.position.x
            and mouse_position.x < self.position.x + self.scale.x
            and mouse_position.y > self.position.y
            and mouse_position.y < self.position.y + self.scale.y
        ):
            self.hovered = True
        else:
            self.hovered = False

        # check if mouse hovered without clicking first
        # this is important so we dont also shove all draggables we drag through
        if self.hovered and not mouse_pressed and not self.being_dragged:
            self.was_pre_hovered = True
            self.pre_hover_countdown = 3

        # if you didnt get dragged within a frame, disable prehover
        self.pre_hover_countdown -= 1
        self.pre_hover_countdown = max(self.pre_hover_countdown, 0)
        if self.pre_hover_countdown == 0:
            self.was_pre_hovered = False

        # check drag start
        if (
            self.was_pre_hovered
            and not self.being_dragged
            and mouse_pressed
            and self.hovered
        ):
            self.being_dragged = True
            self.mouse_last_position = mouse_position
            event = DraggablePressed(self.pressed_tag)
            self.was_pre_hovered = False
            self.pre_hover_countdown = 0

        # check drag finished
        if self.being_dragged and not mouse_pressed:
            self.being_dragged = False
            event = DraggableReleased(self.released_tag)

        # drag move
        if self.being_dragged and mouse_position != self.mouse_last_position:
            delta = mouse_position - self.mouse_last_position
            self.position += delta
            self.mouse_last_position = mouse_position
            event = DraggableMoved(self.moved_tag)

        return event
