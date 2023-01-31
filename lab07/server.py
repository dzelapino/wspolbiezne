import socket
import struct
from enum import Enum


class Action(Enum):
    End = 0
    Rock = 1
    Paper = 2
    Scissors = 3


def game(input1, input2):
    if input1 == input2:
        return [0, 0]
    elif input1 == 1 and input2 == 2:
        return [0, 1]
    elif input1 == 1 and input2 == 3:
        return [1, 0]
    elif input1 == 2 and input2 == 1:
        return [1, 0]
    elif input1 == 2 and input2 == 3:
        return [0, 1]
    elif input1 == 3 and input2 == 2:
        return [1, 0]
    elif input1 == 3 and input2 == 1:
        return [0, 1]


IP = "127.0.0.1"
port = 5001
bufSize = 1024

UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDPServerSocket.bind((IP, port))

client_scores = {}
print("serwer UDP działa")

while True:

    # Gracz 1
    client_message_pack1, client1_adress = UDPServerSocket.recvfrom(bufSize)
    client_message1 = struct.unpack('!i', client_message_pack1)
    client1_choice = client_message1[0]

    # Gracz 2
    client_message_pack2, client2_adress = UDPServerSocket.recvfrom(bufSize)
    client_message2 = struct.unpack('!i', client_message_pack2)
    client2_choice = client_message2[0]

    if int(client1_choice) == 0 or int(client2_choice) == 0:
        client1_odp = struct.pack('!i', -1)
        client2_odp = struct.pack('!i', -1)
        UDPServerSocket.sendto(client1_odp, client1_adress)
        UDPServerSocket.sendto(client2_odp, client2_adress)
        if int(client1_choice) == 0:
            client_scores.pop(client1_adress)
        if int(client2_choice) == 0:
            client_scores.pop(client2_adress)

    else:
        # gra
        if client1_adress not in client_scores:
            client_scores.update({client1_adress: 0})

        if client2_adress not in client_scores:
            client_scores.update({client2_adress: 0})

        current_score = game(int(client1_choice), int(client2_choice))
        client_scores[client1_adress] = client_scores[client1_adress] + current_score[0]
        client_scores[client2_adress] = client_scores[client2_adress] + current_score[1]
        # wysyłanie odpowiedzi
        client1_odp = struct.pack('!i', int(client_scores[client1_adress]))
        client2_odp = struct.pack('!i', int(client_scores[client2_adress]))
        UDPServerSocket.sendto(client1_odp, client1_adress)
        UDPServerSocket.sendto(client2_odp, client2_adress)

        print(client_scores)
