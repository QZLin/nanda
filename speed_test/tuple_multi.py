from timeit import timeit


def fill1():
    tp = (45, 68)
    for i in range(999):
        o = []
        for x in tp:
            o.append(x * i)


def fill2():
    tp = (45, 68)
    for i in range(999):
        o = []
        for ix in range(len(tp)):
            o.append(tp[ix] * i)


def fill3():
    tp = (45, 68)
    for i in range(999):
        o = [x * i for x in tp]


# fill1()
# fill2()

r1, r2, r3 = timeit(fill1, number=1000), timeit(fill2, number=1000), timeit(fill3, number=1000)
print(r1, r2, r3)
