import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable

with DAG(
    dag_id="dags_bash_with_variable",
    schedule="0 0 * * *", 
    start_date=pendulum.datetime(2024, 4, 9, tz="Asia/Seoul"), # 시작 시간
    catchup=False
) as dag:
    var_value = Variable.get("sample_key")

    bash_var_1 = BashOperator(
        task_id = "bash_var_1",
        bash_command=f"echo variable:{var_value}"
    )
    
    bash_var_2 = BashOperator(
        task_id = "bash_var_2",
        bash_command="echo variable:{{var.value.sample_key}}"
    )