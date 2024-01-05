import math
import pygame
import glm

from enum import Enum

from gui import Gui, Button, Slider, GuiEvents

pygame.init()

render_resolution = glm.vec2(240, 160)
window_size = render_resolution * 4

################################ UTILS ################################


def mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / window_size * render_resolution


################################ EVENTS ################################
class SimpleNotification:
    pass


class NumberPad:
    def __init__(self, num):
        self.num = num


class Settings:
    pass


class OpenFoodSelector:
    pass


class FoodOption:
    class Food(Enum):
        POTATO = 0
        HOT_CHIP = 1
        ICE_CREAM = 2
        STEAK = 3

    def __init__(self, selection: Food):
        self.selection = selection


class SliderReleased:
    def __init__(self, value):
        self.value = value


class DemoGuiEvents(GuiEvents):
    SIMPLE_NOTIFICATION = SimpleNotification
    NUMBER_PAD = NumberPad
    SETTINGS = Settings
    OPEN_FOOD_SELECTOR = OpenFoodSelector
    FOOD_OPTION = FoodOption
    SLIDER_RELEASED = SliderReleased


################################ DEFINE GUI ################################
def define_gui(assets):
    gui = Gui()

    # add settings button
    gui.add_button(
        Button(
            glm.vec2(0.1, 0.1),
            glm.vec2(0.1, 0.1),
            color=(200, 200, 200),
            event=DemoGuiEvents.SETTINGS(),
            image=assets.gear,
        )
    )

    # make a number pad
    grid_position = glm.vec2(0.6, 0.1)
    button_count = glm.vec2(3, 3)
    button_scale = glm.vec2(0.1, 0.1)
    nums = [7, 8, 9, 4, 5, 6, 1, 2, 3]

    coords = [
        (ix, iy)
        for ix in range(int(button_count.x))
        for iy in range(int(button_count.y))
    ]

    for i, (ix, iy) in enumerate(coords):
        gui.add_button(
            Button(
                grid_position
                + glm.vec2(ix, iy) * (button_scale + glm.vec2(0.01, 0.01)),
                button_scale,
                color=(200, 200, 200),
                label_color=(0, 0, 0),
                label=str(nums[i]),
                event=DemoGuiEvents.NUMBER_PAD(nums[i]),
            )
        )

    # make a slider
    gui.add_slider(
        Slider(
            glm.vec2(0.1, 0.6),
            glm.vec2(0.3, 0.1),
            0.05,
            0,
            100,
            1,
            50,
            color=(200, 200, 200),
            event=DemoGuiEvents.SLIDER_RELEASED,
        )
    )

    return gui


################################ MAIN ################################


def draw(surface):
    pygame.draw.circle(surface, (0, 255, 0), mouse_pos(), 4)


def main():
    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    render_surface = pygame.Surface(render_resolution.to_tuple())

    class Assets:
        gear = pygame.image.load("assets/gear.png")
        potato = pygame.image.load("assets/potato.png")
        ice_cream = pygame.image.load("assets/ice-cream.png")
        chips = pygame.image.load("assets/chips.png")
        steak = pygame.image.load("assets/meat.png")

    gui = define_gui(Assets)

    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        # update gui
        mouse_pressed = pygame.mouse.get_pressed()[0]
        gui.step(mouse_pos(), mouse_pressed, render_resolution)
        for event in gui.get_events():
            print(event)
        gui.clear_events()

        # drawing
        render_surface.fill((60, 60, 60))
        gui.draw(render_surface, render_resolution)
        draw(render_surface)

        # blit to window
        stretched_surface = pygame.transform.scale(render_surface, window_size)
        window.blit(stretched_surface, (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
