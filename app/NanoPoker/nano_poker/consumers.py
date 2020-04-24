import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import random

class MessageConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "ChannelOne",
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "ChannelOne",
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            "ChannelOne",
            {
                'type': 'on_message',
                'message': message
            }
        )

    def on_message(self, event):
        message = event['message']

        ## Do work with backend here
        message["balance"] = random.randrange(0, 100, 2)

        playerone = {}
        playerone["balance"] = random.randrange(0, 100, 2)
        playerone["betting"] = random.randrange(0, 100, 2)
        playerone["gains"] = random.randrange(0, 100, 2)
        playerone["address"] = random.randrange(0, 100, 2)

        playertwo = {}
        playertwo["balance"] = random.randrange(0, 100, 2)
        playertwo["betting"] = random.randrange(0, 100, 2)
        playertwo["gains"] = random.randrange(0, 100, 2)
        playertwo["address"] = random.randrange(0, 100, 2)

        playerthree = {}
        playerthree["balance"] = random.randrange(0, 100, 2)
        playerthree["betting"] = random.randrange(0, 100, 2)
        playerthree["gains"] = random.randrange(0, 100, 2)
        playerthree["address"] = random.randrange(0, 100, 2)

        transaction = {}
        transaction["from"] = "nano_fgas"
        transaction["to"] = "nano_agfagf"
        transaction["amount"] = random.randrange(0, 100, 2)

        self.send(text_data=json.dumps({
            'players': [playerone, playertwo, playerthree],
            'currentpot': random.randrange(0, 100, 2),
            'totaltransfered': random.randrange(0, 100, 2),
            'totaltransactions': random.randrange(0, 100, 2),
            'transactions': [transaction]
        }))