import threading
import socket
from threading import Lock

LOCAL_INTERFACE = "192.168.7.5"
LISTEN_PORT = 2001
SEND_PORT = 1001
RPROBE_DATA = 3
WPROBE_DATA = b"1"
COUNTER = 0

def recieve_fake_probe():
    global RPROBE_DATA
    global COUNTER
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LOCAL_INTERFACE, LISTEN_PORT))
        data_raw, addr = sock.recvfrom(5)

        if data_raw ==  b"\x00":
            RPROBE_DATA = 0
        elif data_raw == b"\x01":
            RPROBE_DATA = 1
        else:
            RPROBE_DATA = 3

        COUNTER += 1

        print("Probe: {0}. Count: {1}".format(RPROBE_DATA, COUNTER))

def send_fake_probe():
    global COUNTER
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if COUNTER == 20:
            sock.sendto(b"0", (LOCAL_INTERFACE, SEND_PORT))
        else:
            sock.sendto(b"1", (LOCAL_INTERFACE, SEND_PORT))

listen_UDP = threading.Thread(target=recieve_fake_probe)
listen_UDP.start()

#send_UDP = threading.Thread(target=send_fake_probe)
#send_UDP.start()

while True:
    continue