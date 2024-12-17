import pygame
import random

# параметры игры
fps = 7  # частота кадров
speed = 7 # скорость игры
screen_width = 900
screen_height = 800
field_size = 20  # размер квадратного игрового поля
cell_size = 30  # размер клетки

pygame.init()
pygame.display.set_caption('Тетрис с поворотом')
clock = pygame.time.Clock()
field_x = (screen_width - field_size * cell_size) // 2
field_y = (screen_height - field_size * cell_size) // 2
screen = pygame.display.set_mode((screen_width, screen_height))
timer = 0
bomb_image = pygame.image.load('bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (70, 50))
rules_image = pygame.image.load('?.png')
rules_image = pygame.transform.scale(rules_image, (90, 80))
with open('rules.txt', 'r', encoding='utf-8') as file:
    text_rules = file.read()
text_rules = text_rules.splitlines()

# цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (204, 255, 255)
colors = [
    (255, 255, 255),
    (255, 102, 204),
    (153, 153, 255),
    (255, 51, 0),
    (204, 204, 0),
    (102, 255, 51),
    (0, 153, 255),
    (0, 0, 255),
    (204, 0, 102),
    (255, 255, 0),
    (204, 153, 255),
    (153, 255, 204),
    (0, 0, 0)
]
color_pause = red
screen.fill(white)

# текст
font1 = pygame.font.SysFont('Calibri', 30, bold=True)
font2 = pygame.font.SysFont('Calibri', 15)
font3 = pygame.font.Font("kongtext.ttf", 40)


def show_text(screen, text, font, color, x, y):
    a = font.render(text, True, color)
    screen.blit(a, (x, y))


def rules():
    screen.fill(white)
    y = 0
    for i in text_rules:
        text = font2.render(i, True, black)
        screen.blit(text, (0, y))
        y += text.get_height() + 5


class Tetrimino:
    # фигуры и вращения
    figures = [
        # |
        [[[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]],

        # O
        [[[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]],

        # Z
        [[[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]],

        # S
        [[[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
         [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]],

        # L
        [[[0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]],

        # J
        [[[1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
         [[0, 1, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]],

        # T
        [[[0, 1, 1, 1], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
         [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]],

        # Г
        [[[1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]],
         [[0, 1, 1, 1], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]],

        # B
        [[[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
    ]

    def __init__(self):
        self.x = field_size // 2 - 2
        self.y = field_size // 2 - 2
        self.type = random.randint(0, len(self.figures) - 2)
        self.color = random.randint(1, len(colors) - 2)
        self.rotation = 0

    def shape(self):
        return self.figures[self.type][self.rotation]


class Game:
    def __init__(self):
        self.score = 0
        self.figure = None
        self.next_figure = Tetrimino()
        self.figure_count = -1
        self.game_over = False
        self.fast_down = False
        self.fast_left = False
        self.fast_right = False
        self.pause = True
        self.bomb_active = False

        self.field = [[0] * field_size for _ in range(field_size)]  # создание поля

    def new_figure(self):
        self.figure = self.next_figure
        self.next_figure = Tetrimino()
        self.figure_count += 1
        if self.figure_count % 3 == 0:  # поворот поля через каждые 3 фигуры
            self.rotate_field()

    def rotate_field(self):  # поворот поля на 90
        new_field = [[0] * field_size for i in range(field_size)]
        for i in range(field_size):
            for j in range(field_size):
                new_field[i][j] = self.field[field_size - 1 - j][i]
        self.field = new_field

    def check_figure(self):  # проверка расположения фигуры
        for i in range(4):
            for j in range(4):
                if self.figure.shape()[i][j] == 1:
                    y, x = i + self.figure.y, j + self.figure.x
                    if y >= field_size or x >= field_size or x < 0 or self.field[y][x] > 0:
                        return False
        return True

    def check_frame(self):
        for level in range(field_size // 2 - 2):  # ищем уровень на котором есть рамка
            # проверяем верхнюю и нижнюю строки
            if any(self.field[level][i] == 0 or self.field[field_size - level - 1][i] == 0 for i in
                   range(level, field_size - level)):
                continue
            # проверяем левый и правый столбцы
            if any(self.field[j][level] == 0 or self.field[j][field_size - level - 1] == 0 for j in
                   range(level + 1, field_size - level - 1)):
                continue
            return level
        return False

    def clear_frame(self, level):
        # зануляем рамку
        for i in range(level, field_size - level):
            self.field[level][i] = 0
            self.field[field_size - level - 1][i] = 0
        for i in range(level + 1, field_size - level - 1):
            self.field[i][level] = 0
            self.field[i][field_size - level - 1] = 0
        # сдвигаем верхнюю строку вверх
        for i in range(level + 1, field_size - level - 1):
            self.field[level][i] = self.field[level + 1][i]
            self.field[level + 1][i] = 0
        # сдвигаем нижнюю строку вниз
        for i in range(level + 1, field_size - level - 1):
            self.field[field_size - level - 1][i] = self.field[field_size - level - 2][i]
            self.field[field_size - level - 2][i] = 0
        # сдвигаем левый столбец влево
        for i in range(level + 2, field_size - level - 2):
            self.field[i][level] = self.field[i][level + 1]
            self.field[i][level + 1] = 0
        # сдвигаем правый столбец вправо
        for i in range(level + 2, field_size - level - 2):
            self.field[i][field_size - level - 1] = self.field[i][field_size - level - 2]
            self.field[i][field_size - level - 2] = 0

    def move_down(self):  # спуск
        self.figure.y += 1
        if not self.check_figure():
            self.figure.y -= 1
            self.fix_figure()

    def move_side(self, side):  # перемещение фигуры
        self.figure.x += side
        if not self.check_figure():
            self.figure.x -= side

    def fix_figure(self):  # закрепление на месте
        for i in range(4):
            for j in range(4):
                if self.figure.shape()[i][j] == 1:
                    # в соответсвующих ячейках записываем номер цвета
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color

        # проверяем можно ли удалить рамку
        z = self.check_frame()
        if z is not False:
            for x in range(z, field_size // 2 - 2):
                self.clear_frame(x)
            if not self.game_over:
                self.score += 200

        # проверям взрыв
        if self.bomb_active and self.figure.type == len(self.figure.figures) - 1:
            self.boom(self.figure.x, self.figure.y)

        self.new_figure()
        if not self.check_figure():
            self.game_over = True
        if not self.game_over:
            self.score += 1

    def rotate_figure(self):
        old_rotation = self.figure.rotation
        self.figure.rotation = (self.figure.rotation + 1) % len(self.figure.figures[self.figure.type])
        if not self.check_figure():
            self.figure.rotation = old_rotation

    def bomb(self):
        self.next_figure.type = len(self.figure.figures) - 1
        self.next_figure.color = 12
        self.bomb_active = True

    def boom(self, x, y):
        for i in range(-1, 3):
            for j in range(-1, 3):
                if 0 <= x + j < field_size and 0 <= y + i < field_size:
                    self.field[y + i][x + j] = 0
        self.bomb_active = False
        if not self.game_over:
            self.score += 10


game = Game()

while True:
    if game.figure is None:
        game.new_figure()

    timer += 1
    if game.score > 100:
        speed = 3
    if not game.pause:
        if timer % speed == 0 or game.fast_down:
            game.move_down()
        if game.fast_left:
            game.move_side(-1)
        if game.fast_right:
            game.move_side(1)

    # кнопка с правилами
    button_rules = pygame.Rect(0, screen_height - 100, 100, 100)
    pygame.draw.rect(screen, white, button_rules)
    screen.blit(rules_image, button_rules.topleft)

    # кнопка с бомбой
    button_bomb = pygame.Rect(screen_width - 100, 10, 70, 50)
    pygame.draw.rect(screen, white, button_bomb)
    screen.blit(bomb_image, button_bomb.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  # нажатие клавиши
            if event.key == pygame.K_UP:
                game.rotate_figure()
            if event.key == pygame.K_DOWN:
                game.fast_down = True
            if event.key == pygame.K_LEFT:
                game.fast_left = True
            if event.key == pygame.K_RIGHT:
                game.fast_right = True
            if event.key == pygame.K_ESCAPE:
                screen.fill(white)
                game.__init__()
            if event.key == pygame.K_RETURN:
                while game.check_figure():
                    game.figure.y += 1
                game.figure.y -= 1
                game.fix_figure()
            if event.key == pygame.K_SPACE:
                if game.pause or game.game_over:
                    game.pause = False
                    color_pause = red
                else:
                    game.pause = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rules.collidepoint(event.pos):
                rules()
                color_pause = white
                game.pause = True
            if button_bomb.collidepoint(event.pos):
                game.bomb()

        if event.type == pygame.KEYUP:  # опускание клавиши
            if event.key == pygame.K_DOWN:
                game.fast_down = False
            if event.key == pygame.K_LEFT:
                game.fast_left = False
            if event.key == pygame.K_RIGHT:
                game.fast_right = False

    if game.pause:
        text1 = pygame.font.Font("kongtext.ttf", 45).render('PAUSE', True, color_pause)
        screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, screen_height // 2 - text1.get_height() // 2))
        text2 = pygame.font.SysFont('Calibri', 25).render('нажмите пробел', True, red)
        screen.blit(text2, (
            screen_width // 2 - text1.get_width() // 2 + 15, screen_height // 2 - text1.get_height() // 2 + 40))
    else:
        screen.fill(white)
        # отображение поля
        for x in range(field_size):
            for y in range(field_size):
                # окошко для предпросмотра следующей фигуры в центре
                if (field_size // 2 - 2 <= x < field_size // 2 + 2 and
                        field_size // 2 - 2 <= y < field_size // 2 + 2):
                    color = blue
                else:
                    color = colors[game.field[y][x]]
                pygame.draw.rect(screen, color,
                                 (field_x + x * cell_size, field_y + y * cell_size, cell_size, cell_size), 0)
                pygame.draw.rect(screen, (169, 169, 169),
                                 (field_x + x * cell_size, field_y + y * cell_size, cell_size, cell_size), 1)

        # отображение текущей фигуры
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    if game.figure.shape()[i][j] == 1:
                        x = (j + game.figure.x) * cell_size + field_x
                        y = (i + game.figure.y) * cell_size + field_y
                        pygame.draw.rect(screen, colors[game.figure.color], (x, y, cell_size, cell_size), 0)

        # предпросмотр следующей фигуры
        for i in range(4):
            for j in range(4):
                if game.next_figure.shape()[i][j] == 1:
                    x = (field_size // 2 - 2 + j) * cell_size + field_x
                    y = (field_size // 2 - 2 + i) * cell_size + field_y
                    pygame.draw.rect(screen, colors[game.next_figure.color], (x, y, cell_size, cell_size), 0)

        show_text(screen, f'Score: {game.score}', font3, black, 10, 10)
        pygame.draw.rect(screen, white, button_rules)
        screen.blit(rules_image, button_rules.topleft)
        pygame.draw.rect(screen, white, button_bomb)
        screen.blit(bomb_image, button_bomb.topleft)

        if game.game_over:
            screen.fill(white)
            text = font1.render('Конец игры', True, red)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            text1 = font1.render(f'Итоговый счет: {game.score}', True, red)
            screen.blit(text1,
                        (screen_width // 2 - text1.get_width() // 2, screen_height // 2 + text1.get_height() // 2))

    pygame.display.flip()
    clock.tick(fps)
