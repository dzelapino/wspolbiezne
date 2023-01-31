import os
import errno
import time

db = {
    0: "Rom",
    1: "Kel",
    2: "Ler",
    3: "Kash",
    4: "Dojo",
    5: "Pavlo"
}

FIFO = 'server_queue'

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

fifo_in = os.open(FIFO, os.O_RDONLY)

fifo_out1 = os.open(FIFO, os.O_WRONLY | os.O_NDELAY)

while True:
    r = os.read(fifo_in, 38)  # 36 bajtów - uuid + / + id
    if len(r) > 0:
        client_request = r.decode()
        client_split = client_request.split("/")
        request_queue = client_split[0]
        request_id = client_split[1]

        message_to_send = "Nie ma"

        if int(request_id) in db:
            message_to_send = db[int(request_id)]

        fifo_out = os.open(request_queue, os.O_WRONLY)
        os.write(fifo_out, message_to_send.encode())
        print("Żądanie od klienta: %s" % r.decode())
    else:
        print("Koniec żądania klienta")
        break
    time.sleep(2)
