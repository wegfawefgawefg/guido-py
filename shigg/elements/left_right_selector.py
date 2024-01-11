from enum import Enum, auto

import glm

from ._element_event import ElementEvent
from ._element import Element
from .button import Button


class SelectionChanged(ElementEvent):
    def __init__(self, tag, selected_option, end_of_options_reached) -> None:
        super().__init__(tag)
        self.selected_option = selected_option
        self.end_of_options_reached = end_of_options_reached


class InternalLeftRightSelectorEvent(Enum):
    LeftReleased = auto()
    RightReleased = auto()


class LeftRightSelector(Element):
    def __init__(
        self,
        position,
        scale,
        button_width,
        options,
        starting_option,
        color=(200, 200, 200),
        selection_changed_tag=None,
    ) -> None:
        super().__init__()
        self._scale = scale
        self.color = color
        self.button_width = button_width

        self.options = options
        self.selected_option = starting_option

        # find the index of the starting option
        self.selected_option_index = None
        for i, option in enumerate(self.options):
            if option == self.selected_option:
                self.selected_option_index = i
                break
        if self.selected_option_index is None:
            raise ValueError(
                f"starting_option {starting_option} not found in options {options}"
            )

        self.color = color

        self.selection_changed_tag = selection_changed_tag

        self.left_button = Button(
            position,
            glm.vec2(self.button_width, self.scale.y),
            color,
            label="<",
            released_tag=InternalLeftRightSelectorEvent.LeftReleased,
        )

        self.right_button = Button(
            glm.vec2(position.x + self.scale.x - self.button_width, position.y),
            glm.vec2(self.button_width, self.scale.y),
            color,
            label=">",
            released_tag=InternalLeftRightSelectorEvent.RightReleased,
        )

    @property
    def position(self):
        return self.left_button.position

    @position.setter
    def position(self, value):
        self.left_button.position = value
        self.right_button.position = glm.vec2(
            value.x + self.scale.x - self.button_width, value.y
        )

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.left_button.scale = glm.vec2(self.button_width, value.y)
        self.right_button.scale = glm.vec2(self.button_width, value.y)
        # reposition the right button
        self.right_button.position = glm.vec2(
            self.position.x + self.scale.x - self.button_width, self.position.y
        )

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        left_event = self.left_button.step(mouse_position, mouse_pressed)
        right_event = self.right_button.step(mouse_position, mouse_pressed)

        if left_event:
            if left_event.tag == InternalLeftRightSelectorEvent.LeftReleased:
                if self.selected_option_index > 0:
                    self.selected_option_index -= 1
                    self.selected_option = self.options[self.selected_option_index]
                    event = SelectionChanged(
                        self.selection_changed_tag,
                        self.selected_option,
                        False,
                    )
        elif right_event:
            if right_event.tag == InternalLeftRightSelectorEvent.RightReleased:
                if self.selected_option_index < len(self.options) - 1:
                    self.selected_option_index += 1
                    self.selected_option = self.options[self.selected_option_index]
                    if self.selection_changed_tag:
                        event = SelectionChanged(
                            self.selection_changed_tag,
                            self.selected_option,
                            False,
                        )

        return event
