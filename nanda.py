from warnings import warn
from math import sqrt, hypot
from random import choice

from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import init, image, display, quit, event, time
from pygame.font import get_default_font, SysFont, Font
from pygame.sprite import Sprite, Group
from pygame.transform import scale, flip
# Type Mark
from pygame.rect import Rect
from pygame import Surface


def multi_tuple(tp, value):
    o = []
    for x in tp:
        o.append(x * value)
    return o


def distance(x_y1, x_y2):
    x1, y1 = x_y1
    x2, y2 = x_y2
    return hypot(x2 - x1, y2 - y1)


class Gird:
    def __init__(self, xe, ye, xs=0, ys=0):
        """
        initialize gird data
        :param xe: end x value
        :param ye: end y value
        :param xs: start x value
        :param ys: start y value
        """
        self.xs, self.xe = xs, xe
        self.ys, self.ye = ys, ye
        self.xx, self.yy = [], []
        self.pts = []

    def generate_row(self, x_rows, y_rows, int_only=True):
        self.xx, self.yy = [], []
        # if int_only:
        len_x = self.xe - self.xs
        len_y = self.ye - self.ys

        dx, dy = len_x / x_rows, len_y / y_rows

        for ix in range(x_rows):
            self.xx.append(round(self.xs + dx * ix))
        for iy in range(y_rows):
            self.yy.append(round(self.ys + dy * iy))

    def points(self):
        self.pts = []
        for y in self.yy:
            for x in self.xx:
                self.pts.append((x, y))
        return self.pts


class QSprite(Sprite):
    ZERO = 0
    MID = 1

    def __init__(self, img, border_size, *groups, vx=0, vy=0):
        self.image: Surface = img
        self.screen_x, self.screen_y = border_size

        self.rect: Rect = self.image.get_rect()
        self.pixel_x, self.pixel_y = self.image.get_width(), self.image.get_height()

        self.vx, self.vy = vx, vy

        super().__init__(*groups)

    def set_pos(self, x, y, pos_type=ZERO):
        if pos_type == self.ZERO:

            self.rect.x, self.rect.y = x, y
        elif pos_type == self.MID:
            self.rect.x = x - self.pixel_x
            self.rect.y = y - self.pixel_y

    def get_pos(self, pos_type=ZERO):
        if pos_type == self.ZERO:
            return self.rect.x, self.rect.y
        elif pos_type == self.MID:
            return self.rect.x + self.pixel_x / 2, self.rect.y + self.pixel_y / 2


class Char(QSprite):
    STATIC = 0
    MOVE_L = -1
    MOVE_R = 1

    # UP = 2
    # DOWN = -2

    def __init__(self, img, border_size, *groups, vx=0, vy=0):
        super().__init__(img, border_size, *groups, vx=vx, vy=vy)
        self.img_moves, self.img_moves_l = [], []

        self.mov_index_left, self.mov_index_right = 0, 0
        self.load_img()
        self.animate = self.STATIC

    def load_img(self):
        for _ in range(68 + 1):
            img = scale(
                image.load('assets/img/zero_move/' + str(_).zfill(5) + '.png'), (80, 130)
            )
            self.img_moves.append(img)
            self.img_moves_l.append(flip(img, True, False))

    def edge(self, x, y):
        if x < 0 and self.vx < 0:
            self.vx = 0
        elif x > self.screen_x - 72 and self.vx > 0:
            self.vx = 0

        if y < 0 and self.vy < 0:
            self.vy = 0
        elif y > self.screen_y - 108 - 25 and self.vy > 0:
            self.vy = 0

    def avatar(self):
        if self.animate == self.STATIC:
            pass
        elif self.animate == self.MOVE_L:
            self.image = self.img_moves_l[self.mov_index_left]
            self.mov_index_left += 1
            if self.mov_index_left + 1 > len(self.img_moves_l):
                self.mov_index_left = 0
        elif self.animate == self.MOVE_R:
            self.image = self.img_moves[self.mov_index_right]
            self.mov_index_right += 1
            if self.mov_index_right + 1 > len(self.img_moves):
                self.mov_index_right = 0

    def update(self):
        x, y = self.rect.x, self.rect.y
        # self.vx, self.vy = self.vx, self.vy
        self.edge(x, y)

        # if self.vx > 0 or (self.vx == 0 and self.vy < 0):
        if self.vx > 0:
            self.animate = self.MOVE_R
            # self.image = self.img_moves[self.mov_index_right]
            # self.mov_index_right += 1
            # if self.mov_index_right + 1 > len(self.img_moves):
            #     self.mov_index_right = 0
        # elif self.vx < 0 or (self.vx == 0 and self.vy > 0):
        elif self.vx < 0:
            self.animate = self.MOVE_L
            # self.image = self.img_moves_l[self.mov_index_left]
            # self.mov_index_left += 1
            # if self.mov_index_left + 1 > len(self.img_moves_l):
            #     self.mov_index_left = 0
        self.avatar()
        self.rect = self.rect.move(self.vx, self.vy)


class Game:
    keys_arrow = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}

    def __init__(self, width=800, height=600, tick=30):
        init()
        self.width, self.height = width, height
        self.size = width, height
        self.screen: Surface = display.set_mode(self.size)

        self.tick = tick
        self.clock = time.Clock()

        self.keep_going = True

        self.bg: Surface = image.load('assets/img/bg2.png')
        self.crystal = scale(image.load('assets/img/crystal.png'), (50, 50))
        self.font = Font('assets/font/SourceHanSansSC-Normal.otf', 24)

        self.chr = image.load('assets/img/zero_scale2.png')
        self.chr_l = image.load('assets/img/zero_scale2_l.png')
        self.char = Char(self.chr, self.size)
        self.sprites = Group()
        self.sprites.add(self.char)

        self.gird = Gird(800 + 50, 600 + 50, 50, 50)
        self.gird.generate_row(7, 5)
        self.dots = []
        self.__new_point()
        self.pts = 0

        self.text: Surface = self.font.render('Points: ' + str(self.pts), True, (254, 185, 15))
        self.rect_text: Rect = self.text.get_rect()
        self.rect_text.x = self.width / 2 - self.rect_text.width / 2

    def on_key_press(self, key_event):
        if key_event.key in self.keys_arrow.keys():
            # self.velocity = multi_tuple(self.keys_arrow[e.key], 2)
            self.char.vx, self.char.vy = multi_tuple(self.keys_arrow[key_event.key], 2)
            # if self.char.vx > -1:
            #     self.char.image = self.chr
            # elif self.char.vx < -1:
            #     self.char.image = self.chr_l

    def event(self, events):
        for e in events:
            if e.type == KEYDOWN:
                self.on_key_press(e)

            elif e.type == QUIT:
                self.exit()

    def update(self):
        self.sprites.update()
        self.__collect()

    def __move(self):
        warn('use sprite update instead', DeprecationWarning)

        x, y = self.chr_xy.x, self.chr_xy.y
        vx, vy = self.velocity

        if x < 0 and vx < 0:
            self.velocity[0] = 0
        elif x > self.width - 72 and vx > 0:
            self.velocity[0] = 0

        if y < 0 and vy < 0:
            self.velocity[1] = 0
        elif y > self.height - 108 and vy > 0:
            self.velocity[1] = 0

        self.chr_xy = self.chr_xy.move(self.velocity)

    def __new_point(self):
        self.dots.append(choice(self.gird.points()))

    def on_collect(self, i):
        # if (i + 1) % 5 == 0:
        #     return
        pt = choice(self.gird.points())
        smile = QSprite(scale(image.load('assets/img/slime_2.png'), (70, 49)), self.size)
        x, y = pt
        smile.set_pos(x, y, QSprite.MID)
        self.sprites.add(smile)

    def __collect(self):
        r = 50

        px, py = self.char.get_pos(Char.MID)
        for pt in self.dots:
            x, y = pt
            if abs(px - x) < r and abs(py - y) < r and \
                    distance(pt, (px, py)) < r:
                self.dots.remove(pt)
                self.__new_point()
                self.pts += 1
                self.set_point_text(self.pts)
                self.on_collect(self.pts)

    def set_point_text(self, point: int):
        self.text: Surface = self.font.render('Points: ' + str(point), True, (254, 185, 15))
        self.rect_text: Rect = self.text.get_rect()
        self.rect_text.x = self.width / 2 - self.rect_text.width / 2

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for pt in self.dots:
            self.screen.blit(self.crystal, pt)
        self.sprites.draw(self.screen)

        self.screen.blit(self.text, self.rect_text)
        display.flip()

    def mainloop(self):
        while self.keep_going:
            self.update()
            self.draw()
            self.clock.tick(self.tick)
            self.event(event.get())

    def exit(self):
        print('Bye!')
        self.keep_going = False
        quit()


if __name__ == '__main__':
    game = Game(tick=60)
    game.mainloop()
