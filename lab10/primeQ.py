import os
import sys
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


def licz(l, inc, max, q):
    # tworzenie listy małych liczb pierwszych
    r = l + inc
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
    q.put(pierwsze)
    if l < max:
        process = Process(target=licz, args=(r, inc, max, q))
        process.start()
        process.join()
    else:
        print("dzia")
    # print(pierwsze)


#  print(pierwsze)


if __name__ == '__main__':
    print(l, r)
    queue = Queue()
    inc = (r - l) / 10
    start = time.time()
    process_start = Process(target=licz, args=(l, inc, r, queue))
    process_start.start()
    process_start.join()
    print(time.time() - start)

# def lookForPrimes(start, inc, max, q):
#     info('function readFile')
#     file = open(f, "r")
#     inputInstruction = "\input"
#     for line in file:
#         q.put(line.count(word))
#         if inputInstruction in line:
#             fileName = line.split("{")[1].split("}")[0]
#             process = Process(target=readFile, args=(fileName, word, q))
#             process.start()
#             process.join()
#         else:
#             print(line)
#     file.close()
#
#
# if __name__ == '__main__':
#     system_arguments = sys.argv
#     p = system_arguments[1]
#     s = system_arguments[2]
#     desired_file = p + ".txt"
#     start = l
#     max = r
#     inc = (r-l)/10
#
#     queue = Queue()
#
#     process_start = Process(target=readFile, args=(desired_file, s, queue))
#     process_start.start()
#     process_start.join()
#     # words_found = 0
#     # while queue.empty() is False:
#     #     print(queue.get())
#     #     words_found = words_found + queue.get()
#     # print(words_found)
