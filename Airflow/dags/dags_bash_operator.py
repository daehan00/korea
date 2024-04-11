from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="dags_bash_operator", # 파일명과 통일
    schedule="0 0 * * *", # 주기
    start_date=pendulum.datetime(2024, 4, 9, tz="Asia/Seoul"), # 시작 시간
    catchup=False, # 위 datetime 이전 소급적용여부
    dagrun_timeout=datetime.timedelta(minutes=60), # 타임아웃 설정, 현재는 60분인데, 삭제 가능
    tags=["example", "example2"], #검색용 태그
    params={"example_key": "example_value"}, # 아래에서 쓸 파마리터
) as dag:
    bash_task1 = BashOperator( # 태스크 객체
        task_id="bash_task1", # 태스크 객체명, 위와 통일
        bash_command="echo whoami", # string 출력
    )
    bash_task2 = BashOperator( # 태스크 객체
        task_id="bash_task2", # 태스크 객체명, 위와 통일
        bash_command="echo $HOSTNAME", # string 출력
    )

    bash_task1 >> bash_task2