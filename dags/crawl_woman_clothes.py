from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                  datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': seven_days_ago,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('crawl_woman_clothes', default_args=default_args)

crawl_dag = BashOperator(
    task_id='crawl_woman_clothes_task',
    bash_command='python /opt/airflow/crawler/shopee/crawl_woman_clothes.py',
    dag=dag)

crawl_dag