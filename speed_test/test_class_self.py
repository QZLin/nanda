from math import sqrt
from timeit import timeit

from pygame import image
from pygame.rect import Rect, RectType


class TestClass:
    def __init__(self):
        self.value = 68574654
        self.v1, self.v2, self.v3 = 45645, 56464, 68934
        img = image.load('../assets/img/zero.png')
        self.rect = img.get_rect()
        self.rect.x = 545
        self.rect.y = 284

    def test_method1(self):
        for i in range(50):
            v = self.v1 * i / self.v2 + sqrt(self.v3)

    def test_method2(self):
        v1, v2, v3 = self.v1, self.v2, self.v3
        for i in range(50):
            v = v1 * i / v2 + sqrt(v3)

    def t1(self):
        for i in range(50):
            v = self.rect.x * i / self.rect.y + sqrt(self.rect.x)

    def t2(self):
        v1, v2, v3 = self.rect.x, self.rect.y, self.rect.x
        for i in range(50):
            v = v1 * i / v2 + sqrt(v3)


test = TestClass()
r1, r2 = timeit(test.test_method1, number=1000), timeit(test.test_method2, number=1000)
r3, r4 = timeit(test.t1, number=1000), timeit(test.t2, number=1000)
print(r1, r2)
print(r3, r4)
