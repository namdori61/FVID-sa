from airflow import models
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import pendulum
	    
local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'sangho',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 24, tzinfo=local_tz),
    'email': ['namdori61@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)	}

with models.DAG(
    dag_id='crawler', description='crawling keyword trend data from search engine', 
    schedule_interval = '00  14  *  *  *', 
    default_args=default_args) as dag:
    
	
    t1 = BashOperator(
        task_id='keyword_trend_data_crawler',
        bash_command='cd /home/sangho/FVID-sa && python3 ./controller.py',
        dag=dag)

    t2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5',
        retries=3,
        dag=dag)
    
    t2.set_upstream(t1)
