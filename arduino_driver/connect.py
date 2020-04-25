import serial
import threading
import re
import json

from websocket_wrapper import WebSocket
device_id_to_device_name = {'/dev/cu.usbserial-1450': "device_one", '/dev/cu.usbserial-1440': "device_two"}

nano_poker_ws = 'ws://127.0.0.1:8001/ws/message/action'

pot_device = '/dev/cu.usbserial-1450'
player_one_device = '/dev/cu.usbserial-1440'
player_two_device = ''

devices = [pot_device, player_one_device]

ws = WebSocket(nano_poker_ws)


def place_bid(device_name, token_name):
    data = {"message": {"application": "NanoPoker", "device": device_id_to_device_name[device_name], "token": token_name, "type": "bet"}}
    ws.send(json.dumps(data))


def cash_out(device_name, token_name):
    data = {"message": {"application": "NanoPoker", "device": device_id_to_device_name[device_name], "token": token_name, "type": "cash_out"}}
    ws.send(json.dumps(data))


def execute_event(device, token):
    if device == pot_device:
        cash_out(device, token)

    elif device in [player_one_device]:
        place_bid(device, token)

    else:
        raise Exception("Device not registered")


def read_from_port(device, device_name):
    id = 0
    print("Reading from {0}".format(device_name))
    while True:
        try:
            id += 1
            device_bytes = device.readline()
            decoded_bytes = device_bytes[0:len(device_bytes)].decode("utf-8")

            if "Token" in decoded_bytes:
                match = re.search("Token: (.+)", decoded_bytes, re.IGNORECASE)
                token_name = match.group(1)
                token_name = token_name.replace('\r', '')
                execute_event(device_name, token_name)
        except Exception as e:
            print(e)


for d in devices:
    device_serial = serial.Serial(d)
    thread = threading.Thread(target=read_from_port, args=(device_serial, d, ))
    thread.start()
