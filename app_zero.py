from math import sqrt

from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import Surface
from pygame import init, image, display, quit, event, time
from pygame.draw import circle
from pygame.rect import RectType
from pygame.transform import scale


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
        # print(pts)
        return self.pts


class Game:
    keys_arrow = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}

    def __init__(self, width=800, height=600, tick=30):
        init()
        self.width = width
        self.height = height
        self.size = width, height
        self.screen: Surface = display.set_mode(self.size)

        self.tick = tick
        self.clock = time.Clock()

        self.keep_going = True
        ###
        self.bg = image.load('img/bg1.png')

        self.chr = image.load('img/zero.png')
        self.chr = scale(self.chr, (72, 108))
        self.chr_xy: RectType = self.chr.get_rect()
        self.chr_xy.x, self.chr_xy.y = 1, 1

        self.velocity = [3, 3]
        self.gird = Gird(800 + 50, 600 + 50, 50, 50)
        self.gird.generate_row(7, 5)
        self.dots = self.gird.points()

    def __event(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key in self.keys_arrow.keys():
                    self.velocity = [x * 3 for x in self.keys_arrow[e.key]]

            elif e.type == QUIT:
                self.exit()

    def update(self):
        self.__move()
        self.__collect()

    def __move(self):
        # self.ball_rect: RectType
        x, y = self.chr_xy.x, self.chr_xy.y
        # print(x, y)
        if x < 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        elif x > self.width - 72 and self.velocity[0] > 0:
            self.velocity[0] = 0

        if y < 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        elif y > self.height - 108 and self.velocity[1] > 0:
            self.velocity[1] = 0

        self.chr_xy = self.chr_xy.move(self.velocity)

    def __collect(self):
        for pt in self.dots:
            px, py = self.chr_xy.x, self.chr_xy.y
            x, y = pt
            if abs(px - x) < 100 and abs(py - y) < 100:
                if distance(pt, (self.chr_xy.x + 40, self.chr_xy.y + 64)) < 50:
                    self.dots.remove(pt)

    def __draw(self):
        # self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        for pt in self.dots:
            circle(self.screen, (255, 0, 0), pt, 10)

        self.screen.blit(self.chr, self.chr_xy)
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
