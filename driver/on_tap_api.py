import requests
import json


class OnTap:

    def __init__(self, base_endpoint):
        self.base_endpoint = base_endpoint

    def execute(self, device_name, token_name, application):
        data = {'application': application, 'device_name': device_name, 'token_name': token_name}
        post_data("/action/execute", data)

    def update_policy_action_limit(self, application, policy_name, action_limit):
        policy = get_policy(application, policy_name)
        policy['fields']['action_limit'] = action_limit

        post_data("action/actionpolicy/update", policy)

    def get_policy(self, application, policy_name):
        data = {'application': application, 'policy_name': policy_name }
        return json.loads(post_data("/action/actionpolicy/get", data))

    def post_data(self, path, data):
        response = requests.post("{0}{1}".format(self.base_endpoint, path), data=data)

        if response.status != 200:
            raise Exception('post error')

        print(response.body)
        return response.body

