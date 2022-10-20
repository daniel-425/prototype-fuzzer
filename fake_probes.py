import threading
import socket

LOCAL_INTERFACE = "127.0.0.1"
LISTEN_PORT = 2001
SEND_PORT = 1001

def recieve_fake_probe():
    while True:
        global RPROBE_DATA
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LOCAL_INTERFACE, LISTEN_PORT))
        data_raw, addr = sock.recvfrom(5)
        print("Probe: {0}".format(data_raw))

def send_fake_probe():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"1", (LOCAL_INTERFACE, SEND_PORT))

listen_UDP = threading.Thread(target=recieve_fake_probe)
listen_UDP.start()

send_UDP = threading.Thread(target=send_fake_probe)
send_UDP.start()

while True:
    continue