import time
import random
import requests
import json

from auth import Signature

class Crawler():

    def time_sleep(self, max_sleep_time):
        time.sleep(random.uniform(1, max_sleep_time))

    def get_header(self, method, uri, api_key, secret_key, customer_id):
        self.timestamp = str(round(time.time() * 1000))
        self.signature = Signature.generate(self.timestamp, method, uri, secret_key)
        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': self.timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': self.signature}

    def set_params(self, keyword, start_date, end_date, time_unit='date', device='', gender='', ages=[]):
        params = {}
        params['startDate'] = start_date  # yyyy-mm-dd
        params['endDate'] = end_date  # yyyy-mm-dd
        params['timeUnit'] = time_unit  # date, week, month
        params['keywordGroups'] = [{'groupName': keyword, 'keywords': [keyword]}]
        params['device'] = device  # None, pc, mo
        params['gender'] = gender  # None, m, f
        params['ages'] = ages  # None, 0-11
        return json.dumps(params)

    def get_method(self, base_url, uri, params, headers):
        response = requests.get(base_url + uri, params=params, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)

        json_obj = response.json()
        return json_obj

    def post_method(self, base_url, params, headers):
        response = requests.post(base_url, data=params, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
            
        json_obj = response.json()
        return json_obj