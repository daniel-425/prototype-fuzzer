import threading
import socket

'''
This will open up local ports to then translate the fuzzing data to direct hardware IO.
'''
INTERFACE_WPORT_1 = 1001
INTERFACE_WPORT_2 = 1002
INTERFACE_WPORT_3 = 1003

RELAY_PORT = 1111

INTERFACE_DEVICE_IP = ""
LOCAL_INTERFACE = "127.0.0.1"

def relay():
    print("Starting Relay")

    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LOCAL_INTERFACE, RELAY_PORT))
    data_raw, addr = sock_in.recvfrom(65535)

    # Parse the data. Format will be a string of the sequence. i.e. 2:2:2:2:2:2:2:2:2:2
    print("Relay Recv: {0}".format(data_raw))

    split_data = data_raw.split(':')

    list_of_integers = list(map(int, split_data))
    
    # Iterate through the list pressing the correct button
    for iter in list_of_integers: 
        if iter == 1:
            button_port = INTERFACE_WPORT_1
        elif iter == 2:
            button_port = INTERFACE_WPORT_2
        elif iter == 3: 
            button_port = INTERFACE_WPORT_3
        else: 
            raise Exception("ERROR UNKNOWN BUTTON")

        sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_out.sendto("1", (INTERFACE_DEVICE_IP, button_port))

if __name__ == "__main__":
    relay()