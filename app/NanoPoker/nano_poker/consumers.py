import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import random
import logging

from .models import Account
from .models import GameState
from .handle_event import Event
from .models import Transaction
from .models import Action
from .utils import *

logger = logging.getLogger(__name__)


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

        # notify of started transaction
        async_to_sync(self.channel_layer.group_send)(
            "ChannelOne",
            {
                'type': 'transaction_pending',
                'message': message
            }
        )

        device = message["device"]
        token = message["token"]
        application = message["application"]
        action_type = message["type"]

        event = Event(application, device, token)

        if action_type == "bet":
            logger.info("Trigger bet signal received")
            event.trigger_bet()
        elif action_type == "cash_out":
            logger.info("Trigger cash_out signal received")
            event.trigger_cash_out()
        else:
            raise Exception("Not a valid type")

        # notify of completed transaction
        async_to_sync(self.channel_layer.group_send)(
            "ChannelOne",
            {
                'type': 'transaction_complete',
                'message': message
            }
        )

    def transaction_pending(self, message):
        self.send(text_data=json.dumps({
            "type": "transaction_pending",
            "message": message
        }))


    def transaction_complete(self, message):

        player_one = Account.objects.get(account_name="Player One")
        player_two = Account.objects.get(account_name="Player Two")
        pot_account = Account.objects.get(account_name="Pot Account")
        game_state = GameState.objects.get(application_name="NanoPoker")

        transactions = Transaction.objects.all().order_by('-pk')[:3]
        for t in transactions:
            t.amount = convert_raw_to_NANO(t.amount)

        actions = Action.objects.all().order_by('-pk')[:9]

        self.send(text_data=json.dumps({
            'players': [Account.to_dict(player_one), Account.to_dict(player_two)],
            'currentpot': "{:0.2f}".format(pot_account.balance),
            'totaltransfered': "{:0.2f}".format(game_state.total_nano_transferred),
            'totaltransactions': "{:0.2f}".format(game_state.total_transactions),
            'transactions': serialize_general(transactions),
            'actions': serialize_general(actions)
        }))

    def sync_data(self):
        player_one_account, d = Account.objects.get_or_create(account_name="Player One")
        player_two_account, d = Account.objects.get_or_create(account_name="Player Two")
        pot, d = Account.objects.get_or_create(account_name="Pot Account")

        Account.sync_account(player_one_account)
        Account.sync_account(player_two_account)
        Account.sync_account(pot)

        transactions = Transaction.objects.all().order_by('-pk')[:3]
        for t in transactions:
            t.amount = convert_raw_to_NANO(t.amount)

        actions = Action.objects.all().order_by('-pk')[:9]

        game_state, d = GameState.objects.get_or_create(application_name="NanoPoker")
        self.send(text_data=json.dumps({
            "type": "initial",
            'players': [Account.to_dict(player_one_account), Account.to_dict(player_two_account)],
            'currentpot': "{:0.2f}".format(pot.balance),
            'totaltransfered': "{:0.2f}".format(game_state.total_nano_transferred),
            'totaltransactions': "{:0.2f}".format(game_state.total_transactions),
            'transactions': serialize_general(transactions),
            'actions': serialize_general(actions)
        }))
