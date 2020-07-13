from math import sqrt
from random import choice

from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import init, image, display, quit, event, time
from pygame.sprite import Sprite, Group
from pygame.transform import scale
# Type Mark
from pygame.rect import Rect
from pygame import Surface


def distance(x_y1, x_y2):
    x1, y1 = x_y1
    x2, y2 = x_y2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Gird:
    def __init__(self, xe, ye, xs=0, ys=0):
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


class Char(Sprite):
    ZERO = 0
    MID = 1

    def __init__(self, img, border_size, *groups, vx=0, vy=0):
        self.image: Surface = img
        self.screen_x, self.screen_y = border_size

        self.rect: Rect = self.image.get_rect()
        self.pixel_xy = self.image.get_width(), self.image.get_height()
        # self.pos = [self.rect.x, self.rect.y]
        self.vx, self.vy = vx, vy

        super().__init__(*groups)

    def set_pos(self, x, y, pos_type=ZERO):
        if pos_type == self.ZERO:
            # self.pos = [x, y]
            self.rect.x, self.rect.y = x, y
        elif pos_type == self.MID:
            self.rect.x = x - self.pixel_xy[0]
            self.rect.y = y - self.pixel_xy[1]

    def update(self):
        x, y = self.rect.x, self.rect.y
        vx, vy = self.vx, self.vy
        # print(x, y)
        if x < 0 and vx < 0:
            self.vx = 0
        elif x > self.screen_x - 72 and vx > 0:
            self.vx = 0

        if y < 0 and vy < 0:
            self.vy = 0
        elif y > self.screen_y - 108 and vy > 0:
            self.vy = 0

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
        ###
        self.bg: Surface = image.load('img/bg1.png')
        self.crystal = scale(image.load('img/crystal.png'), (50, 50))

        self.chr = image.load('img/zero.png')
        self.char = Char(scale(self.chr, (72, 108)), self.size)
        self.sprites = Group()
        self.sprites.add(self.char)

        self.chr = scale(self.chr, (72, 108))
        self.chr_xy: Rect = self.chr.get_rect()
        self.chr_xy.x, self.chr_xy.y = 1, 1

        self.velocity = [3, 3]
        self.gird = Gird(800 + 50, 600 + 50, 50, 50)
        self.gird.generate_row(7, 5)
        self.dots = []
        self.__new_point()
        # self.dots = self.gird.points()

    def __event(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key in self.keys_arrow.keys():
                    self.velocity = [x * 3 for x in self.keys_arrow[e.key]]
                    self.char.vx, self.char.vy = [x * 3 for x in self.keys_arrow[e.key]]

            elif e.type == QUIT:
                self.exit()

    def update(self):
        self.sprites.update()
        self.__move()
        self.__collect()

    def __move(self):
        # self.ball_rect: RectType
        x, y = self.chr_xy.x, self.chr_xy.y
        vx, vy = self.velocity
        # print(x, y)
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

    def __collect(self):
        r = 50
        # px, py = self.chr_xy.x, self.chr_xy.y
        px, py = self.char.rect.x, self.char.rect.y
        for pt in self.dots:
            x, y = pt
            if abs(px - x) < r and abs(py - y) < r and \
                    distance(pt, (self.chr_xy.x + 40, self.chr_xy.y + 64)) < r:
                self.dots.remove(pt)
                self.__new_point()

    def __draw(self):
        self.screen.blit(self.bg, (0, 0))

        for pt in self.dots:
            self.screen.blit(self.crystal, pt)
            # circle(self.screen, (255, 0, 0), pt, 10)

        self.sprites.draw(self.screen)
        # self.screen.blit(self.chr, self.chr_xy)
        display.flip()

    def mainloop(self):
        while self.keep_going:
            self.update()
            self.__draw()
            self.clock.tick(self.tick)
            self.__event(event.get())

    def exit(self):
        print('Bye!')
        self.keep_going = False
        quit()


if __name__ == '__main__':
    game = Game(tick=60)
    game.mainloop()
