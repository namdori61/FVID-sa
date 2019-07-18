import configparser
import sys
#sys.path.append("..")

from crawler import Crawler

class Controller():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        
        self.api_key = config['API']['AD_ACCESS_LICENSE']
        self.secret_key = config['API']['AD_SECRET_KEY']
        self.customer_id = config['API']['AD_CUSTOMER_ID']
        self.ad_url = config['API']['AD_URL']
        self.ad_uri = config['API']['AD_URI']
        
        self.client_id = config['API']['LAB_CLIENT_ID']
        self.client_secret = config['API']['LAB_CLIENT_SECRET']
        self.lab_url = config['API']['LAB_URL']

        self.crawler = Crawler()

if __name__ == "__main__":
    controller = Controller()

    #get_method example in Naver Ad api
    #header = controller.crawler.get_header("GET", controller.ad_uri, controller.api_key, controller.secret_key, controller.customer_id)
    #res = controller.crawler.get_method(controller.ad_url, controller.ad_uri, {'hintKeywords': '이니스프리', 'showDetail': 1}, header)

    #post_method example in Naver data lab api
    #res = controller.crawler.post_method(controller.lab_url, controller.crawler.set_params('이니스프리','2019-07-06','2019-07-08'), {'X-Naver-Client-Id' : controller.client_id, 'X-Naver-Client-Secret' : controller.client_secret, 'Content-Type' : 'application/json'})