import pygame
from pygame.color import THECOLORS
from pygame import Vector2, K_LEFT, K_RIGHT
import sys
from typing import Iterable, Union

from classes import Ball, Board
# from contoller import move_to_left, move_to_right, controller
# from objects_controller import init_screen

# SCREEN_WIDTH = 1200
# SCREEN_HEIGHT = 800
# SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# SCREEN_COLOR = THECOLORS.get('black', (0, 0, 0))
# LINES_COLOR = THECOLORS.get('wheat', (0, 0, 0))

BALL_COLOR = THECOLORS.get('azure', (0, 0, 0))
BALL_RADIUS = 25

BOARD_SIZE = (100, 10)
BOARD_COLOR = THECOLORS.get('bisque1', (0, 0, 0))
BOARD_SPEED = Vector2(5, 0)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

SCREEN_COLOR = THECOLORS.get('black', (0, 0, 0))

OBJECTS_DICT = dict()

print(THECOLORS.keys())

FPS = 60

TO_LEFT = -1  # движение влево
TO_RIGHT = 1  # движение вправо

KEY_TO_LEFT = K_LEFT
KEY_TO_RIGHT = K_RIGHT

BALL_START_POSITION = Vector2(100, 100)
BOARD_START_POSITION = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)

START_POSITIONS_DICT = {
    'ball': BALL_START_POSITION,
    'board': BOARD_START_POSITION
}

CANVAS = pygame.display.set_mode(SCREEN_SIZE)


# ------------------------------------------------------------


# def fill_obj(obj: 'Surface', color):
#     obj.fill(color)
#
#
# def fill_objs(objs: Iterable):
#     for obj in objs:
#         fill_obj(obj)


# def blit_obj(canvas: 'Surface', obj: '_Base'):
#     canvas.blit(obj, obj.rect)


def blit_objs(canvas: 'Surface', objs: Iterable):
    for obj in objs:
        canvas.blit(obj, obj.rect)


def move_obj(obj, direction: int):
    obj.move(direction)


# def check_movement(obj, old_pos, new_pos):
#     if new_pos != old_pos:
#         blit_obj(CANVAS, obj)




ACTIONS_KEYS = {
    KEY_TO_LEFT: TO_LEFT,
    KEY_TO_RIGHT: TO_RIGHT,
}


pygame.init()  # Инициализация
clock = pygame.time.Clock()

# screen = CANVAS

ball = Ball(BALL_RADIUS, BALL_COLOR, SCREEN_COLOR)
board = Board(BOARD_SIZE, BOARD_START_POSITION, BOARD_COLOR, SCREEN_COLOR, BOARD_SPEED)



OBJECTS_DICT['screen'] = CANVAS
OBJECTS_DICT['ball'] = ball
OBJECTS_DICT['board'] = board

GAME_OBJS = [
    ball,
    board
]

for g_obj in GAME_OBJS:
    color = g_obj.base_color
    g_obj.fill(color)
    # fill_obj(g_obj, color)

pygame.draw.circle(ball, ball._sprite_color, ball._rect.center, ball._radius)

blit_objs(CANVAS, GAME_OBJS)

# screen.blit(ball, (100, 100))
# screen.blit(board, (600, 750))


board_pos = BOARD_START_POSITION  # Текущая позиция доски
ball_pos = BALL_START_POSITION  # Текущая позиция шара


running = True
while running:
    for event in pygame.event.get():
        e_type = event.type

        if event.type == pygame.QUIT:
            running = False

        elif e_type == pygame.KEYDOWN:
            try:
                direction = ACTIONS_KEYS[event.key]
                # board_pos_new = move_obj(board, direction)
                move_obj(board, direction)
                # blit_obj(CANVAS, board)
                # check_movement(board, board_pos, board_pos_new)

                # board_pos = board_pos_new

            except KeyError:
                print('Рандомная клавиша')

    CANVAS.fill(SCREEN_COLOR)

    blit_objs(CANVAS, GAME_OBJS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()





