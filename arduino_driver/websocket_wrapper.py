import websocket
import time


class WebSocket:

    def __init__(self, ws_address):
        self.ws_address = ws_address
        self.nano_poker_ws = websocket.WebSocket()
        self.nano_poker_ws.connect(ws_address, on_connect=self.on_connect, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.queue = []
        self.last_time = 0

    def on_connect(self, ws, message):
       print(message)

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ws ###")

    def send(self, data):

        if time.time() - self.last_time < 5:
            return

        i = 0
        while True:
            try:
                print(data)
                self.last_time = time.time()
                self.queue.append((data, time.time()))
                self.nano_poker_ws.send(data)
                return
            except:
                print("Reconnecting socket...")
                self.nano_poker_ws = websocket.WebSocket()
                self.nano_poker_ws.connect(self.ws_address, on_connect=self.on_connect, on_message=self.on_message,
                                           on_error=self.on_error, on_close=self.on_close)
                i += 1
                if i > 5:
                    raise


