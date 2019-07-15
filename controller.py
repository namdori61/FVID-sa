import configparser
import sys

sys.path.append("..")

class Controller:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        
        self.api_key = config['API']['AD_ACCESS_LICENSE']
        self.secret_key = config['API']['AD_SECRET_KEY']
        self.customer_id = config['API']['AD_CUSTOMER_ID']
        
        self.client_id = config['API']['LAB_CLIENT_ID']
        self.client_secret = config['API']['LAB_CLIENT_SECRET']

if __name__ == "__main__":
    controller = Controller()
    
    lab_url = "https://openapi.naver.com/v1/datalab/search"
    
    ad_url = 'https://api.naver.com'
    ad_uri = '/keywordstool'

    