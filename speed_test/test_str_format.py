from timeit import timeit


def str0():
    for i in range(999):
        y = 'assets/img/zero_move/%s.png' % str(i).zfill(5)


def str1():
    for i in range(999):
        y = 'assets/img/zero_move/' + str(i).zfill(5) + '.png'
        # print(y)


# fill1()
# fill2()

r1, r2 = timeit(str0, number=1000), timeit(str1, number=1000)
print(r1, r2)
