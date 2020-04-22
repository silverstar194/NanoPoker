import serial
import threading
import re
from .token_model import Token

def read_from_port(device, device_name):
    id = 0
    while True:
        try:
            id += 1
            device_bytes = device.readline()
            decoded_bytes = device_bytes[0:len(device_bytes)].decode("utf-8")

            if "Token" in decoded_bytes:
                match = re.search("Token: (.+)", decoded_bytes, re.IGNORECASE)
                token_name = match.group(1)
                print(device_name[-4:]+" "+token_name)
        except Exception as e:
            print(e)




device_one_name = '/dev/cu.usbserial-1440'
device_two_name = '/dev/cu.usbserial-1460'

device_one = serial.Serial(device_one_name)
device_two = serial.Serial(device_two_name)

thread_one = threading.Thread(target=read_from_port, args=(device_one, device_one_name, ))
thread_one.start()

thread_two = threading.Thread(target=read_from_port, args=(device_two,device_two_name, ))
thread_two.start()
