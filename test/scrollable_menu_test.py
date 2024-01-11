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

    cursor = glm.vec2(0.1, 0.1)

    # lets make a vertical column of labeled interactable elements
    button_names = ["dog", "cat", "mouse", "bird", "fish", "lizard", "snake", "frog"]

    slider_variants = [
        ("Volume", (0, 100)),
        ("Brightness", (0, 100)),
        ("Contrast", (0, 100)),
        ("View Distance", (0, 100)),
        ("FOV", (0, 100)),
        ("Mouse Sensitivity", (0, 100)),
        ("Gamma", (0, 100)),
    ]

    left_right_selector_variants = [
        ("Resolution", ("320x240", "640x480", "1280x720", "1920x1080", "3840x2160")),
        ("Texture Quality", ("Low", "Medium", "High")),
        ("Audio Quality", ("Low", "Medium", "High")),
        ("Audio Device", ("Speakers", "Headphones")),
        ("Language", ("English", "Spanish", "French", "German")),
    ]
    button_toggle_variants = [
        ("Food", ("Potato", "Ice Cream")),
        ("Fullscreen", ("No", "Yes")),
        ("Invert Y", ("Normal", "Inverted")),
        ("VSync", ("No", "Yes")),
        ("Shadows", ("Off", "On")),
        ("Grass", ("Off", "On")),
        ("Anti-Aliasing", ("Off", "On")),
        ("Anisotropic Filtering", ("Off", "On")),
    ]

    cursor = glm.vec2(0.1, 0.01)
    row_height = 0.05
    label_width = 0.2
    element_width = 0.5
    label_element_gap = 0.02

    scroll_bar_width = 0.05

    rows = []
    num_rows = 50
    element_types = [Button, Slider, LeftRightSelector, ButtonToggle]
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
            variant = random.choice(slider_variants)
            label_text = variant[0]
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
            min_value = variant[1][0]
            max_value = variant[1][1]
            row.append(
                Slider(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    color=(200, 200, 200),
                    thumb_width=0.02,
                    minimum=min_value,
                    maximum=max_value,
                    step_size=(max_value - min_value) / 100.0,
                    default_value=random.random() * (max_value - min_value),
                    label=label_text,
                )
            )
        elif element_type == LeftRightSelector:
            variant = random.choice(left_right_selector_variants)
            label_text = variant[0]
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
            list_selector_options = variant[1]
            row.append(
                LeftRightSelector(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    0.05,
                    color=(200, 200, 200),
                    options=list_selector_options,
                    starting_option=random.choice(list_selector_options),
                )
            )
        elif element_type == ButtonToggle:
            variant = random.choice(button_toggle_variants)
            label_text = variant[0]
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
            left_option = variant[1][0]
            right_option = variant[1][1]
            row.append(
                ButtonToggle(
                    glm.vec2(cursor.x + label_width + label_element_gap, cursor.y),
                    glm.vec2(element_width, row_height),
                    left_option,
                    right_option,
                    left_option,
                    right_option,
                    random.choice((left_option, right_option)),
                    color=(200, 200, 200),
                )
            )

        rows.append(row)

        cursor.y += row_height * 1.1

    #  make sure row elements dont draw if they are above the first row position
    def cull():
        for row in rows:
            for element in row:
                if element.position.y >= first_row_height and element.position.y <= 0.8:
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
    scroll_bar_scale = glm.vec2(scroll_bar_width, 0.8 - thumb_height / 2.0)

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

    # lets get some back and apply buttons at the bottom

    back_and_apply_height = 0.85
    back_button = Button(
        glm.vec2(0.1, back_and_apply_height),
        glm.vec2(0.1, row_height),
        color=(200, 200, 200),
        label="Back",
    )
    apply_button = Button(
        glm.vec2(0.21, back_and_apply_height),
        glm.vec2(0.1, row_height),
        color=(200, 200, 200),
        label="Apply",
    )
    gui.add_element(back_button)
    gui.add_element(apply_button)

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
