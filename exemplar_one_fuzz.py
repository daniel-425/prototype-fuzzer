from ast import Global
from shutil import ExecError
import socket
from boofuzz import *
import threading
import time

LOCAL_INTERFACE = "192.168.7.5"
INTERFACE_IP = "192.168.7.100"

TARGET_IP = "192.168.8.150"

TARGET_PORT = 1234
INTERFACE_RPORT_1 = 2001
INTERFACE_WPORT_1 = 1001
INTERFACE_WPORT_2 = 1002
INTERFACE_WPORT_3 = 1003
SLEEP_TIME = 1 

RPROBE_1_DATA = 3

# A thread that will listen on the probe socket and put into rprobedata
def recieve_read_probe_one():
    while True:
        global RPROBE_1_DATA
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LOCAL_INTERFACE, INTERFACE_RPORT_1))
        data_raw, addr = sock.recvfrom(5)

        '''test
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"0", (INTERFACE_IP, INTERFACE_WPORT_1))
        sock.sendto(b"1", (INTERFACE_IP, INTERFACE_WPORT_2))
        sock.sendto(b"0", (INTERFACE_IP, INTERFACE_WPORT_3))
        '''

        try:
            if data_raw == b"\x00":
                RPROBE_1_DATA = 0
            elif data_raw == b"\x01":
                RPROBE_1_DATA = 1
            else:
                RPROBE_1_DATA = 3
            
            #print("RPROBE DATA 1: {0}".format(RPROBE_1_DATA))
        except Exception:
            print("WARNING COULDNT CONVERT DATA")


class voltage_monitor(BaseMonitor):
    def alive():
        # This is run at the start to see if the target is alive. 
        print("Voltage Monitor checking if alive")
        return True

    def pre_send(target=None, fuzz_data_logger=None, session=None):
        print("Executing presend")
        '''
        This should be the socket connection to enable the vulnerable service through a 
        remote button push. Send a UDP Packet to the write interface probe
        '''

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"1", (INTERFACE_IP, INTERFACE_WPORT_1))
        
        return True

    def set_options(*args, **kwargs):
        return True

    def start_target():
        print("Starting target")
        return True
    
    def post_start_target(target=None, fuzz_data_logger=None, session=None):
        print("Post start target")
        return True

    def post_send(target=None, fuzz_data_logger=None, session=None):
        print("Post Send")
        # Retrun True here if no crash. False if there is a crash. 
        # Read the global rdataprobe to see if there is a crash 

        time.sleep(1.5)

        print("RPROBEDATA: {0}".format(RPROBE_1_DATA))

        if RPROBE_1_DATA == 0:
            return False
        elif RPROBE_1_DATA == 1:
            return True
        else: 
            raise Exception("Unknown RPROBEDATA: {0}".format(RPROBE_1_DATA))
    
    def restart_target(target=None, fuzz_data_logger=None, session=None):
        print("Restart Target")
        return True

    def get_crash_synopsis():
        return True


def test_case_callback(target, fuzz_data_logger, session, *args, **kwargs):
    print("In test case callback")
    response = target.recv()

    print("Response: {0}".format(response))

    if response == b"REJECT":
        raise Exception("Target rejected our connection")


def execute_fuzzer():
    print("Fuzzing exemplar device 1")

    listen_UDP = threading.Thread(target=recieve_read_probe_one)
    listen_UDP.start()

    '''test
    while(True):
        continue
    '''

    # Create the requestself
    # The format will be {SIZE}:{DATA}. 
    req = Request("FUZZ_REQUEST",children=(
        Block("DATA", children=(
        String(name="length", default_value="0010", fuzzable=False),
        String(name="delim", default_value=":", fuzzable=False),
        FromFile(name="data", filename="test_case_files/test_one/regular_run.txt")
    ))))

    # Create the sessionData
    session = Session(
        target=Target(
            connection=TCPSocketConnection(TARGET_IP, TARGET_PORT),
            #monitors=[]),
            monitors=[voltage_monitor]),      
        sleep_time=SLEEP_TIME,
        crash_threshold_request=1)

    session.register_post_test_case_callback(test_case_callback)

    # Run the session 
    session.connect(req)
    session.fuzz()

    print("Completed Fuzzing run")

if __name__ == "__main__":
    execute_fuzzer()
