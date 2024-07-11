import random
import time

import pygame

from pygame.color import THECOLORS
from pygame import Vector2, K_LEFT, K_RIGHT
from classes import Ball, Board, Block

pygame.init()  # Инициализация

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_COLOR_NAME = 'black'
SCREEN_COLOR = THECOLORS.get(SCREEN_COLOR_NAME, (0, 0, 0))

CANVAS = pygame.display.set_mode(SCREEN_SIZE)

BOARD_SIZE = (100, 30)
BOARD_COLOR = THECOLORS.get('bisque1', (0, 0, 0))
BOARD_SPEED = Vector2(5, 0)
BOARD_START_POSITION = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)

BALL_SPRITE = pygame.image.load('resources/sprites/ball.png').convert_alpha()
BALL_START_POSITION = Vector2(100, 100)
BALL_SPEED = Vector2(0, 7) * -1

BALL_SPEED.rotate_ip(23)

BLOCK_SIZE = (50, 20)
BLOCK_COLORS = [THECOLORS[color] for color in THECOLORS.keys() if color != SCREEN_COLOR_NAME]
BLOCK_LINE_COUNT = 1
# BLOCK_LINE_COUNT = 10
BLOCK_COUNT_IN_LINE = (SCREEN_WIDTH // BLOCK_SIZE[0])

OBJECTS_DICT = dict()

FPS = 60

TO_LEFT = BOARD_SPEED * -1  # движение влево
TO_RIGHT = BOARD_SPEED  # движение вправо

KEY_TO_LEFT = K_LEFT
KEY_TO_RIGHT = K_RIGHT

ACTIONS_KEYS = {
    KEY_TO_LEFT: TO_LEFT,
    KEY_TO_RIGHT: TO_RIGHT,
}

GAME_OBJS = list()


# ------------------------------------------------------------
def blit_objs():
    """
    Отрисовка блоков и доски на экране
    """
    for obj in GAME_OBJS:
        CANVAS.blit(obj, obj.rect)


def create_blocks(start_block) -> list:
    """
    Создает блоки по образцу
    :param start_block: Блок
    :return: Список блоков
    """
    # blocks = [start_block]
    blocks = []

    offset_x = Vector2(BLOCK_SIZE[0], 0)
    # topleft = Vector2(start_block.rect.topleft) + offset_x
    topleft = Vector2(start_block.rect.topleft)

    for i in range(BLOCK_LINE_COUNT):
        for j in range(BLOCK_COUNT_IN_LINE):
            block = Block.init_from_rect(start_block.get_rect(topleft=topleft))

            block.base_color = random.choice(BLOCK_COLORS)
            # block.bg_color = SCREEN_COLOR

            blocks.append(block)

            topleft += offset_x

        topleft = Vector2(start_block.rect.bottomleft) * (i + 1)

    return blocks


clock = pygame.time.Clock()

ball = Ball(BALL_SPRITE)

ball.speed = BALL_SPEED

board = Board(BOARD_SIZE, BOARD_COLOR)
board.rect = BOARD_START_POSITION
board.speed = BOARD_SPEED

BALL_START_POSITION = board.rect.midtop  # Привязываем стартовую позицию шара к доске

ball.rect = BALL_START_POSITION

block = Block(BLOCK_SIZE, random.choice(BLOCK_COLORS))
Block.destruct_block()  # не считаем только что созданный, он образец

# blocks = create_blocks(block)
GAME_OBJS.extend(create_blocks(block))

GAME_OBJS.append(board)

for g_obj in GAME_OBJS:
    color = g_obj.base_color
    g_obj.fill(color)

blit_objs()
CANVAS.blit(ball.image, ball.rect)

running = True
key_down = None

print(Block.get_count())
win = False
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

    ball.control_pos_out_screen(CANVAS)

    ind = ball.check_collide(GAME_OBJS)

    if ind != -1:
        obj = GAME_OBJS[ind]
        ball.change_direction(obj)

        if not isinstance(obj, Board):
            GAME_OBJS.pop(ind)
            Block.destruct_block()
            print(Block.get_count())

    if Block.get_count() <= 0:
        running = False
        win = True

    CANVAS.fill(SCREEN_COLOR)

    blit_objs()
    CANVAS.blit(ball.image, ball.rect)

    pygame.display.flip()

    clock.tick(FPS)

if win:
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = my_font.render('Победа!', False, (220, 0, 0))
    CANVAS.blit(textsurface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2.5)

pygame.quit()
