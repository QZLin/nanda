import sys

from pygame import Surface, KEYDOWN
from pygame import init, image, display, QUIT, quit, event, time
from pygame.rect import RectType

init()  # 初始化pygame

size = width, height = 640, 480  # 设置窗口大小
screen: Surface = display.set_mode(size)  # 显示窗口

color = (0, 0, 0)  # 设置颜色

ball = image.load('img/zero.png')  # 加载图片
ball_rect: RectType = ball.get_rect()  # 获取矩形区域

clock = time.Clock()

flag_direct_a = True
while True:  # 死循环确保窗口一直显示
    clock.tick(30)

    for e in event.get():  # 遍历所有事件
        if e.type == QUIT:  # 如果单击关闭窗口，则退出
            print('Bye!')
            quit()  # 退出pygame
            sys.exit()
        elif e.type == KEYDOWN:
            print('keydown')
            flag_direct_a = not flag_direct_a

    screen.fill(color)  # 填充颜色(设置为0，执不执行这行代码都一样)
    screen.blit(ball, ball_rect)  # 将图片画到窗口上
    display.flip()  # 更新全部显示

    if flag_direct_a:
        ball_rect = ball_rect.move(1, 1)
    else:
        ball_rect = ball_rect.move(-1, -1)

    if not (0 < ball_rect.x < 200 and 0 < ball_rect.y < 200):
        flag_direct_a = not flag_direct_a
