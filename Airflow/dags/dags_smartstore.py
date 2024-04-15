import pendulum
import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from common.common_func import access_token, list_order

with DAG(
    dag_id="dags_smartstore",
    schedule="0 8-17 * * 1-5", #매주 월-금 8-17시까지 1시간 간격으로 수행
    start_date=pendulum.datetime(2024, 4, 15, tz="Asia/Seoul"),
    catchup=False
) as dag:

    get_token = PythonOperator(
        task_id = 'get_token',
        python_callable = access_token,
        op_kwargs = {'nav_id':'{{var.value.nav_id}}','nav_secret':'{{var.value.nav_secret}}'}
    )

    order_list = PythonOperator(
        task_id='order_list',
        python_callable= list_order,
        op_kwargs={'access_token':'{{ ti.xcom_pull(task_ids="get_token") }}'}
    )

    email_alarm = EmailOperator(
        task_id='email_alarm',
        to='2000daehan@naver.com',
        subject='{{ data_interval_end.in_timezone("Asia/Seoul") | ds }} 신규주문내역 {{ti.xcom_pull(task_ids="order_list")}}건',
        html_content='작업 실행 결과는 성공입니다. <br> \
                    주문내역 결과 {{ti.xcom_pull(task_ids="order_list")}}건입니다. <br>'
    )