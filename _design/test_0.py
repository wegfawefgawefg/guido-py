import copy
from enum import Enum, auto
import math

import pygame
import glm
from small_ass_cache import AssetCache, loader

from shigg import Gui, Button, Slider, Draggable
from shigg import transform_mouse_to_normalized_subsurface_coords


pygame.init()

window_size = glm.vec2(1200, 800)
render_resolution = window_size / 1.0

################################ UTILS ################################


def normalized_mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / window_size


################################ ASSETS ################################


@loader(pygame.image.load, path="assets/")
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


################################ DEFINE GUI ################################
def drag_button(gui, assets, pos):
    cursor = pos

    ss = 0.03
    s = glm.vec2(ss, ss)
    c = (50, 200, 50)

    # add new draggable
    tl = Draggable(
        copy.deepcopy(cursor),
        s,
        c,
        moved_tag=CustomEvent.TL_MOVED,
    )
    gui.add_draggable(tl)
    cursor += glm.vec2(0.1, 0.1)

    # add new draggable
    br = Draggable(
        copy.deepcopy(cursor),
        s,
        c,
        moved_tag=CustomEvent.BR_MOVED,
    )
    gui.add_draggable(br)

    # add a button that is at tl, but size br - tl
    button = Button(
        copy.deepcopy(tl.position + tl.scale),
        br.position - (tl.position + tl.scale),
        color=(200, 200, 200),
        label="button",
    )
    gui.add_button(button)

    def event_handler(event):
        if event.tag == CustomEvent.TL_MOVED:
            # move br also
            br.position = tl.position + tl.scale + button.scale

        if event.tag == CustomEvent.TL_MOVED or event.tag == CustomEvent.BR_MOVED:
            button.position = tl.position + tl.scale
            button.scale = br.position - (tl.position + tl.scale)

            # make sure br doesnt go to the left of the bottom right of tl
            if br.position.x < tl.position.x + tl.scale.x:
                br.position.x = tl.position.x + tl.scale.x
            if br.position.y < tl.position.y + tl.scale.y:
                br.position.y = tl.position.y + tl.scale.y

    return event_handler


def define_gui(assets):
    gui = Gui()

    cursor = glm.vec2(0.1, 0.1)

    db_event_handler = drag_button(gui, assets, copy.deepcopy(cursor))

    cursor.y += 0.1 * 1.1

    db2_event_handler = drag_button(gui, assets, copy.deepcopy(cursor))

    return gui, db_event_handler, db2_event_handler


################################ MAIN ################################


def main():
    # hide mouse
    pygame.mouse.set_visible(False)

    # init
    window = pygame.display.set_mode(window_size.to_tuple())
    pygame.display.set_caption("Shigg Builder")
    render_surface = pygame.Surface(render_resolution.to_tuple())

    gui, db_event_handler, db2_event_handler = define_gui(assets)

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

            db_event_handler(event)
            db2_event_handler(event)

        ################################ RENDERING ################################
        # clear surfaces
        render_surface.fill((60, 60, 60))

        # draw gui
        gui.draw(render_surface, render_resolution)

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
