from timeit import timeit


def func1():
    for x in range(99):
        pass


def func2():
    for x in range(99):
        pass


# func1()
# func2()

r1, r2 = timeit(func1, number=1000), timeit(func2, number=1000)
print(r1, r2)
