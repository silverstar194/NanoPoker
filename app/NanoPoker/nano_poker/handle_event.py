from ..NanoPoker.settings import NANOTOKEN_ENDPOINT
import requests
import json

from .models import GameState


class Event:

    device_to_player_map = {"device_one": "pot", "device_two": "player_one", "device_three": "player_two"}

    def __init__(self, application_name, device_name, token_name):
        self.device_name = device_name
        self.token_name = token_name
        self.application_name = application_name

    def update_gamestate_after_cashout(self):
        game_state = GameState.objects.get(application_name="nano_poker")
        game_state.total_transactions += 1

        past_actions = json.dumps(requests.post(NANOTOKEN_ENDPOINT + "/action/actionhistory/all", data=token_data))
        print(past_actions)
        ## sync accounts

        ## add new transaction


        ## add new action

    def update_gamestate_after_bet(self):
        game_state = GameState.objects.get(application_name="nano_poker")
        game_state.total_transactions += 1

        past_actions = json.dumps(requests.post(NANOTOKEN_ENDPOINT + "/action/actionhistory/all", data=token_data))
        print(past_actions)
        ## add to pot
        ## update account bet

        ## sync accounts

        ## add new transaction

        ## add new action

    def change_token_action_polices_bet(self):
        # after bet allow  send to any player
        data = {'application': application, 'token_name': self.token_name}
        token_data = json.loads(requests.post(NANOTOKEN_ENDPOINT+"/action/token/get", data=data))

        token_data['action_polices'] = ["Allow Send from Pot"]
        requests.post(NANOTOKEN_ENDPOINT+"/action/token/update", data=token_data)

    def change_token_action_polices_cash_out(self):
        # after cash out allow send only back to pot
        data = {'application': application, 'token_name': self.token_name}
        token_data = json.loads(requests.post(NANOTOKEN_ENDPOINT+"/action/token/get", data=data))

        token_data['action_polices'] = ["Allow Send to Pot from "+device_to_player_map[device_to_player_map]]

        requests.post(NANOTOKEN_ENDPOINT+"/action/token/update", data=token_data)

    def trigger_bet(self):
        self.trigger()
        self.change_token_action_polices_bet()
        self.update_gamestate_after_bet()

    def trigger_cash_out(self):
        self.trigger()
        self.change_token_action_polices_cash_out()
        self.update_gamestate_after_bet()

    def trigger(self):
        data = {"application_name": self.application_name, "token_name": self.token_name, "device_name": self.device_name}
        requests.post(NANOTOKEN_ENDPOINT + "/action/execute", data=data)
