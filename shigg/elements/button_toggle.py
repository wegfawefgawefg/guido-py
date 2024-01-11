from enum import Enum, auto

import glm

from ._element import Element
from ._element_event import ElementEvent
from .button import Button


class ToggleChanged(ElementEvent):
    def __init__(self, tag, toggled_option) -> None:
        super().__init__(tag)
        self.toggled_option = toggled_option


class InternalLeftRightEvents(Enum):
    LeftToggled = auto()
    RightToggled = auto()


class ButtonToggle(Element):
    def __init__(
        self,
        position,
        scale,
        left_button_label,
        right_button_label,
        left_option,
        right_option,
        starting_option,
        color=(200, 200, 200),
        toggle_changed_tag=None,
    ) -> None:
        super().__init__()
        self._scale = scale
        self.color = color

        self.left_button_label = left_button_label
        self.right_button_label = right_button_label

        self.left_option = left_option
        self.right_option = right_option

        # make sure starting option is one of the options
        if starting_option not in [self.left_option, self.right_option]:
            raise ValueError(
                f"starting_option {starting_option} not found in given options: {self.left_option}, {self.right_option}"
            )
        self.toggled_option = starting_option
        self.toggle_changed_tag = toggle_changed_tag

        self.left_button = Button(
            position,
            glm.vec2(self.scale.x / 2, self.scale.y),
            color,
            label=self.left_button_label,
            released_tag=InternalLeftRightEvents.LeftToggled,
        )

        self.right_button = Button(
            glm.vec2(position.x + self.scale.x / 2, position.y),
            glm.vec2(self.scale.x / 2, self.scale.y),
            color,
            label=self.right_button_label,
            released_tag=InternalLeftRightEvents.RightToggled,
        )

    @property
    def position(self):
        return self.left_button.position

    @position.setter
    def position(self, value):
        self.left_button.position = value
        self.right_button.position = glm.vec2(value.x + self.scale.x / 2, value.y)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        half_width = value.x / 2
        self.left_button.scale = glm.vec2(half_width, value.y)
        self.right_button.scale = glm.vec2(half_width, value.y)
        self.right_button.position = glm.vec2(
            self.position.x + half_width, self.position.y
        )

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        left_event = self.left_button.step(mouse_position, mouse_pressed)
        right_event = self.right_button.step(mouse_position, mouse_pressed)

        if left_event and left_event.tag == InternalLeftRightEvents.LeftToggled:
            self.toggled_option = self.left_option
            event = ToggleChanged(self.toggle_changed_tag, self.toggled_option)

        elif right_event and right_event.tag == InternalLeftRightEvents.RightToggled:
            self.toggled_option = self.right_option
            event = ToggleChanged(self.toggle_changed_tag, self.toggled_option)

        return event
