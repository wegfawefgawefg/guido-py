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

    cursor = glm.vec2(0.1, 0.1)

    # lets make a vertical column of labeled interactable elements
    slider_names = ["red", "green", "blue", "alpha", "width", "height", "x", "y", "z"]
    button_names = ["dog", "cat", "mouse", "bird", "fish", "lizard", "snake", "frog"]
    # resolutions
    list_selector_options = [
        "320x240",
        "640x480",
        "1280x720",
        "1920x1080",
        "3840x2160",
        "2560x1440",
        "2560x1600",
    ]

    cursor = glm.vec2(0.1, 0.01)
    row_height = 0.05
    label_width = 0.2
    element_width = 0.5
    label_element_gap = 0.02

    scroll_bar_width = 0.05

    rows = []
    num_rows = 50
    element_types = [Button, Slider, LeftRightSelector]
    # settings label at the top
    settings_title = Label(
        copy.deepcopy(cursor),
        glm.vec2(
            label_width
            + element_width
            + label_element_gap
            + label_element_gap
            + scroll_bar_width,
            row_height,
        ),
        color=(50, 20, 20),
        text="Settings",
        text_color=(255, 255, 255),
        # no_background=True,
    )

    cursor.y += row_height * 1.1

    first_row_height = copy.deepcopy(cursor.y)

    section_num = 1
    for i in range(num_rows):
        new_section_chance = 0.15
        new_section_roll = random.random()
        if i == 0:
            new_section_roll = 0.0
        if new_section_roll < new_section_chance:
            cursor.y += row_height * 1.1
            # add a new section label
            section_label = Label(
                copy.deepcopy(cursor),
                glm.vec2(
                    label_width + element_width + label_element_gap,
                    row_height,
                ),
                color=(50, 20, 20),
                text=f"Section {section_num}",
                text_color=(255, 255, 255),
                # no_background=True,
            )
            section_num += 1
            rows.append([section_label])
            cursor.y += row_height * 1.1
            continue

        row = []
        # random element
        element_type = random.choice(element_types)
        if element_type == Button:
            label_text = f"{button_names[random.randint(0, len(button_names) - 1)]}"
            row.append(
                Label(
                    copy.deepcopy(cursor),
                    glm.vec2(label_width, row_height),
                    color=(20, 20, 20),
                    text=label_text,
                    text_color=(255, 255, 255),
                    # no_background=True,
                )
            )
            row.append(
                Button(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    color=(200, 200, 200),
                    label=f"{button_names[random.randint(0, len(button_names) - 1)]}",
                )
            )
        elif element_type == Slider:
            label_text = f"{slider_names[random.randint(0, len(slider_names) - 1)]}"
            row.append(
                Label(
                    copy.deepcopy(cursor),
                    glm.vec2(label_width, row_height),
                    color=(20, 20, 20),
                    text=label_text,
                    text_color=(255, 255, 255),
                    # no_background=True,
                )
            )
            row.append(
                Slider(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    color=(200, 200, 200),
                    thumb_width=0.02,
                    minimum=0,
                    maximum=1,
                    step_size=0.01,
                    default_value=random.random(),
                    label=label_text,
                )
            )
        elif element_type == LeftRightSelector:
            label_text = f"{slider_names[random.randint(0, len(slider_names) - 1)]}"
            row.append(
                Label(
                    copy.deepcopy(cursor),
                    glm.vec2(label_width, row_height),
                    color=(20, 20, 20),
                    text=label_text,
                    text_color=(255, 255, 255),
                    # no_background=True,
                )
            )
            row.append(
                LeftRightSelector(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    0.02,
                    color=(200, 200, 200),
                    options=list_selector_options,
                    starting_option=list_selector_options[
                        random.randint(0, len(list_selector_options) - 1)
                    ],
                )
            )

        rows.append(row)

        cursor.y += row_height * 1.1

    #  make sure row elements dont draw if they are above the first row position
    def cull():
        for row in rows:
            for element in row:
                if element.position.y >= first_row_height and element.position.y <= 0.9:
                    element.hidden = False
                else:
                    element.hidden = True

    for row in rows:
        for element in row:
            gui.add_element(element)

    # add a scroll bar at the right side
    thumb_height = 0.05
    scroll_bar_position = glm.vec2(
        settings_title.position.x + settings_title.scale.x - scroll_bar_width,
        settings_title.position.y
        + settings_title.scale.y
        + row_height * 0.1
        + thumb_height / 2.0,
    )
    scroll_bar_scale = glm.vec2(scroll_bar_width, 0.9 - thumb_height / 2.0)

    # find max y position element
    max_element_position = 0.0
    for element in gui.elements:
        if element.position.y > max_element_position:
            max_element_position = element.position.y

    scroll_bar_max = max_element_position
    scroll_bar = VerticalSlider(
        scroll_bar_position,
        scroll_bar_scale,
        color=(200, 200, 200),
        thumb_height=0.05,
        minimum=0.0,
        maximum=max_element_position,
        snap_sensetivity_fraction=0.00,
        step_size=row_height * 1.1,
        default_value=0,
        label="scroll",
        moved_tag=CustomEvent.MENU_SCROLL,
    )
    gui.add_element(scroll_bar)

    elements = []
    for row in rows:
        for element in row:
            elements.append(element)
    original_element_positions = []
    for element in elements:
        original_element_positions.append(copy.deepcopy(element.position))

    # shift all elements position up when scroll bar is moved
    def scroll_bar_event_handler(event):
        if event.tag == CustomEvent.MENU_SCROLL:
            for i, element in enumerate(elements):
                original_pos = original_element_positions[i]
                element.position = glm.vec2(
                    original_pos.x, original_pos.y - event.value
                )

    gui.add_element(settings_title)

    return gui, scroll_bar_event_handler, cull, scroll_bar


################################ MAIN ################################


def main():
    # hide mouse
    pygame.mouse.set_visible(False)

    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    pygame.display.set_caption("Shigg Builder")
    render_surface = pygame.Surface(render_resolution.to_tuple())

    gui, scroll_bar_event_handler, cull, scroll_bar = define_gui(assets)

    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

            # if the mouse scroll wheel is moved, scroll the scroll bar
            scroll_event = None
            if event.type == pygame.MOUSEWHEEL:
                # determine if up or down
                if event.y < 0:
                    scroll_event = scroll_bar.scroll_up_one_step()
                elif event.y > 0:
                    scroll_event = scroll_bar.scroll_down_one_step()

        # update gui
        mouse_pressed = pygame.mouse.get_pressed()[0]

        nmp = normalized_mouse_pos()
        # print(f"{nmp}, ui: {ui_mp}, preview: {preview_mp}")

        gui.step(nmp, mouse_pressed)
        if scroll_event:
            gui.events.append(scroll_event)
        for event in gui.get_events():
            print(f"event: {event}")
            print(f"event.tag: {event.tag}")
            scroll_bar_event_handler(event)

        ################################ RENDERING ################################
        # clear surfaces
        render_surface.fill((60, 60, 60))

        # draw gui
        cull()
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
