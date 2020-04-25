from django.db import models
from django.conf import settings


import requests
import json
from decimal import *
import logging

logger = logging.getLogger(__name__)


class Account(models.Model):
    balance = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    betting = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    gains = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    address = models.CharField(max_length=64)

    account_name = models.CharField(max_length=64)

    application_name = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.account_name
    @staticmethod
    def sync_account(account):
        data = {"application": account.application_name, "account_name": account.account_name}
        logger.info(settings.NANOTOKEN_ENDPOINT+"/action/account/get/balance")

        response = requests.post(settings.NANOTOKEN_ENDPOINT+"/action/account/get/balance", json.dumps(data))
        if response.status_code != 200:
            logger.error("sync_account failed for account {0}".format(account.sync_account))
        account_json = json.loads(response.text)
        logger.info(account_json)

        account.balance = Decimal(account_json["message"]["current_balance"])

        response = requests.post(settings.NANOTOKEN_ENDPOINT + "/action/account/get/address", json.dumps(data))
        if response.status_code != 200:
            logger.error("sync_account failed for account {0}".format(account.sync_account))

        account_json = json.loads(response.text)
        account.address = account_json["message"]["address"]
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
