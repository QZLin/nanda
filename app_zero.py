from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import Surface
from pygame import init, image, display, quit, event, time
from pygame.event import EventType
from pygame.rect import RectType
from pygame.transform import scale


class App:
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

        self.ball = image.load('img/zero.png')
        self.ball = scale(self.ball, (72, 108))
        self.ball_rect: RectType = self.ball.get_rect()
        self.ball_rect.x, self.ball_rect.y = 1, 1

        self.velocity = [3, 3]

    def event_handler(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key in self.keys_arrow.keys():
                    self.velocity = [x * 3 for x in self.keys_arrow[e.key]]

            elif e.type == QUIT:
                self.exit()

    def update(self):
        # self.ball_rect: RectType
        x, y = self.ball_rect.x, self.ball_rect.y
        print(x, y)
        if x < 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        elif x > self.width - 72 and self.velocity[0] > 0:
            self.velocity[0] = 0

        if y < 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        elif y > self.height - 108 and self.velocity[1] > 0:
            self.velocity[1] = 0

        self.ball_rect = self.ball_rect.move(self.velocity)

    def draw(self):
        # self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.ball, self.ball_rect)
        display.flip()

    def mainloop(self):
        while self.keep_going:
            self.update()
            self.draw()
            self.clock.tick(self.tick)
            self.event_handler(event.get())

    def exit(self):
        print('Bye!')
        self.keep_going = False
        quit()


app = App(tick=60)
app.mainloop()
