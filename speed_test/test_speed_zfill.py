from timeit import timeit


def fill1():
    for i in range(999):
        y = '0' * (5 - len(str(i))) + str(i) + '.png'
        # print(y)


def fill2():
    for i in range(999):
        i = str(i)
        y = i.zfill(5) + '.png'
        # print(y)


# fill1()
# fill2()

r1, r2 = timeit(fill1, number=1000), timeit(fill2, number=1000)
print(r1, r2)
