import signal
import sys
import time
import sysv_ipc


def handler(signum, frame):
    print('Signal handler', signum)


def handler_exit(signum, frame):
    print('Handling exit', signum)
    sys.exit(0)


dictionary = {
    "pies": "dog",
    "husky": "husky",
    "auto": "car",
    "bum": "boom"
}


signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGUSR1, handler_exit)

pid_max = 0

in_queue = 6
out_queue = 9

in_queue = sysv_ipc.MessageQueue(in_queue, sysv_ipc.IPC_CREAT)
out_queue = sysv_ipc.MessageQueue(out_queue, sysv_ipc.IPC_CREAT)


while True:
    time.sleep(5)
    message = None
    client_pid = None
    try:
        message, client_pid = in_queue.receive(False, type = pid_max)
    except sysv_ipc.BusyError:
        print("Working")
    if message and client_pid:
        result = dictionary.get(message.decode(), ": Word not found")
        out_queue.send(result.encode(), True, client_pid)
