import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_with_macro_eg1", # 파일명과 통일
    schedule="0 0 L * *", # 매월 말일
    start_date=pendulum.datetime(2024, 4, 9, tz="Asia/Seoul"), # 시작 시간
    catchup=False, # 위 datetime 이전 소급적용여부
) as dag:
    
    bash_task1 = BashOperator(
        #START_DATE:전월 말일, END_DATE: 1일 전 
        task_id="bash_task1", 
        env = {
            'START_DATE':'{{data_interval_start.in_timezone("Asia/Seoul") | ds}}',
            'END_DATE':'{{(data_interval_end.in_timezone("Asia/Seoul") - macros.dateutil.relativedelta.relativedelta(days=1)) | ds}}'
        },
        bash_command= 'echo "START_DATE: $START_DATE" && echo "END_DATE: $END_DATE"'
    )