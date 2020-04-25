import websocket
import time

class WebSocket:

    def __init__(self, ws_address):
        self.nano_poker_ws = websocket.WebSocket()
        self.nano_poker_ws.connect(ws_address, on_connect=self.on_connect, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.queue = []

    def on_connect(self, ws, message):
        print(message)

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ws ###")

    def send(self, data):
        already_seen = [item for item in self.queue if item[0] == data]
        if already_seen:
            if (time.time() - already_seen[0][1]) < 5:
                return
            else:
                self.queue.remove(already_seen[0])

        logger.info(data)
        self.queue.append((data, time.time()))
        self.nano_poker_ws.send(data)
