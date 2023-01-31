import os
import uuid
import time
import errno

FIFO_Server = 'server_queue'

client_input = input()[0]

client_id = str(uuid.uuid4())

FIFO_Client = client_id
client_message = client_id + '/' + client_input

fifo_out = os.open(FIFO_Server, os.O_WRONLY)
os.write(fifo_out, client_message.encode())

try:
    os.mkfifo(FIFO_Client)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

fifo_in = os.open(FIFO_Client, os.O_RDONLY)

while True:
    r = os.read(fifo_in, 20)
    if len(r) > 0:
        print("Odpowiedź od serwera: %s" % r.decode())
        break
    else:
        print("Serwer odesłał odpowiedź")
        break
