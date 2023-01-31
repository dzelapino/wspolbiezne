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
    for p in mlp:
        if k % p == 0:
            return False
        if p * p > k:
            return True
    return True


def licz(left, inc, max, queue_mlp, queue_first, queue_time):
    start = time.time()
    # print("licz od do")
    # print(left)
    right = left + inc
    # print(right)
    mlp = []
    while queue_mlp.empty() is False:
        mlp.append(queue_mlp.get())
    s = math.ceil(math.sqrt(right))
    for i in range(2, s + 1):
        if pierwsza(i):
            mlp.append(i)
            queue_mlp.put(i)
    for i in range(left, right + 1):
        if pierwsza1(i, mlp):
            queue_first.put(i)
    queue_time.put(time.time() - start)
    if left < max - inc:
        process = Process(target=licz, args=(right, inc, max, queue_mlp, queue_first, queue_time))
        process.start()
        process.join()
    else:
        # print(mlp)
        q_time = 0
        while queue_time.empty() is False:
            # print(queue_time.get())
            q_time = q_time + queue_time.get()
            print(q_time)


#  print(pierwsze)


if __name__ == '__main__':
    print(l, r)
    # start = time.time()
    # licz(l, r)
    # print(time.time() - start)

    queue_mlp = Queue()
    queue_first = Queue()
    queue_time = Queue()
    # start = time.time()
    process_start = Process(target=licz, args=(l, 100000, r, queue_mlp, queue_first, queue_time))
    process_start.start()
    process_start.join()
    # print(time.time() - start)

    # while queue.empty() is False:
    #     print(queue.get())
    #     words_found = words_found + queue.get()
    # print(words_found)
