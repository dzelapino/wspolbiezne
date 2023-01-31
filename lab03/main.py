import os
import sys
from multiprocessing import Process, Queue


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def readFile(f, word, q):
    info('function readFile')
    file = open(f, "r")
    inputInstruction = "\input"
    for line in file:
        q.put(line.count(word))
        if inputInstruction in line:
            fileName = line.split("{")[1].split("}")[0]
            process = Process(target=readFile, args=(fileName, word, q))
            process.start()
            process.join()
        else:
            print(line)
    file.close()


if __name__ == '__main__':
    system_arguments = sys.argv
    p = system_arguments[1]
    s = system_arguments[2]
    desired_file = p + ".txt"

    queue = Queue()

    process_start = Process(target=readFile, args=(desired_file, s, queue))
    process_start.start()
    process_start.join()
    words_found = 0
    while queue.empty() is False:
        print(queue.get())
        words_found = words_found + queue.get()
    print(words_found)
