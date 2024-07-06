from abc import ABC
from typing import Union, List

import pygame.draw
from pygame import Rect, Vector2, Surface
from pygame.sprite import Sprite


class MoveMixin:
    _speed = Vector2(1, 0)
    # _direction = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed: Vector2):
        self._speed = new_speed

    def move(self) -> Union[Vector2, None]:
        speed = self.speed

        if hasattr(self, 'rect'):
            rect = getattr(self, 'rect')

            # rect.move_ip(speed)
            rect.center += speed

            return rect.center


class Block(Surface):
    def __init__(self, size: tuple, base_color=None, bg_color=None):
        super().__init__(size)

        self._size = size
        self._base_color = base_color  # основной цвет
        self._bg_color = bg_color  # для перерисовки

        self._rect = self.get_rect()

    @classmethod
    def init_from_rect(cls, rect):
        size = rect.size
        obj = cls(size)
        obj.rect.center = rect.center

        return obj

    @property
    def base_color(self):
        return self._base_color

    @base_color.setter
    def base_color(self, color):
        self._base_color = color

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def size(self):
        return self._size

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color


class Ball(Sprite, Block, MoveMixin):
    # def __init__(self, image, speed):
    def __init__(self, image):
        super().__init__()

        self._image = image
        self._rect = self._image.get_rect()
        # self.speed = speed

    @property
    def image(self):
        return self._image

    @property
    def rect(self) -> Rect:
        return super().rect

    @rect.setter
    def rect(self, bottom_pos):
        """
        Задает стартовую позицию
        :param bottom_pos: Позиция центра нижней граници
        """

        self._rect = self.image.get_rect(midbottom=bottom_pos)

    def check_collide(self, obstacles_list: list) -> int:
        # return self.rect.collidelistall(obstacles_list)  # можно использовать спец. метод, сразу возвращая объекты, но я не использую
        return self.rect.collidelist(obstacles_list)  # можно использовать спец. метод, сразу возвращая объекты, но я не использую

    def change_direction(self, collide: Block):
        top = self.rect.top
        bot = self.rect.bottom
        left = self.rect.left
        right = self.rect.right

        speed = self.speed

        obj = collide
        obj_top = obj.rect.top
        obj_bot = obj.rect.bottom
        obj_left = obj.rect.left
        obj_right = obj.rect.right

        if speed.x == 0 or speed.y == 0:  # движение вверх/вниз, или влево/вправо
            self.speed *= -1

            return

        if speed.y < 0:
            height = top - obj_bot

        else:
            height = bot - obj_top

        if speed.x > 0:
            width = right - obj_left

        else:
            width = left - obj_right

        if height == width:  # попали ровно в угол
            self.speed *= -1

        elif height > width:
            self.speed.y *= -1

        else:
            self.speed.x *= -1

    def __str__(self):
        return self.__class__.__name__ + str(self._rect.center)


class Board(Block, MoveMixin):
    # def __init__(self, size, start_pos,  board_color, screen_color, speed):
    def __init__(self, size, board_color, screen_color):
        self.board_color = board_color
        self.screen_color = screen_color
        # self.speed = speed

        super().__init__(size, board_color, screen_color)

        # self.rect.center = start_pos

    @property
    def rect(self) -> Rect:
        return super().rect

    @rect.setter
    def rect(self, center_pos):
        """
        Задает стартовую позицию
        :param center_pos: Позиция центра
        """
        self._rect.center = center_pos

    # def move(self, direction) -> Vector2:
    #     speed = self.speed
    #
    #     self.rect.move_ip(speed)
    #
    #     return self.rect.center
