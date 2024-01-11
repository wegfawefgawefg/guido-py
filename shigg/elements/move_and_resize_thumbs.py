from enum import Enum, auto

from ._element_event import ElementEvent
from ._element import Element

from .draggable import Draggable


class InternalMoveAndResizeThumbsEvent(Enum):
    MoveThumbMoved = auto()
    ResizeThumbMoved = auto()


class MoveAndResizeThumbs(Element):
    """Adjusts the target element position and size based on thumbs.
    Does not return any events."""

    def __init__(
        self,
        scale,
        target_element,
        color=(200, 200, 200),
        texture=None,
        image=None,
    ) -> None:
        super().__init__()
        self.target_element = target_element

        self.color = color
        self.texture = texture
        self.image = image

        self.move_thumb = Draggable(
            self.target_element.position - scale,
            scale,
            color,
            moved_tag=InternalMoveAndResizeThumbsEvent.MoveThumbMoved,
        )

        self.resize_thumb = Draggable(
            self.target_element.position + self.target_element.scale,
            scale,
            color,
            moved_tag=InternalMoveAndResizeThumbsEvent.ResizeThumbMoved,
        )

    @property
    def position(self):
        return self.move_thumb.position

    @position.setter
    def position(self, value):
        self.move_thumb.position = value
        self.target_element.position = value + self.move_thumb.scale
        self.resize_thumb.position = (
            value + self.move_thumb.scale + self.target_element.scale
        )

    @property
    def scale(self):
        return self.move_thumb.scale

    @scale.setter
    def scale(self, value):
        self.move_thumb.scale = value
        self.resize_thumb.scale = value

        self.target_element.position = self.move_thumb.position + self.move_thumb.scale
        self.resize_thumb.position = (
            self.move_thumb.position + self.move_thumb.scale + self.target_element.scale
        )

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        move_event = self.move_thumb.step(mouse_position, mouse_pressed)
        resize_event = self.resize_thumb.step(mouse_position, mouse_pressed)

        if move_event:
            if move_event.tag == InternalMoveAndResizeThumbsEvent.MoveThumbMoved:
                self.target_element.position = (
                    self.move_thumb.position + self.move_thumb.scale
                )
                self.resize_thumb.position = (
                    self.move_thumb.position
                    + self.move_thumb.scale
                    + self.target_element.scale
                )

        if resize_event:
            if resize_event.tag == InternalMoveAndResizeThumbsEvent.ResizeThumbMoved:
                self.target_element.scale = (
                    self.move_thumb.position + self.move_thumb.scale
                )
                self.target_element.scale = self.resize_thumb.position - (
                    self.move_thumb.position + self.move_thumb.scale
                )

        self.move_thumb.position = self.target_element.position - self.move_thumb.scale
        self.resize_thumb.position = (
            self.target_element.position + self.target_element.scale
        )

        # make sure resize thumb doesnt go to the left of the bottom right of move thumb
        if (
            self.resize_thumb.position.x
            < self.move_thumb.position.x + self.move_thumb.scale.x
        ):
            self.resize_thumb.position.x = (
                self.move_thumb.position.x + self.move_thumb.scale.x
            )
        if (
            self.resize_thumb.position.y
            < self.move_thumb.position.y + self.move_thumb.scale.y
        ):
            self.resize_thumb.position.y = (
                self.move_thumb.position.y + self.move_thumb.scale.y
            )
