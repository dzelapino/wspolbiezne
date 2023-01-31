import os
import sysv_ipc

key_in = 6
key_out = 9

to_translate = input("Translate: ")
pid = os.getpid()

in_queue = sysv_ipc.MessageQueue(key_in, sysv_ipc.IPC_CREAT)

in_queue.send(to_translate.encode(), True, pid)

out_queue = sysv_ipc.MessageQueue(key_out, sysv_ipc.IPC_CREAT)

while True:
    message = None
    try:
        message, client_pid = out_queue.receive(True, pid)
    except sysv_ipc.BusyError:
        print("Server busy")
    if message:
        print("Received: " + message.decode())
    break
