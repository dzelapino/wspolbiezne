import threading
import sys
import time

sys.setrecursionlimit(10 ** 9)
MAX_THREADS = 3
threads = {}
lockFirst = threading.Lock()

result = []

MAX = 100
array = []
for i in range(2, MAX):
    array.append(i)


def find_first(arr, bar):
    global result
    local_result = []
    for number in arr:
        if is_first(number):
            local_result.append(number)
    # print("koniec pracy watku")
    # print(result)
    with lockFirst:
        result += local_result
    print("koniec pracy watku")
    bar.wait()
    # print(result)
    print("koniec czekania watku")


def is_first(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    first = int(n**0.5) + 1
    for divider in range(3, first, 2):
        if n % divider == 0:
            return False
    return True


b = threading.Barrier(MAX_THREADS + 1)
x = 0
while x < MAX_THREADS:
    arr_start = x * int(len(array) / MAX_THREADS)
    if x == MAX_THREADS - 1:
        arr_end = len(array)
    else:  # else sluzy aby upewnic sie ze cala tablica bedzie przeiterowana
        arr_end = arr_start + int(len(array) / MAX_THREADS)
    arr_local = array[arr_start:arr_end]
    threads[x] = threading.Thread(target=find_first, args=(arr_local, b))
    # print(threads[x])
    x = x + 1

# print(threads)

x = 0
while x < MAX_THREADS:
    threads[x].start()
    # print(threads[x])
    x = x + 1


b.wait()
print(result)


# x = 0
# while x < MAX_THREADS:
#     threads[x].join()
#     # print(threads[x])
#     x = x + 1

# print(result)
