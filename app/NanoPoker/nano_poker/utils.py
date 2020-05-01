from django.core import serializers

import re
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def deserializer_general(objects_serialized):
    objects_deserialized = serializers.deserialize('python', objects_serialized, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    transactions = []
    for obj in objects_deserialized:
        obj.save()
        transactions.append(obj.object)
    return transactions

def convert_raw_to_NANO(raw_amount):
    raw_amount_to_one_nano = Decimal(1000000000000000000000000000000)
    return raw_amount / raw_amount_to_one_nano

def add_text(input, before, after):
    input_str = json.dumps(input)
    input_proccssed = input_str.replace(before, after)
    return json.loads(input_proccssed)

def serialize_general(objects):
    object_temp = serializers.serialize('python', objects, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return strip_text(object_temp, "nano_poker.")

def strip_text(before, value):
    obj_str = json.dumps(before,  cls=DecimalEncoder, default=str).replace(value, "") # remove token_api
    re.sub(r', \s +]', "]", obj_str) # remove trailing comma
    re.sub(r', \s +}', "}", obj_str)  # remove trailing comma
    obj = json.loads(obj_str)
    return obj
