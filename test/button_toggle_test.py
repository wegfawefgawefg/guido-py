import copy
from enum import Enum, auto
import math
import random

import pygame
import glm
from small_ass_cache import AssetCache, loader

# if you want to import from the local version of shigg
import sys


sys.path.append("../")
from shigg import Element, ElementEvent
from shigg import (
    Gui,
    Button,
    Slider,
    Draggable,
    Label,
    LeftRightSelector,
    VerticalSlider,
    ButtonToggle,
)
from shigg import transform_mouse_to_normalized_subsurface_coords


pygame.init()

window_size = glm.vec2(1200, 800)
render_resolution = window_size / 1.0

################################ UTILS ################################


def normalized_mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / window_size


################################ ASSETS ################################


@loader(pygame.image.load, path="../assets/")
class Icons(Enum):
    cursor = "mouse.png"
    gear = "gear.png"
    potato = "potato.png"
    ice_cream = "ice-cream.png"
    chips = "chips.png"
    steak = "meat.png"
    food_selector = "fast-food.png"


assets = AssetCache()

################################ EVENTS ################################


class CustomEvent(Enum):
    TL_MOVED = auto()
    BR_MOVED = auto()
    MENU_SCROLL = auto()


################################ DEFINE GUI ################################


def define_gui(assets):
    gui = Gui()

    button_toggle = ButtonToggle(
        glm.vec2(0.5, 0.5),
        glm.vec2(0.2, 0.1),
        "left",
        "right",
        "left",
        "right",
        "left",
    )

    gui.add_element(button_toggle)

    return gui


################################ MAIN ################################


def main():
    # hide mouse
    pygame.mouse.set_visible(False)

    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    pygame.display.set_caption("Shigg Builder")
    render_surface = pygame.Surface(render_resolution.to_tuple())

    gui = define_gui(assets)

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
        # print(f"{nmp}, ui: {ui_mp}, preview: {preview_mp}")

        gui.step(nmp, mouse_pressed)
        for event in gui.get_events():
            print(f"event: {event}")
            print(f"event.tag: {event.tag}")

        ################################ RENDERING ################################
        # clear surfaces
        render_surface.fill((60, 60, 60))

        # draw gui
        gui.draw(render_surface, render_resolution)

        # draw mouse
        render_surface.blit(
            assets.get(Icons.cursor), normalized_mouse_pos() * render_resolution
        )

        # blit to window
        stretched_surface = pygame.transform.scale(render_surface, window_size)
        window.blit(stretched_surface, (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
