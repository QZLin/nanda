from pygame import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
from pygame import Surface
from pygame import init, image, display, quit, event, time
from pygame.event import EventType
from pygame.rect import RectType


class App:
    keys_arrow = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}

    def __init__(self, width=800, height=600, tick=30):
        init()
        self.size = width, height
        self.screen: Surface = display.set_mode(self.size)

        self.tick = tick
        self.clock = time.Clock()

        ###

        self.ball = image.load('img/zero.png')
        self.ball_rect: RectType = self.ball.get_rect()

        self.velocity = 3, 3

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.ball, self.ball_rect)
        display.flip()

    def update(self):
        self.ball_rect = self.ball_rect.move(self.velocity)

    @staticmethod
    def exit():
        print('Bye!')
        quit()
        exit()

    def mainloop(self):
        while True:
            self.clock.tick(self.tick)
            for e in event.get():
                e: EventType
                if e.type == KEYDOWN:
                    if e.key in self.keys_arrow.keys():
                        self.velocity = self.keys_arrow[e.key]

                elif e.type == QUIT:
                    self.exit()

            self.update()
            self.draw()


app = App(tick=60)
app.mainloop()
