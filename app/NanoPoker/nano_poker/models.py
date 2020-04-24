from django.db import models
from django.conf import settings
import requests
import json


class Account(models.Model):
    balance = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    betting = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    gains = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    address = models.CharField(max_length=64)

    account_name = models.CharField(max_length=64)

    application_name = models.CharField(max_length=64, null=False)

    @staticmethod
    def sync_account(account):
        data = {"application_name": account.application_name, "account_name": account.account_name}
        account_json = json.dumps(requests.post(settings.NANOTOKEN_ENDPOINT+"/action/accounts/get", data))
        account.balance = account_json["fields"]["balance"]
        account.address = account_json["fields"]["address"]
        account.save()

    @staticmethod
    def to_dict(account):
        output = {}
        output['balance'] = "{:0.2f}".format(account.balance)
        output['address'] = account.address
        output['betting'] = "{:0.2f}".format(account.betting)
        output['gains'] = "{:0.2f}".format(account.gains)
        return output


class Action(models.Model):
    action_name = models.CharField(max_length=64)

    policy_name = models.CharField(max_length=64)

    executed_time = models.DateTimeField(default=None, null=True)

    application_name = models.CharField(max_length=64, null=False)


class Transaction(models.Model):
    to_account = models.CharField(max_length=64)

    from_account = models.CharField(max_length=64)

    amount = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    application_name = models.CharField(max_length=64, null=False)

    executed_time = models.DateTimeField(default=None, null=True)


class GameState(models.Model):
    total_nano_transferred = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    total_transactions = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    application_name = models.CharField(max_length=64, null=False)
