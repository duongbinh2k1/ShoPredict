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

dag = DAG('crawl_man_clothes', default_args=default_args)

crawl_man_dag = BashOperator(
    task_id='crawl_man_clothes_task',
    bash_command='python /opt/airflow/crawl_man_data.py',
    dag=dag)

publish_dag = BashOperator(
    task_id='publish_product_task',
    bash_command='python /opt/airflow/publish_product.py',
    dag=dag)

consume_dag = BashOperator(
    task_id='consume_product_task',
    bash_command='python /opt/airflow/consume_product.py',
    dag=dag)

crawl_man_dag >> publish_dag >> consume_dag