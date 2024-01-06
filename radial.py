from __future__ import annotations
import pygame as pg
from pygame import Vector2 as vec2


class Game:
    def __init__(self, width: int, height: int):
        pg.init()
        self.window = pg.display.set_mode((width, height))
        self.win_size = vec2(width, height)
        self.clock = pg.time.Clock()
        self.running = False
        self.dt = 0.0
        self.menu = RadialMenu(
            vec2(1280, 720).elementwise() / 2.0,
            items=[i for i in range(6)],
            radius=128,
            item_size=64,
            start_open=True,
            speed=0.0001,
            callback=lambda item: print(f"{item=}"),
        )

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu.is_open():
                    self.menu.process_click_event()
                else:
                    self.menu.state = "opening"

    def update(self):
        self.dt = self.clock.tick(60) * 0.001
        fps = self.clock.get_fps()
        pg.display.set_caption(f"{fps:0.2f}")

        mpos = vec2(pg.mouse.get_pos())
        self.menu.update(self.dt)

    def draw(self):
        self.window.fill((30, 20, 20))

        self.menu.draw(self.window)

        pg.display.update()


class RadialMenu:
    def __init__(
        self,
        pos,
        radius=None,
        items=[],
        item_size=24,
        item_padding=0,
        speed=0.001,
        callback=None,
        start_open=False,
    ):
        self.pos = vec2(pos)
        self.radius = radius
        self.item_size = item_size
        self.item_padding = item_padding
        self.items = items
        self.surf = None
        self.center = vec2()
        self.speed = speed
        self.progress = 0
        self.state = "opening" if start_open else "closed"
        self.callback = callback

    def process_click_event(self):
        if self.selected is not None:
            if callable(self.callback):
                self.callback(self.selected)
            else:
                print(self.selected)
        self.state = "closing"

    def is_open(self):
        return not self.state == "closed"

    def set_pos(self, pos):
        self.pos = vec2(pos)
        self.state = "opening"

    def update(self, dt):
        if not self.speed:
            self._radius = self.radius
        if self.state == "closed":
            return
        length = len(self.items)
        mpos = vec2(pg.mouse.get_pos())
        mouse_pos = mpos - self.pos + self.center
        self.selected = None
        if length == 0:
            return
        elif length == 1:
            self.surf = pg.Surface(vec2(self.item_size + 8), pg.SRCALPHA)
            self.center = vec2(self.surf.get_size()) / 2
            color = (200, 200, 200, 100)
            line = 1
            if self.center.distance_to(mouse_pos) < self.item_size / 2:
                color = (0, 200, 0)
                line = 0
            pg.draw.circle(self.surf, color, self.center, self.item_size / 2, line)
        else:
            radius = self._get_radius(length, dt)
            self.surf = pg.Surface(vec2((radius + self.item_size) * 2), pg.SRCALPHA)
            self.center = vec2(self.surf.get_size()) / 2
            spacing_angle = 360 / length
            half_spacing_angle = spacing_angle / 2

            for i, item in enumerate(self.items):
                current_angle = spacing_angle * i
                item_angle = vec2(0, -1).rotate(current_angle).normalize()

                color = (200, 200, 200, 100)
                line = 1
                angle_to_mouse = abs((mouse_pos - self.center).angle_to(item_angle))
                dist_to_mouse = self.center.distance_to(mouse_pos)
                if (
                    angle_to_mouse < half_spacing_angle
                    and dist_to_mouse <= radius + self.item_size
                ):
                    self.selected = item
                    color = (0, 200, 0)
                    line = 0
                size = self.item_size / 2
                if self.speed:
                    size = self.remap(self.progress, 0, self.speed, 0, size)
                pg.draw.circle(
                    self.surf, color, self.center + (item_angle * radius), size, line
                )

    def _get_radius(self, length, dt):
        radius = self.radius or max(
            self.item_size, ((self.item_size + self.item_padding) / 6) * length
        )
        if not self.speed:
            return radius
        else:
            if self.state == "opening":
                if self.progress < self.speed:
                    self.progress = min(self.speed, self.progress + dt)
                else:
                    self.state = "open"
            elif self.state == "closing":
                if self.progress > 0:
                    self.progress = max(0, self.progress - dt)
                else:
                    self.state = "closed"
            return self.remap(self.progress, 0, self.speed, 0, radius)

    def remap(self, old_val, old_min, old_max, new_min, new_max):
        old_range = old_max - old_min
        new_range = new_max - new_min
        return (((old_val - old_min) * new_range) / old_range) + new_min

    def draw(self, surf):
        if self.state == "closed" or not self.surf:
            return
        surf.blit(self.surf, self.pos - self.center)


Game(1280, 720).run()
