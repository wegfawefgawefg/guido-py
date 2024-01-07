import glm
from shigg.default_drawing import draw_button, draw_slider
from shigg.elements import Button, Slider


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
        events = self.events
        self.events = []
        return events

    def clear_events(self):
        self.events.clear()

    def draw(self, surface, resolution):
        for button in self.buttons:
            draw_button(surface, button, resolution)

        for slider in self.sliders:
            draw_slider(surface, slider, resolution)
