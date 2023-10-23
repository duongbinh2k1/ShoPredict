from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from crawler.shopee.run import crawl_woman_clothes_shopee

dag = DAG(
    "crawl_woman_clothes_shopee",
    start_date=datetime(2023, 1, 1),
)

crawl_woman_clothes_task = PythonOperator(
    task_id="crawl_woman_clothes",
    python_callable=crawl_woman_clothes_shopee,
    dag=dag,
)
