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
                    event = self.event()
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
                event_constructor = self.event
                event = event_constructor(value=self.value)
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
