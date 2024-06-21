from abc import ABC

import pygame.draw
from pygame import Rect, Vector2, Surface


class MoveMixin:
    _speed = Vector2(10, 0)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed: Vector2):
        self._speed = new_speed



class _Base(Surface, ABC):
    def __init__(self, size: tuple, base_color, bg_color):
        super().__init__(size)

        self._base_color = base_color  # основной цвет
        self._bg_color = bg_color  # для перерисовки

        self._rect = self.get_rect()

    @property
    def base_color(self):
        return self._base_color

    @property
    def rect(self) -> Rect:
        return self._rect


class Block(_Base):
    ...


class Ball(_Base, MoveMixin):
    def __init__(self, diameter: int, base_color, screen_color):

        self._radius = diameter / 2
        self._sprite_color = base_color

        size = diameter, diameter

        super().__init__(size, screen_color, screen_color)


class Board(_Base, MoveMixin):
    def __init__(self, size, start_pos,  board_color, screen_color, speed):
        self.board_color = board_color
        self.screen_color = screen_color
        self.speed = speed

        super().__init__(size, board_color, screen_color)

        # self.rect = self.get_rect()
        self.rect.center = start_pos

    def move(self, direction: int) -> Vector2:
        print('self.rect.center', self.rect.center)

        speed = self.speed

        self.rect.move_ip(speed * direction)

        new_pos = self.rect.center
        print('new_pos', new_pos)

        return new_pos
