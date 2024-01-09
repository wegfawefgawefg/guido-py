import glm
from shigg.default_drawing import draw_button, draw_slider, draw_draggable
from shigg.elements import Button, Slider, Draggable


class Gui:
    def __init__(self) -> None:
        self.elements = []
        self.draw_kit = None

    def add_element(self, element):
        """Add an element to the gui."""
        self.elements.append(element)

    def step(
        self,
        mouse_position: glm.vec2,
        mouse_pressed: bool,
        click=False,
    ):
        """Step the gui, and all elements within it.
        Mouse position should be normalized to the resolution of the gui.
        [0.0, 1.0] if its inside the gui, and [-inf, inf] if its outside.
        """
        for element in self.elements:
            if event := element.step(mouse_position, mouse_pressed):
                self.events.append(event)

    def get_events(self):
        """Get all events that occured since the last call to step.
        Calling this function will clear the event list."""
        events = self.events
        self.events = []
        return events

    def consume_events(self, events):
        """Consume a list of events, and pass each event to all child Elements.
        This is useful for self referential behaviour,
            such as defining a composite Element which responds to events from other elements.
        Generally you won't need this, and can just respond to the events as they come from get_events.
        """
        for element in self.elements:
            if element.consume_events:
                element.consume_events(events)

    def set_draw_kit(self, draw_kit):
        """Set the draw kit for all elements in the gui.
        The draw kit is a dictionary mapping element types to draw functions.
        """
        self.draw_kit = draw_kit

    def propogate_draw_kit(self):
        """This is for if you have some compound element you want to set all the childrens draw kit at once.
        You shouldn't be calling this often, only at ui construction time."""
        for element in self.elements:
            element.set_draw_kit(self.draw_kit)

    def draw(self, surface, resolution):
        """Draw the gui to the given surface."""
        if self.draw_kit is None:
            raise RuntimeError(
                "Cannot draw gui, no draw kit has been set. "
                "Use set_draw_kit to add a draw kit."
            )
        for element in self.elements:
            self.draw_kit(element, surface, resolution)
