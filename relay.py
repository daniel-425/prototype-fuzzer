import threading
import socket

'''
This will open up local ports to then translate the fuzzing data to direct hardware IO.
'''
INTERFACE_WPORT_1 = 1001
INTERFACE_WPORT_2 = 1002
INTERFACE_WPORT_3 = 1003

RELAY_PORT = 1111
INTERFACE_DEVICE_IP = "192.168.7.100"
LOCAL_INTERFACE = "127.0.0.1"

def relay():
    print("Starting Relay")

    while True:
        sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_in.bind((LOCAL_INTERFACE, RELAY_PORT))

        sock_in.listen()

        conn, addr = sock_in.accept()
        with conn:
            print("Connected by {0}".format(addr))
            data_raw = conn.recv(1024)

        # Parse the data. Format will be a string of the sequence. i.e. 2:2:2:2:2:2:2:2:2:2
        print("Relay Recv: {0}".format(data_raw))

        split_data = data_raw.split(b':')

        list_of_integers = list(map(int, split_data))

        print("Order: {0}".format(list_of_integers))
        
        # Iterate through the list pressing the correct button
        for iter in list_of_integers: 
            if iter == 2:
                button_port = INTERFACE_WPORT_1
            elif iter == 3:
                button_port = INTERFACE_WPORT_2
            elif iter == 4: 
                button_port = INTERFACE_WPORT_3
            else: 
                raise Exception("ERROR UNKNOWN BUTTON")

            #sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock_out.sendto("1", (INTERFACE_DEVICE_IP, button_port))

if __name__ == "__main__":
    relay()