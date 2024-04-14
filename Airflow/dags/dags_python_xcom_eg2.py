import pendulum
import datetime
from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="dags_python_xcom_eg2",
    schedule="0 0 * * *", 
    start_date=pendulum.datetime(2024, 4, 9, tz="Asia/Seoul"), # 시작 시간
    catchup=False, 
) as dag:
    @task(task_id='python_xcom_push_by_return')
    def xcom_push_result(**kwargs):
        return 'Success'
    
    @task(task_id='python_xcom_pull_1')
    def xcom_pull_1(**kwargs):
        ti= kwargs['ti']
        value1 = ti.xcom_pull(task_ids='python_xcom_push_by_return')
        print('xcom_pull 메서드로 직접 찾은 리턴 값: ' + value1)
    
    @task(task_id='python_xcom_pull_2')
    def xcom_pull_2(status, **kwargs):
        print('함수 입력값으로 받은 값: ' + status)

python_xcom_push_by_result = xcom_push_result() # 그냥 리턴값을 가지고 있는 str이 아니라 task 객체로 보아야 한다.
xcom_pull_2(python_xcom_push_by_result)
python_xcom_push_by_result >> xcom_pull_1()