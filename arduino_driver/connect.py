import serial
import threading
import re
import json
import time
import argparse
import sys

from websocket_wrapper import WebSocket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--playerOne", help="device file path for player one", required=True)
    parser.add_argument("--playerTwo", help="device file path for player two", required=True)
    parser.add_argument("--pot", help="device file path for pot", required=True)
    parser.add_argument("--nanoPokerWs", help="device file path pot", required=True)
    args = parser.parse_args()

    player_one_device = args.playerOne
    player_two_device =  args.playerTwo
    pot_device = args.pot
    nano_poker_ws = args.nanoPokerWs

    try:
        ws = WebSocket(nano_poker_ws)
    except:
        print("Nano Poker backend not started at {0}".format(nano_poker_ws))
        sys.exit()

    device_id_to_device_name = {pot_device: "device_one", player_one_device: "device_two", player_one_device: "device_three"}
    devices = [pot_device, player_one_device, player_two_device]

    try:
        for d in devices:
            device_serial = serial.Serial(d)
            thread = threading.Thread(target=read_from_port, args=(device_serial, d, ))
            thread.start()
    except:
        print("No device {0}".format(d))
        sys.exit()

def place_bid(device_name, token_name, id):
    data = {"message": {"id": id, "application": "NanoPoker", "device": device_id_to_device_name[device_name], "token": token_name, "type": "bet"}}
    ws.send(json.dumps(data))


def cash_out(device_name, token_name, id):
    data = {"message": {"id": id, "application": "NanoPoker", "device": device_id_to_device_name[device_name], "token": token_name, "type": "cash_out"}}
    ws.send(json.dumps(data))


def execute_event(device, token, id):
    if device == pot_device:
        place_bid(device, token, id)

    elif device in [player_one_device]:
        cash_out(device, token, id)

    else:
        raise Exception("Device not registered")


def read_from_port(device, device_name):
    id = 0
    print("Reading from {0}".format(device_name))
    last_read = 0
    while True:
        try:
            id += 1
            device_bytes = device.readline()
            decoded_bytes = device_bytes[0:len(device_bytes)].decode("utf-8")

            if "Token" in decoded_bytes and (int(round(time.time() * 1000)) - last_read > 5*1000):
                match = re.search("Token: (.+)", decoded_bytes, re.IGNORECASE)
                token_name = match.group(1)
                token_name = token_name.replace('\r', '')
                execute_event(device_name, token_name, id)
                last_read = int(round(time.time() * 1000))
        except Exception as e:
            print("Exception reading:", str(e))

