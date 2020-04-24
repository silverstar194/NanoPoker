import serial
import threading
import re
import websocket
import json

from .websocket import WebSocket

nano_poker_ws = 'ws://127.0.0.1:8000/ws/message/action'

pot_device = '/dev/cu.usbserial-1440'
player_one_device = '/dev/cu.usbserial-1460'
player_two_device = ''
player_three_device = ''

devices = [pot_device, player_one_device, player_two_device, player_three_device]

ws = WebSocket(nano_poker_ws)


def place_bid(device_name, token_name):
    ws.send(json.dumps({"message": {"device": device_name, "token": token_name, "type": "bid"}}))


def cash_out(device_name, token_name):
    ws.send(json.dumps({"message": {"device": device_name, "token": token_name, "type": "cash_out"}}))


def execute_event(device, token):
    if device == pot_device:
        cash_out(device, token)

    if device in devices[-1:]:
        place_bid(device, token)


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
                print(device_name[-4:], token_name)
                execute_event(device_name[-4:], token_name)
        except Exception as e:
            print(e)


for device in devices:
    device_serial = serial.Serial(device)
    thread = threading.Thread(target=read_from_port, args=(device_serial, device, ))
    thread.start()
