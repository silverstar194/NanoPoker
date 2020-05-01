from django.conf import settings


import requests
import json
import logging
import threading
from datetime import datetime


from .utils import *
from .models import GameState
from .models import Account
from .models import Transaction
from .models import Action
from .retry import *

logger = logging.getLogger(__name__)


class Event:

    def __init__(self, application, device_name, token_name):
        self.device_name = device_name
        self.token_name = token_name
        self.application = application
        self.device_to_player_map = {"device_one": "Pot", "device_two": "Device - Player One", "device_three": "Device - Player Two"}

    def update_gamestate_before_event(self):
        game_state = GameState.objects.get(application_name=self.application)
        game_state.total_transactions += 1
        game_state.save()

    def trigger_bet(self):
        self.update_gamestate_before_event()

        trigger_response = self.trigger()

        transactions = self.process_transactions_with_internal_state(trigger_response)

        # update pot and betting account balances
        for t in transactions:
            if origin_account.balance - convert_raw_to_NANO(t.amount) >= 0:
                origin_account = Account.objects.get(account_name=t.origin[2:-2])
                origin_account.betting += convert_raw_to_NANO(t.amount)
                origin_account.balance -= convert_raw_to_NANO(t.amount)
                origin_account.gains -= convert_raw_to_NANO(t.amount)
                origin_account.save()

                destination_account = Account.objects.get(account_name=t.destination[2:-2])
                destination_account.balance += convert_raw_to_NANO(t.amount)
                destination_account.save()

        action = Action.objects.create()
        print(trigger_response)
        action.action_name = trigger_response['message'][0]['fields']['action_set'][0] if trigger_response['message'][0]['fields']['action_set'] else None
        action.policy_name = trigger_response['message'][0]['fields']['policy'][0] if trigger_response['message'][0]['fields']['policy'] else None
        action.executed_time = datetime.now()
        action.save()



    def trigger_cash_out(self):
        self.update_gamestate_before_event()

        trigger_response = self.trigger()

        transactions = self.process_transactions_with_internal_state(trigger_response)

        for t in transactions:
            origin_account = Account.objects.get(account_name=t.origin[2:-2])
            if origin_account.balance - convert_raw_to_NANO(t.amount) >= 0:
                origin_account.balance -= convert_raw_to_NANO(t.amount)
                origin_account.save()

                destination_account = Account.objects.get(account_name=t.destination[2:-2])
                destination_account.balance += convert_raw_to_NANO(t.amount)
                destination_account.gains += convert_raw_to_NANO(t.amount)
                destination_account.save()

            accounts = Account.objects.all()
            for a in accounts:
                a.betting = 0
                a.save()

        action = Action.objects.create()
        action.action_name = trigger_response['message'][0]['fields']['action_set'][0] if trigger_response['message'][0]['fields']['action_set'] else "None"
        action.policy_name = trigger_response['message'][0]['fields']['policy'][0] if trigger_response['message'][0]['fields']['policy'] else "None"
        action.application_name = trigger_response['message'][0]['fields']['application'][0] if trigger_response['message'][0]['fields']['application'][0] else "None"
        action.executed_time = datetime.now()
        action.save()

    def trigger(self):
        data = {"application": self.application, "token_name": self.token_name, "device_name": self.device_to_player_map[self.device_name]}
        return self.post_request("/action/execute", data, noretry=True)

    def post_request(self, path, data, noretry=False):
        logger.info(path)
        logger.info(str(data))

        if noretry:
            response = requests.post(settings.NANOTOKEN_ENDPOINT + path, data=json.dumps(data))
        else:
            response = retry_post(lambda: requests.post(settings.NANOTOKEN_ENDPOINT + path, data=json.dumps(data)))

        if response.status_code != 200:
            logger.error(response.text)
            raise Exception("Post failed")

        body = json.loads(response.text)
        logger.info(body)

        return body

    def process_transactions_with_internal_state(self, trigger_response):
        transactions = self.save_transactions_from_trigger(trigger_response)
        game_state = GameState.objects.get(application_name=self.application)
        print(transactions)
        for t in transactions:
            game_state.total_nano_transferred += convert_raw_to_NANO(t.amount)
            game_state.save()

        return transactions

    def save_transactions_from_trigger(self, trigger_response):
        response_transactions = trigger_response['message'][0]['fields']['transactions']

        transaction_for_saving = add_text(response_transactions, r'"model": "transaction"', r'"model": "nano_poker.transaction"')
        transactions = deserializer_general(transaction_for_saving)
        return transactions
