import pendulum
import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.email import EmailOperator

with DAG(
    dag_id="dags_python_email_xcom",
    schedule="0 0 * * *", 
    start_date=pendulum.datetime(2024, 4, 9, tz="Asia/Seoul"), # 시작 시간
    catchup=False, 
) as dag:
    @task(task_id='something_task')
    def some_logic(**kwargs):
        from random import choice
        return choice(['Success','Fail'])
    
    send_email = EmailOperator(
        task_id='send_email',
        to='2000daehan@naver.com',
        subject='{{}} some_logic 처리결과',
        html_content='{{}} 처리 결과는 <br> \
                    {{}} 했습니다 <br>'
    )

    some_logic() >> send_email