from ._element_event import ElementEvent
from ._element import Element


class SliderMoved(ElementEvent):
    def __init__(self, tag, value) -> None:
        super().__init__(tag)
        self.value = value


class SliderReleased(ElementEvent):
    def __init__(self, tag, value) -> None:
        super().__init__(tag)
        self.value = value


class Slider(Element):
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
        tag=None,
    ) -> None:
        super().__init__(tag)

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

        self.hovered = False
        self.was_pressed = False

    def step(self, mouse_position, mouse_pressed, resolution):
        event = None

        if self.was_pressed and not mouse_pressed:
            event = SliderReleased(self.tag, self.value)
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
                old_value = self.value

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

                # only emit event if value changed
                if self.value != old_value:
                    event = SliderMoved(self.tag, self.value)

                self.was_pressed = True
        else:
            self.hovered = False

        return event
