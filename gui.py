from enum import Enum
import math

import pygame
import glm
from drawing import draw_button, draw_slider


################################ Event Base ################################
class DataEnum(Enum):
    """Like an enum, that can hold data. Your event enum should inherit this."""

    def __call__(self, *args, **kwargs):
        instance = self.value(*args, **kwargs)
        instance._enum_name = self.name  # Store the enum's name in the instance

        # Override the instance's __repr__ to provide a custom string representation
        def instance_repr(self):
            attrs = ", ".join(
                f"{k}: {v}" for k, v in self.__dict__.items() if k != "_enum_name"
            )
            return f"{self._enum_name}({attrs})"

        instance.__class__.__repr__ = instance_repr

        return instance

    def __repr__(self) -> str:
        return f"{self.name}"


class GuiEvents(DataEnum):
    """The enum that holds your events. Inherit this."""

    pass


################################ UI ELEMENTS ################################


class Button:
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
        event=None,
    ) -> None:
        self.position = position
        self.scale = scale
        self.color = color
        self.text = text
        self.texture = texture
        self.label = label
        self.label_color = label_color
        self.image = image
        self.event = event

        self.hovered = False
        self.pressed = False

    def step(self, mouse_position, mouse_pressed, resolution):
        event = None
        absolute_position = resolution * self.position
        absolute_dimensions = resolution * self.scale

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
                if self.event:
                    event = self.event
            self.pressed = True
        else:
            self.pressed = False

        return event


class Slider:
    def __init__(
        self,
        position,
        scale,
        thumb_width,
        minimum,
        maximum,
        step_size,
        default_value,
        snap_sensetivity_fraction=0.05,
        color=(200, 200, 200),
        event=None,
    ) -> None:
        self.position = position
        self.scale = scale
        self.color = color
        self.thumb_width = thumb_width

        self.minimum = minimum
        self.maximum = maximum
        self.step_size = step_size
        self.snap_sensetivity_fraction = snap_sensetivity_fraction

        self.value = default_value

        self.color = color
        self.event = event

        self.hovered = False
        self.was_pressed = False

    def step(self, mouse_position, mouse_pressed, resolution):
        event = None

        if self.was_pressed and not mouse_pressed:
            if self.event:
                event = self.event(value=self.value)
            self.was_pressed = False

        absolute_tl = resolution * self.position
        absolute_dimensions = resolution * self.scale
        absolute_br = absolute_tl + absolute_dimensions

        if (
            mouse_position.x > absolute_tl.x
            and mouse_position.x < absolute_br.x
            and mouse_position.y > absolute_tl.y
            and mouse_position.y < absolute_br.y
        ):
            self.hovered = True
            if mouse_pressed:
                total = absolute_br.x - absolute_tl.x
                local_p = mouse_position.x - absolute_tl.x
                fraction = local_p / total
                self.value = self.minimum + fraction * (self.maximum - self.minimum)

                # if value is within 5% of the minimum or maximum, snap to it
                if self.snap_sensetivity_fraction > 0.0:
                    if self.value > self.maximum * (
                        1.0 - self.snap_sensetivity_fraction
                    ):
                        self.value = self.maximum
                    if self.value < (
                        (self.maximum - self.minimum) * self.snap_sensetivity_fraction
                    ):
                        self.value = self.minimum

                # round to nearest 100th, needs to work for negative and 0
                self.value = round(self.value, 2)

                self.was_pressed = True
        else:
            self.hovered = False

        return event


################################ GUI ################################


class Gui:
    def __init__(self) -> None:
        self.events = []
        self.buttons = []
        self.sliders = []

    def add_button(self, button: Button):
        self.buttons.append(button)

    def add_slider(self, slider: Slider):
        self.sliders.append(slider)

    def step(
        self,
        mouse_position: glm.vec2,
        mouse_pressed: bool,
        resolution: glm.vec2,
        click=False,
    ):
        for button in self.buttons:
            if event := button.step(mouse_position, mouse_pressed, resolution):
                self.events.append(event)

        for slider in self.sliders:
            if event := slider.step(mouse_position, mouse_pressed, resolution):
                self.events.append(event)

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events.clear()

    def draw(self, surface, resolution):
        for button in self.buttons:
            draw_button(surface, button, resolution)

        for slider in self.sliders:
            draw_slider(surface, slider, resolution)
