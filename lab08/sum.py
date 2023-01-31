import threading
import random
import math
import sys

sys.setrecursionlimit(10 ** 9)
MAX_THREADS = 3
threads = {}
lockFirst = threading.Lock()

result = []

# array = [1, 1, 1, 2, 2, 2, 3, 3, 3, 3]
MAX = 1000
array = []
for i in range(0, MAX):
    x = random.randint(1, MAX)
    array.append(x)


def sumArray(arr):
    global result
    local_result = [sum(arr)]
    with lockFirst:
        result += local_result


x = 0
while x < MAX_THREADS:
    arr_start = x * int(len(array) / MAX_THREADS)
    if x == MAX_THREADS - 1:
        arr_end = len(array)
    else:  # else sluzy aby upewnic sie ze cala tablica bedzie przeiterowana
        arr_end = arr_start + int(len(array) / MAX_THREADS)
    arr_local = array[arr_start:arr_end]
    threads[x] = threading.Thread(target=sumArray, args=[arr_local])
    # print(threads[x])
    x = x + 1

# print(threads)

x = 0
while x < MAX_THREADS:
    threads[x].start()
    # print(threads[x])
    x = x + 1

x = 0
while x < MAX_THREADS:
    threads[x].join()
    # print(threads[x])
    x = x + 1

# print(result)
print(sum(result))
