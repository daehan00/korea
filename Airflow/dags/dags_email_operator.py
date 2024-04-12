from airflow import DAG
import pendulum
import datetime
from airflow.operators.email import EmailOperator

with DAG(
    dag_id = 'dags_email_operator',
    schedule = '0 9 * * *',
    start_date = pendulum.datetime(2024, 4, 12, tz = 'Asia/Seoul'),
    catchup = False
) as dag :
    send_email_task = EmailOperator(
        task_id = 'send_email_task',
        to = '2000daehan@naver.com',
        subject = 'Airflow test mail'
        html_content = 'Test success'
    )