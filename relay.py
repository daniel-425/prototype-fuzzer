import threading
import socket

'''
This will open up local ports to then translate the fuzzing data to direct hardware IO.
'''
INTERFACE_WPORT_1 = 1001
INTERFACE_WPORT_2 = 1002
INTERFACE_WPORT_3 = 1003

INTERFACE_DEVICE_IP = ""
LOCAL_INTERFACE = "127.0.0.1"

def relay_wprobe_one():
    while True:
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind((LOCAL_INTERFACE, INTERFACE_WPORT_1))
        data_raw, addr = sock_in.recvfrom(5)

        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out.sendto(data_raw, (INTERFACE_DEVICE_IP, INTERFACE_WPORT_1))

def relay_wprobe_two():
    while True:
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind((LOCAL_INTERFACE, INTERFACE_WPORT_2))
        data_raw, addr = sock_in.recvfrom(5)

        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out.sendto(data_raw, (INTERFACE_DEVICE_IP, INTERFACE_WPORT_2))

def relay_wprobe_three():
    while True:
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_in.bind((LOCAL_INTERFACE, INTERFACE_WPORT_3))
        data_raw, addr = sock_in.recvfrom(5)

        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out.sendto(data_raw, (INTERFACE_DEVICE_IP, INTERFACE_WPORT_3))

def relay():
    print("Starting Relay")

    probe_relay_one = threading.Thread(target=relay_wprobe_one)
    probe_relay_one.start()

    probe_relay_two = threading.Thread(target=relay_wprobe_two)
    probe_relay_two.start()

    probe_relay_three = threading.Thread(target=relay_wprobe_three)
    probe_relay_three.start()

if __name__ == "__main__":
    relay()