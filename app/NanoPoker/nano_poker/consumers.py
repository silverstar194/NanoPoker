import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import random

from .models import Account
from .models import GameState

class MessageConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "ChannelOne",
            self.channel_name
        )

        self.accept()
        self.sync_data()

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

        device = message["device"]
        token = message["token"]
        application = message["application"]
        action_type = message["type"]

        event = Event(application, device, token)

        if action_type == "bet":
            event.trigger_bet()
        elif action_type == "cash_out":
            event.trigger_cash_out()
        else:
            raise Exception("Not a valid type")

        self.send(text_data=json.dumps({
            'players': [playerone, playertwo],
            'currentpot': 0,
            'totaltransfered': random.randrange(0, 100, 2),
            'totaltransactions': random.randrange(0, 100, 2),
            'transactions': [""],
            'actions': [""]
        }))

    def sync_data(self):
        player_one_account, d = Account.objects.get_or_create(account_name="player_one")
        player_two_account, d = Account.objects.get_or_create(account_name="player_two")
        pot, d = Account.objects.get_or_create(account_name="pot")

        Account.sync_account(player_one_account)
        Account.sync_account(player_two_account)
        Account.sync_account(pot)

        game_state, d = GameState.objects.get_or_create(application_name="nano_poker")
        self.send(text_data=json.dumps({
            'players': [Account.to_dict(player_one_account), Account.to_dict(player_two_account)],
            'currentpot': "{:0.2f}".format(pot.balance),
            'totaltransfered': "{:0.2f}".format(game_state.total_nano_transferred),
            'totaltransactions': "{:0.2f}".format(game_state.total_transactions),
            'transactions': [""],
            'actions': [""]
        }))
