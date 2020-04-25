from django.conf import settings


import requests
import json
import logging

from .models import GameState

logger = logging.getLogger(__name__)


class Event:

    def __init__(self, application, device_name, token_name):
        self.device_name = device_name
        self.token_name = token_name
        self.application = application
        self.device_to_player_map = {"device_one": "Pot", "device_two": "Player One", "device_three": "Player Two"}

    def update_gamestate_after_cashout(self):
        game_state = GameState.objects.get(application_name=self.application)
        game_state.total_transactions += 1

        past_actions = self.post_request("/action/actionhistory/all", token_data)
        ## sync accounts

        ## add new transaction


        ## add new action

    def update_gamestate_after_bet(self):
        game_state = GameState.objects.get(application_name=self.application)
        game_state.total_transactions += 1

        self.post_request("/action/actionhistory/all", token_data)
        ## add to pot
        ## update account bet

        ## sync accounts

        ## add new transaction

        ## add new action

    def change_token_action_polices_bet(self):
        # after bet allow  send to any player
        data = {'application': self.application, 'token_name': self.token_name}

        token_data = self.post_request("/action/token/get", data)

        token_data['action_polices'] = ["Allow Send from Pot"]
        self.post_request("/action/token/update", data)

    def change_token_action_polices_cash_out(self):
        # after cash out allow send only back to pot
        data = {'application': self.application, 'token_name': self.token_name}

        token_data = self.post_request("/action/token/get", data)
        token_data['action_polices'] = ["Allow Send to Pot from "+self.device_to_player_map[self.device_name]]

        self.post_request("/action/token/update", token_data)

    def trigger_bet(self):
        self.trigger()
        self.change_token_action_polices_bet()
        self.update_gamestate_after_bet()

    def trigger_cash_out(self):
        self.trigger()
        self.change_token_action_polices_cash_out()
        self.update_gamestate_after_bet()

    def trigger(self):
        data = {"application": self.application, "token_name": self.token_name, "device_name": self.device_to_player_map[self.device_name]}
        self.post_request("/action/execute", data)

    def post_request(self, path, data):
        logger.info(path, json.dumps(data))

        response = requests.post(settings.NANOTOKEN_ENDPOINT + path, data=json.dumps(data))
        if response.status_code != 200:
            logger.error("Post Failed")

        body = json.loads(response.text)
        logger.info(body)

        return body
