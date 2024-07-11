from pygame import Rect, Vector2, Surface
from pygame.sprite import Sprite


class MoveMixin:
    """
    Миксин для добавления свойства двигаться
    """
    _speed = Vector2(1, 0)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed: Vector2):
        self._speed = new_speed

    def move(self) -> None:
        """
        Смещает центр объекта на заданную скорость
        """
        speed = self.speed

        if hasattr(self, 'rect'):
            rect = getattr(self, 'rect')

            rect.center += speed


class Block(Surface):
    """
    Описывает разрушаемый блок
    """

    _count = 0

    def __init__(self, size: tuple, base_color=None):
        super().__init__(size)

        self._size = size
        self._base_color = base_color  # основной цвет

        self._rect = self.get_rect()
        if self.__class__.__name__ == 'Block':
            Block._count += 1

    @classmethod
    def destruct_block(cls):
        cls._count -= 1

    @classmethod
    def init_from_rect(cls, rect: Rect) -> 'Block':
        """
        Создает и возвращает новый блок на основе объекта  Rect
        :param rect: Rect на основе которого создать объект
        :return: объект Block
        """
        size = rect.size
        obj = cls(size)
        obj.rect.center = rect.center

        return obj

    @classmethod
    def get_count(cls) -> int:
        return cls._count

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


class Ball(Sprite, Block, MoveMixin):
    """
    Описывает шарик
    """
    def __init__(self, image):
        super().__init__()

        self._image = image
        self._rect = self._image.get_rect()

    @property
    def image(self):
        return self._image

    @property
    def rect(self) -> Rect:
        return super().rect

    @rect.setter
    def rect(self, bottom_pos: Vector2):
        """
        Задает стартовую позицию
        :param bottom_pos: Позиция центра нижней граници
        """

        self._rect = self.image.get_rect(midbottom=bottom_pos)

    def control_pos_out_screen(self, screen) -> None:
        """
        Контролирует позицию шарика внутри экрана, изменяет направления от удара о борта
        :param screen: экран
        :return:
        """
        screen_rect = screen.get_rect()
        ball_rect = self.rect

        speed = self.speed

        if ball_rect.left <= screen_rect.left or ball_rect.right >= screen_rect.right:
            if speed.y == 0:
                self.speed *= -1

            else:
                self.speed.x *= -1

        # elif ball_rect.top <= screen_rect.top:
        elif ball_rect.top <= screen_rect.top or ball_rect.bottom >= screen_rect.bottom:
            if speed.x == 0:
                self.speed *= -1

            else:
                self.speed.y *= -1

    def check_collide(self, obstacles_list: list) -> int:
        """
        Проверяте, столкнулся ли шарик с блоком
        :param obstacles_list: список блоков
        :return: индекс блока, с которым столкнулся шарик или -1, если нет столкновения ни с одним блоком
        """
        return self.rect.collidelist(obstacles_list)  # можно использовать спец. метод, сразу возвращая объекты, но я не использую

    def change_direction(self, collide: Block) -> None:
        """
        Изменяет направление движения шарика от препятствия
        :param collide: препятствие
        """
        speed = self.speed

        if speed.x == 0 or speed.y == 0:  # движение вверх/вниз, или влево/вправо
            self.speed *= -1

            return

        ball_left_c = Vector2(self.rect.bottomleft)
        ball_right_c = Vector2(self.rect.topright)

        obj_left_c = Vector2(collide.rect.bottomleft)
        obj_right_c = Vector2(collide.rect.topright)

        left = max(ball_left_c.x, obj_left_c.x)
        top = max(ball_right_c.y, obj_right_c.y)
        right = min(ball_right_c.x, obj_right_c.x)
        bot = min(ball_left_c.y, obj_left_c.y)

        width = right - left
        height = top - bot

        # if speed.y < 0:
        #     height = top - obj_bot
        #
        # else:
        #     height = bot - obj_top
        #
        # if speed.x > 0:
        #     width = right - obj_left
        #
        # else:
        #     width = left - obj_right

        # if height == width:  # попали ровно в угол
        #     self.speed *= -1

        if height < width:
            self.speed.y *= -1

        else:
            self.speed.x *= -1

    def change_direction1(self, collide: Block) -> None:
        """
        Изменяет направление движения шарика от препятствия
        :param collide: препятствие
        """
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
    """
    Описывает доску.
    """
    def __init__(self, size, board_color):
        self.board_color = board_color

        super().__init__(size, board_color)

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
