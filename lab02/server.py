import os
import time


def read_file(filename):
    f = open(filename, "r")
    print(f.readlines())
    f.close()


def write_file(filename, buffer_used):
    f = open(filename, "a")
    print("Insert text (Server): ")
    f.write(str(input()))
    f.write(chr(27))
    f.close()
    buffer_used.truncate(0)
    buffer_used.close()


buffer = "buffer.txt"
if not os.path.exists(buffer):
    b = open(buffer, "x")
    b.close()

while True:
    if os.path.getsize(buffer) > 0:
        b = open(buffer, "r+")
        client_file = b.readline().strip()
        print("Received message from client: ")
        read_file(client_file)
        write_file(client_file, b)
        open("temp" + client_file, "x")
        os.system("clear")
        if os.path.exists("lockFile"):
            os.remove("lockFile")
    else:
        if os.path.exists("lockfile"):
            os.remove("lockfile")
        time.sleep(0.05)
