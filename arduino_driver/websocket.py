
class WebSocket:

    def __init__(self, ws_address):
        self.nano_poker_ws = websocket.WebSocket()
        self.nano_poker_ws.connect(ws_address, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def send(self, data):
        self.nano_poker_ws.send(data)
