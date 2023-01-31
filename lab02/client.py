import errno
import os
import sys
import time


def read_file_name():
    system_arguments = sys.argv
    if len(system_arguments) > 1:
        file_name = system_arguments[1]
        print(file_name)
        return file_name
    return "no_name"


client_file_name = read_file_name() + ".txt"
f = open(client_file_name, "w")
print("Insert text (Client): ")
f.write(str(input()))
f.write(chr(27))
f.close()


while True:
    try:
        lockfile = os.open("lockFile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        os.system("clear")
        print("Loading...")
        time.sleep(0.05)

server_buffer = open("buffer.txt", "w")
server_buffer.write(client_file_name + "\n")
server_buffer.close()

while True:
    if os.path.exists(client_file_name) and os.path.exists("temp" + client_file_name):
        answer = open(client_file_name, "r")
        print("Received message from server: ")
        print(answer.readlines())
        answer.close()
        os.remove(client_file_name)
        os.remove("temp" + client_file_name)
        break
    else:
        time.sleep(0.05)
