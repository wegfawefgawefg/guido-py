from enum import Enum, auto
import math

import pygame
import glm
from small_ass_cache import AssetCache, loader

# if you want to import from the local version of shigg
import sys

sys.path.append("../")
from shigg import Gui, Button, Slider
from shigg import transform_mouse_to_normalized_subsurface_coords


pygame.init()

render_resolution = glm.vec2(1200, 800) / 4.0
window_size = render_resolution * 4.0

################################ UTILS ################################


def normalized_mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / window_size


################################ ASSETS ################################


@loader(pygame.image.load, path="../assets/")
class Icons(Enum):
    gear = "gear.png"
    potato = "potato.png"
    ice_cream = "ice-cream.png"
    chips = "chips.png"
    steak = "meat.png"
    food_selector = "fast-food.png"


assets = AssetCache()

################################ EVENTS ################################


class TopLevel(Enum):
    Settings = auto()
    SetVolume = auto()


class NumPad(Enum):
    One = auto()
    Two = auto()
    Three = auto()
    Four = auto()
    Five = auto()
    Six = auto()
    Seven = auto()
    Eight = auto()
    Nine = auto()


class FoodSelector(Enum):
    OpenFoodSelector = auto()
    SelectionPotato = auto()
    SelectionHotChip = auto()
    SelectionIceCream = auto()
    SelectionSteak = auto()


################################ DEFINE GUI ################################
def define_gui(assets):
    gui = Gui()

    # add settings button
    gui.add_element(
        Button(
            glm.vec2(0.1, 0.1),
            glm.vec2(0.1, 0.1),
            color=(200, 200, 200),
            image=assets.get(Icons.gear),
            released_tag=TopLevel.Settings,
        )
    )

    # number pad
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
        gui.add_element(
            Button(
                grid_position
                + glm.vec2(ix, iy) * (button_scale + glm.vec2(0.01, 0.01)),
                button_scale,
                color=(200, 200, 200),
                label_color=(0, 0, 0),
                label=str(nums[i]),
                released_tag=[
                    NumPad.Seven,
                    NumPad.Eight,
                    NumPad.Nine,
                    NumPad.Four,
                    NumPad.Five,
                    NumPad.Six,
                    NumPad.One,
                    NumPad.Two,
                    NumPad.Three,
                ][i],
            )
        )

    # make a slider
    gui.add_element(
        Slider(
            glm.vec2(0.1, 0.25),
            glm.vec2(0.3, 0.1),
            0.05,
            0,
            100,
            1,
            50,
            color=(200, 200, 200),
            released_tag=TopLevel.SetVolume,
        )
    )

    return gui


def food_gui_top_level(gui, assets):
    gui.elements = []
    # make a select food option button
    gui.add_element(
        Button(
            glm.vec2(0.6, 0.6),
            glm.vec2(0.1, 0.1),
            color=(200, 200, 200),
            image=assets.get(Icons.food_selector),
            released_tag=FoodSelector.OpenFoodSelector,
        )
    )


def food_selector(gui, assets):
    # row of buttons,
    # each button is a food option
    # potato, hot chip, ice cream, steak

    gui.elements = []
    buttons_position = glm.vec2(0.5, 0.7)
    buttons_scale = glm.vec2(0.1, 0.1)
    buttons_spacing = glm.vec2(0.01, 0.01)

    event_tags = [
        FoodSelector.SelectionPotato,
        FoodSelector.SelectionHotChip,
        FoodSelector.SelectionIceCream,
        FoodSelector.SelectionSteak,
    ]

    for i, event_tag in enumerate(event_tags):
        icon = {
            FoodSelector.SelectionPotato: Icons.potato,
            FoodSelector.SelectionHotChip: Icons.chips,
            FoodSelector.SelectionIceCream: Icons.ice_cream,
            FoodSelector.SelectionSteak: Icons.steak,
        }[event_tag]

        gui.add_element(
            Button(
                buttons_position + glm.vec2(i, 0) * (buttons_scale + buttons_spacing),
                buttons_scale,
                color=(200, 200, 200),
                released_tag=event_tag,
                image=assets.get(icon),
            )
        )


################################ MAIN ################################


def main():
    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    pygame.display.set_caption("GUI Demo")
    render_surface = pygame.Surface(render_resolution.to_tuple())

    gui = define_gui(assets)
    food_gui = Gui()
    food_gui_top_level(food_gui, assets)

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
        nmp = normalized_mouse_pos()
        gui.step(nmp, mouse_pressed, render_resolution)
        for event in gui.get_events():
            print(f"event: {event}")
            print(f"event.tag: {event.tag}")

        # update food gui
        food_gui.step(nmp, mouse_pressed, render_resolution)
        for event in food_gui.get_events():
            print(f"event: {event}")
            print(f"event.tag: {event.tag}")
            if event.tag == FoodSelector.OpenFoodSelector:
                food_selector(food_gui, assets)
            elif isinstance(event.tag, FoodSelector):
                food_gui_top_level(food_gui, assets)

        # drawing
        render_surface.fill((60, 60, 60))
        gui.draw(render_surface, render_resolution)
        food_gui.draw(render_surface, render_resolution)

        # blit to window
        stretched_surface = pygame.transform.scale(render_surface, window_size)
        window.blit(stretched_surface, (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
