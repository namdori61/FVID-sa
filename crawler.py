import time
import random
import requests

class Crawler():
    def get_header(self, method, uri, api_key, secret_key, customer_id):
        self.timestamp = str(round(time.time() * 1000))
        self.signature = Signature.generate(self.timestamp, method, uri, secret_key)
        return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': self.timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': self.signature}
    
    def set_params(keyword, start_date, end_date, time_unit='date', device='', gender='', ages=[]):
        params = {}
        params['startDate'] = start_date #yyyy-mm-dd
        params['endDate'] = end_date #yyyy-mm-dd
        params['timeUnit'] = time_unit #date, week, month
        params['keywordGroups'] = [{'groupName' : keyword, 'keywords' : [keyword]}]
        params['device'] = device #None, pc, mo
        params['gender'] = gender #None, m, f
        params['ages'] = ages #None, 0-11
        return json.dumps(params)
    
    def get_method(self, base_url, uri, params, headers):
        return requests.get(base_url + uri, params=params, headers=headers)
    
    def post_method(self, base_url, params, headers):
        return requests.post(url, data=params, headers=headers)

#get_method example in Naver Ad api
'''
ad_url = 'https://api.naver.com'
api_key = config['API']['AD_ACCESS_LICENSE']
secret_key = config['API']['AD_SECRET_KEY']
customer_id = config['API']['AD_CUSTOMER_ID']
uri = '/keywordstool'

cr = Crawler()
cr.get_header(method, uri, api_key, secret_key, customer_id)
res = cr.get_method(ad_url, uri, {'hintKeywords': '이니스프리', 'showDetail': 1}, cr.get_header("GET", uri, api_key, secret_key, customer_id))
'''

#post_method example in Naver data lab api
'''
client_id = config['API']['LAB_CLIENT_ID']
client_secret = config['API']['LAB_CLIENT_SECRET']
lab_url = "https://openapi.naver.com/v1/datalab/search"

cr = Crawler()
res = cr.post_method(lab_url, cr.set_params('이니스프리','2019-07-06','2019-07-08'), {'X-Naver-Client-Id' : client_id, 'X-Naver-Client-Secret' : client_secret, 'Content-Type' : 'application/json'})
'''