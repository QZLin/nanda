from math import sqrt
from timeit import timeit

from pygame import Vector2
from Vector2D import Vector2D


def v2_tuple():
    pos = [6879, 4859]
    for x in range(645):
        pos[0] = x
        pos[1] = x // 2
        # pos[0] *= 2


def v2_pygame():
    pos = Vector2()
    pos.x = 6879
    pos.y = 4859
    for x in range(645):
        pos.x = x
        pos.y = x // 2
        # pos.x *= 2


def v2_vector2d():
    pos = Vector2D()
    pos.x = 6879
    pos.y = 4859
    for x in range(645):
        pos.x = x
        pos.y = x // 2
        # pos.x *= 2


def multi_tuple():
    pos = [6879, 4859]
    for x in range(50):
        # pos = [i * x for i in pos]
        pos[0], pos[1] = pos[0] * x, pos[1] * x


def multi_tuple2():
    pos = Vector2()
    pos.x, pos.y = 6879, 4859
    for x in range(50):
        pos *= x


def multi_tuple3():
    pos = Vector2D()
    pos.x, pos.y = 6879, 4859
    for x in range(50):
        pos *= x


r1, r2, r3 = timeit(v2_tuple, number=1000), timeit(v2_pygame, number=1000), timeit(v2_vector2d, number=1000)
r5, r6, r7 = timeit(multi_tuple, number=1000), timeit(multi_tuple2, number=1000), timeit(multi_tuple3, number=1000)
print(r1, r2, r3)
print(r5, r6, r7)
