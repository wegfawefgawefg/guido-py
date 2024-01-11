import copy
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

window_size = glm.vec2(1200, 800)
render_resolution = window_size / 1.0
ui_ratio = 0.3
ui_resolution = glm.vec2(render_resolution.x * ui_ratio, render_resolution.y)
preview_resolution = glm.vec2(
    render_resolution.x * (1.0 - ui_ratio), render_resolution.y
)

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


class BuilderEvent(Enum):
    NewButton = auto()
    NewSlider = auto()
    SetX = auto()
    SetY = auto()
    SetWidth = auto()
    SetHeight = auto()

    SaveLayout = auto()

    SetColorR = auto()
    SetColorG = auto()
    SetColorB = auto()


################################ DEFINE GUI ################################
def define_builder_gui(assets):
    gui = Gui()

    cursor = glm.vec2(0.1, 0.1)

    # add new button button
    gui.add_element(
        Button(
            copy.deepcopy(cursor),
            glm.vec2(0.8, 0.1),
            color=(200, 200, 200),
            label="add button",
            released_tag=BuilderEvent.NewButton,
        )
    )
    cursor.y += 0.1 * 1.1

    # add new slider button
    gui.add_element(
        Button(
            copy.deepcopy(cursor),
            glm.vec2(0.8, 0.1),
            color=(200, 200, 200),
            label="add slider",
            released_tag=BuilderEvent.NewSlider,
        )
    )

    cursor.y += 0.1 * 1.1

    # add save button
    gui.add_element(
        Button(
            copy.deepcopy(cursor),
            glm.vec2(0.8, 0.1),
            color=(200, 200, 200),
            label="save layout",
            released_tag=BuilderEvent.SaveLayout,
        )
    )

    slider_height = 0.05
    slider_width = 0.8
    thumb_width_frac = 0.08
    color = (200, 200, 200)
    minval = 0.0
    maxval = 1.0
    step_size = 0.1
    default_value = 0.5

    cursor = glm.vec2(0.1, 0.5)
    # pos x
    x_pos_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        moved_tag=BuilderEvent.SetX,
    )
    gui.add_element(x_pos_slider)
    cursor.y += slider_height * 1.1

    # pos y
    y_pos_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        moved_tag=BuilderEvent.SetY,
    )
    gui.add_element(y_pos_slider)

    cursor.y += slider_height * 1.1

    # width
    width_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        label="x",
        moved_tag=BuilderEvent.SetWidth,
    )
    gui.add_element(width_slider)

    cursor.y += slider_height * 1.1

    # height
    height_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        label="y",
        moved_tag=BuilderEvent.SetHeight,
    )
    gui.add_element(height_slider)

    cursor.y += slider_height * 1.1
    cursor.y += slider_height * 1.1

    # color r
    red_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        label="r",
        moved_tag=BuilderEvent.SetColorR,
    )
    gui.add_element(red_slider)

    cursor.y += slider_height * 1.1

    # color g
    green_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        label="g",
        moved_tag=BuilderEvent.SetColorG,
    )
    gui.add_element(green_slider)

    cursor.y += slider_height * 1.1

    # color b
    blue_slider = Slider(
        copy.deepcopy(cursor),
        glm.vec2(slider_width, slider_height),
        thumb_width_frac,
        minval,
        maxval,
        step_size,
        default_value,
        color=color,
        label="b",
        moved_tag=BuilderEvent.SetColorB,
    )
    gui.add_element(blue_slider)

    # make a named tuple for the sliders, so we can easily access them
    from collections import namedtuple

    settings_sliders = namedtuple(
        "settings_sliders",
        [
            "x_pos_slider",
            "y_pos_slider",
            "width_slider",
            "height_slider",
            "red_slider",
            "green_slider",
            "blue_slider",
        ],
    )(
        x_pos_slider,
        y_pos_slider,
        width_slider,
        height_slider,
        red_slider,
        green_slider,
        blue_slider,
    )

    return gui, settings_sliders


################################ MAIN ################################


def main():
    # hide mouse
    pygame.mouse.set_visible(False)

    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    pygame.display.set_caption("Shigg Builder")
    render_surface = pygame.Surface(render_resolution.to_tuple())

    ui_surface = pygame.Surface(ui_resolution.to_tuple())
    preview_surface = pygame.Surface(preview_resolution.to_tuple())

    builder_gui, settings_sliders = define_builder_gui(assets)

    ui_position = glm.vec2(0.0, 0.0)
    preview_pos = glm.vec2(ui_resolution.x, 0.0)

    buttons = []
    current_element = None

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
        ui_mp = transform_mouse_to_normalized_subsurface_coords(
            nmp, render_resolution, ui_position, ui_resolution
        )
        preview_mp = transform_mouse_to_normalized_subsurface_coords(
            nmp, render_resolution, preview_pos, preview_resolution
        )
        # print(f"{nmp}, ui: {ui_mp}, preview: {preview_mp}")

        builder_gui.step(ui_mp, mouse_pressed)
        for event in builder_gui.get_events():
            print(f"event: {event}")
            print(f"event.tag: {event.tag}")
            if event.tag == BuilderEvent.NewButton:
                if current_element:
                    buttons.append(current_element)
                current_element = Button(
                    glm.vec2(0.0, 0.0),
                    glm.vec2(0.1, 0.1),
                    color=(200, 200, 200),
                    label="wow",
                )
            elif event.tag == BuilderEvent.NewSlider:
                if current_element:
                    buttons.append(current_element)
                current_element = Slider(
                    glm.vec2(0.0, 0.0),
                    glm.vec2(0.1, 0.1),
                    0.1,
                    0.0,
                    1.0,
                    0.1,
                    0.5,
                    color=(200, 200, 200),
                    label="wow",
                )
            elif event.tag == BuilderEvent.SetX:
                if current_element:
                    current_element.position.x = event.value
            elif event.tag == BuilderEvent.SetY:
                if current_element:
                    current_element.position.y = event.value
            elif event.tag == BuilderEvent.SetWidth:
                if current_element:
                    current_element.scale.x = event.value
            elif event.tag == BuilderEvent.SetHeight:
                if current_element:
                    current_element.scale.y = event.value
            elif event.tag == BuilderEvent.SetColorR:
                if current_element:
                    r = math.floor(event.value * 255)
                    color = (r, current_element.color[1], current_element.color[2])
                    current_element.color = color
            elif event.tag == BuilderEvent.SetColorG:
                if current_element:
                    g = math.floor(event.value * 255)
                    color = (current_element.color[0], g, current_element.color[2])
                    current_element.color = color
            elif event.tag == BuilderEvent.SetColorB:
                if current_element:
                    b = math.floor(event.value * 255)
                    color = (current_element.color[0], current_element.color[1], b)
                    current_element.color = color

        # set the sliders to the properties of the current button
        if current_element:
            settings_sliders.x_pos_slider.value = current_element.position.x
            settings_sliders.y_pos_slider.value = current_element.position.y
            settings_sliders.width_slider.value = current_element.scale.x
            settings_sliders.height_slider.value = current_element.scale.y
            settings_sliders.red_slider.value = current_element.color[0] / 255
            settings_sliders.green_slider.value = current_element.color[1] / 255
            settings_sliders.blue_slider.value = current_element.color[2] / 255

        temp_gui = Gui()
        if current_element:
            temp_gui.add_element(current_element)
        for button in buttons:
            temp_gui.add_element(button)
        temp_gui.step(preview_mp, mouse_pressed)

        ################################ RENDERING ################################
        # clear surfaces
        render_surface.fill((60, 60, 60))
        ui_surface.fill((70, 70, 70))
        preview_surface.fill((20, 20, 20))

        # draw builder ui
        builder_gui.draw(ui_surface, ui_resolution)
        render_surface.blit(ui_surface, (0, 0))

        # draw preview
        temp_gui.draw(preview_surface, preview_resolution)
        render_surface.blit(preview_surface, preview_pos)

        # draw mouse
        # pygame.draw.circle(
        #     render_surface, (0, 255, 0), normalized_mouse_pos() * render_resolution, 4
        # )
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
