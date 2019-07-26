import configparser
import sys
#sys.path.append("..")
import platform
from datetime import date, timedelta

from crawler import Crawler
from logic import LogicManager
from db_manager import DataBaseManager

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

        if platform.system() != 'Darwin':
            self.db_host = config['SERVER']['DB_HOST']
            self.db_port = config['SERVER']['DB_PORT']
            self.db_db = config['SERVER']['DB_DB']
            self.db_user = config['SERVER']['DB_USER']
            self.db_pw = config['SERVER']['DB_PW']
            self.db_keyword_set_table = config['SERVER']['DB_KEYWORD_SET_TABLE']
            self.db_trend_table = config['SERVER']['DB_TREND_TABLE']
        else:
            self.db_host = config['LOCAL']['DB_HOST']
            self.db_port = config['LOCAL']['DB_PORT']
            self.db_db = config['LOCAL']['DB_DB']
            self.db_user = config['LOCAL']['DB_USER']
            self.db_pw = config['LOCAL']['DB_PW']
            self.db_keyword_set_table = config['LOCAL']['DB_KEYWORD_SET_TABLE']
            self.db_trend_table = config['LOCAL']['DB_TREND_TABLE']
        
        self.crawler = Crawler()
        self.logic_manager = LogicManager()
        self.db_manager = DataBaseManager()

# Scheduler
from celery.schedules import crontab
from celery import Celery
app = Celery('crawler', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

app.conf.update(
    BROKER_URL='redis://localhost:6379/0',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'get_keyword_data-every-day': {
            'task': 'controller.get_keyword_data',
            'schedule': crontab(hour=15),
            'args': ()
        },
    }
)

@app.task

def get_keyword_data():

    controller = Controller()

    pool = controller.db_manager.create_pool(controller.db_host, controller.db_port, controller.db_db, controller.db_user, controller.db_pw)

    keyword_list = controller.db_manager.select_data(pool, controller.db_keyword_set_table, "keyword")

    for keyword in keyword_list:
        header = controller.crawler.get_header("GET", controller.ad_uri, controller.api_key, controller.secret_key, controller.customer_id)
        ad_data = controller.crawler.get_method(controller.ad_url, controller.ad_uri, {'hintKeywords': keyword, 'showDetail': 1}, header)['keywordList'][0]
        lab_data = controller.crawler.post_method(controller.lab_url, controller.crawler.set_params(keyword,(date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),(date.today() - timedelta(days=1)).strftime('%Y-%m-%d')), {'X-Naver-Client-Id' : controller.client_id, 'X-Naver-Client-Secret' : controller.client_secret, 'Content-Type' : 'application/json'})
        refined_data = controller.logic_manager.keyword_data_transformer(lab_data, ad_data)
        controller.db_manager.insert_data(pool, controller.db_trend_table, refined_data)
        controller.crawler.time_sleep(10)

    controller.db_manager.closer(pool)