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
        label=None,
        moved_tag=None,
        released_tag=None,
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
        self.label = label

        self.moved_tag = moved_tag
        self.released_tag = released_tag

        self.hovered = False
        self.was_pressed = False

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        if self.was_pressed and not mouse_pressed:
            event = SliderReleased(self.released_tag, self.value)
            self.was_pressed = False

        tl = self.position
        br = tl + self.scale

        if (
            mouse_position.x > tl.x
            and mouse_position.x < br.x
            and mouse_position.y > tl.y
            and mouse_position.y < br.y
        ):
            self.hovered = True
            if mouse_pressed:
                old_value = self.value

                total = br.x - tl.x
                local_p = mouse_position.x - tl.x
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

                # round to nearest step size
                self.value = round(self.value / self.step_size) * self.step_size

                # only emit event if value changed
                if self.value != old_value:
                    event = SliderMoved(self.moved_tag, self.value)

                self.was_pressed = True
        else:
            self.hovered = False

        return event
