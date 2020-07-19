from math import hypot, sqrt
from timeit import timeit


def func1():
    for x in range(99):
        y = hypot(x, x + 1)
    # print(y)


def func2():
    for x in range(99):
        y = sqrt(x ** 2 + (x + 1) ** 2)
    # print(y)


func1()
func2()

r1, r2 = timeit(func1, number=1000), timeit(func2, number=1000)
print(r1, r2)
