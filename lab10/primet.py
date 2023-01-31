import time
import math
from multiprocessing import Process, Queue

l = 1000000
r = 2000000


def pierwsza(k):
    # sprawdzenie, czy k jest pierwsza
    for i in range(2, k - 1):
        if i * i > k:
            return True
        if k % i == 0:
            return False
    return True


def pierwsza1(k, mlp):
    # sprawdzenie, czy k jest pierwsza
    # korzystając z zestawu małych liczb pierwszych mlp
    for p in mlp:
        if k % p == 0:
            return False
        if p * p > k:
            return True
    return True


def licz(l, r):
    # tworzenie listy małych liczb pierwszych
    mlp = []
    s = math.ceil(math.sqrt(r))
    for i in range(2, s + 1):
        if pierwsza(i):
            mlp.append(i)
    #  print(mlp)
    # tworzenie właściwej listy liczb pierwszych
    pierwsze = []
    for i in range(l, r + 1):
        if pierwsza1(i, mlp):
            pierwsze.append(i)
    # print(pierwsze)


#  print(pierwsze)


if __name__ == '__main__':
    print(l, r)
    start = time.time()
    licz(l, r)
    print(time.time() - start)
