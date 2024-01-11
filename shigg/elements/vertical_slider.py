from ._element_event import ElementEvent
from ._element import Element


class VerticalSliderMoved(ElementEvent):
    def __init__(self, tag, value) -> None:
        super().__init__(tag)
        self.value = value


class VerticalSliderReleased(ElementEvent):
    def __init__(self, tag, value) -> None:
        super().__init__(tag)
        self.value = value


class VerticalSlider(Element):
    def __init__(
        self,
        position,
        scale,
        thumb_height,
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
        super().__init__()
        self.position = position
        self.scale = scale
        self.color = color
        self.thumb_height = thumb_height

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

    def scroll_down_one_step(self):
        self.value -= self.step_size
        if self.value < self.minimum:
            self.value = self.minimum

        return VerticalSliderMoved(self.moved_tag, self.value)

    def scroll_up_one_step(self):
        self.value += self.step_size
        if self.value > self.maximum:
            self.value = self.maximum

        return VerticalSliderMoved(self.moved_tag, self.value)

    def step(self, mouse_position, mouse_pressed) -> ElementEvent:
        event = None

        if self.was_pressed and not mouse_pressed:
            event = VerticalSliderReleased(self.released_tag, self.value)
            self.was_pressed = False

        tl = self.position
        br = tl + self.scale

        if (
            mouse_position.x > tl.x - self.thumb_height / 2
            and mouse_position.x < br.x + self.thumb_height / 2
            and mouse_position.y > tl.y
            and mouse_position.y < br.y
        ):
            self.hovered = True
            if mouse_pressed:
                old_value = self.value

                total = br.y - tl.y
                local_p = mouse_position.y - tl.y
                fraction = local_p / total
                self.value = self.minimum + fraction * (self.maximum - self.minimum)

                if self.snap_sensetivity_fraction > 0.0:
                    if self.value > self.maximum * (
                        1.0 - self.snap_sensetivity_fraction
                    ):
                        self.value = self.maximum
                    if self.value < (
                        (self.maximum - self.minimum) * self.snap_sensetivity_fraction
                    ):
                        self.value = self.minimum

                self.value = round(self.value, 2)
                self.value = round(self.value / self.step_size) * self.step_size

                if self.value != old_value:
                    event = VerticalSliderMoved(self.moved_tag, self.value)

                self.was_pressed = True
        else:
            self.hovered = False

        return event
