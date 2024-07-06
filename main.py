import random

import pygame
from pygame.color import THECOLORS
from pygame import Vector2, K_LEFT, K_RIGHT
import sys
from typing import Iterable, Union

from classes import Ball, Board, Block
pygame.init()  # Инициализация

# from contoller import move_to_left, move_to_right, controller
# from objects_controller import init_screen

# SCREEN_WIDTH = 1200
# SCREEN_HEIGHT = 800
# SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# SCREEN_COLOR = THECOLORS.get('black', (0, 0, 0))
# LINES_COLOR = THECOLORS.get('wheat', (0, 0, 0))





SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_COLOR_NAME = 'black'
SCREEN_COLOR = THECOLORS.get(SCREEN_COLOR_NAME, (0, 0, 0))

CANVAS = pygame.display.set_mode(SCREEN_SIZE)



BOARD_SIZE = (100, 10)
BOARD_COLOR = THECOLORS.get('bisque1', (0, 0, 0))
BOARD_SPEED = Vector2(1, 0)
BOARD_START_POSITION = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)

BALL_SPRITE = pygame.image.load('resources/sprites/ball.png').convert_alpha()
BALL_START_POSITION = Vector2(100, 100)
BALL_SPEED = Vector2(0, 2) * -1

print(BALL_SPEED.x, BALL_SPEED.y)
BALL_SPEED.rotate_ip(15)
print(BALL_SPEED.x, BALL_SPEED.y)

BLOCK_SIZE = (50, 20)
BLOCK_COLORS = [THECOLORS[color] for color in THECOLORS.keys() if color != SCREEN_COLOR_NAME]
BLOCK_LINE_COUNT = 10
BLOCK_COUNT_IN_LINE = (SCREEN_WIDTH // BLOCK_SIZE[0])



OBJECTS_DICT = dict()

print(THECOLORS.keys())

FPS = 60





TO_LEFT = Vector2(-1, 0)  # движение влево
TO_RIGHT = Vector2(1, 0)  # движение вправо

KEY_TO_LEFT = K_LEFT
KEY_TO_RIGHT = K_RIGHT

ACTIONS_KEYS = {
    KEY_TO_LEFT: TO_LEFT,
    KEY_TO_RIGHT: TO_RIGHT,
}

GAME_OBJS = list()


# ------------------------------------------------------------

#
# def fill_obj(obj: 'Surface', color):
#     obj.fill(color)
#
#
# def fill_objs(objs: Iterable):
#     for obj in GAME_OBJS:
#         fill_obj(obj)


# def blit_obj(canvas: 'Surface', obj: '_Base'):
#     canvas.blit(obj, obj.rect)


def blit_objs():
    """
    Отрисовка блоков и доски на экране
    """
    # map(lambda obj: CANVAS.blit(obj, obj.rect), GAME_OBJ)

    for obj in GAME_OBJS:
        # print(obj.rect.center)
        CANVAS.blit(obj, obj.rect)


def create_blocks(start_block) -> list:
    """
    Создает блоки по образцу
    :param start_block: Блок
    :return: Список блоков
    """
    blocks = [start_block]

    offset_x = Vector2(BLOCK_SIZE[0], 0)
    topleft = Vector2(start_block.rect.topleft) + offset_x

    for i in range(BLOCK_LINE_COUNT):
        for j in range(BLOCK_COUNT_IN_LINE):
            block = Block.init_from_rect(start_block.get_rect(topleft=topleft))

            block.base_color = random.choice(BLOCK_COLORS)
            block.bg_color = SCREEN_COLOR

            blocks.append(block)

            topleft += offset_x

        topleft = Vector2(start_block.rect.bottomleft) * (i + 1)

    return blocks




# def check_movement(obj, old_pos, new_pos):
#     if new_pos != old_pos:
#         blit_obj(CANVAS, obj)


clock = pygame.time.Clock()

ball = Ball(BALL_SPRITE)

ball.speed = BALL_SPEED
# ball.rect = BALL_START_POSITION

# board = Board(BOARD_SIZE, BOARD_START_POSITION, BOARD_COLOR, SCREEN_COLOR, BOARD_SPEED)
board = Board(BOARD_SIZE, BOARD_COLOR, SCREEN_COLOR)
board.rect = BOARD_START_POSITION
board.speed = BOARD_SPEED

BALL_START_POSITION = board.rect.midtop  # Привязываем стартовую позицию шара к доске
# print('top', ball.rect.size)
ball.rect = BALL_START_POSITION

block = Block(BLOCK_SIZE, random.choice(BLOCK_COLORS), SCREEN_COLOR)

GAME_OBJS.extend(create_blocks(block))
GAME_OBJS.append(board)

for g_obj in GAME_OBJS:
    color = g_obj.base_color
    g_obj.fill(color)

blit_objs()
CANVAS.blit(ball.image, ball.rect)

board_pos = BOARD_START_POSITION  # Текущая позиция доски
ball_pos = BALL_START_POSITION  # Текущая позиция шара

running = True
key_down = None
while running:
    for event in pygame.event.get():
        e_type = event.type

        if event.type == pygame.QUIT:
            running = False

        elif e_type == pygame.KEYDOWN:
            key_down = event.key

        elif e_type == pygame.KEYUP:
            key_down = None

    direction = ACTIONS_KEYS.get(key_down)

    if direction is not None:
        board.speed = direction
    else:
        board.speed = Vector2(0)

    board.move()
    ball.move()

    ind = ball.check_collide(GAME_OBJS)

    obj = GAME_OBJS[ind]

    if ind != -1:
        ball.change_direction(obj)
        if not isinstance(obj, Board):
            GAME_OBJS.pop(ind)

    CANVAS.fill(SCREEN_COLOR)

    blit_objs()
    CANVAS.blit(ball.image, ball.rect)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()





