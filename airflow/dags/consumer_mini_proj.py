from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pandas as pd

default_args = {
    'owner':'Ayala',
    'start_date': datetime(2023,7,15),
    'schedule_interval': '@daily',
    
}

def read_csv_file():
    
    path_to_file='~/output.csv'
    print("Reading the csv files.") 
    df=pd.read_csv(path_to_file)
    return df
    

def apply_data_cleaning(**context):
    df = context['ti'].xcom_pull(task_ids='read_csv_file')
    df_cleaned=df.dropna()
    df_cleaned.drop(df_cleaned[df_cleaned['price'] <=0].index, inplace = True)
    df_cleaned.drop(df_cleaned[(df_cleaned['points'] > 100) | (df_cleaned['points'] < 0)].index,inplace=True)

    print("Applying data cleaning.")
    return df_cleaned

def write_to_postres(**context):
    df = context['ti'].xcom_pull(task_ids='apply_data_cleaning')
    print('Writing to postgres.')



with DAG(dag_id="consumer_mini_project_v1",
         default_args=default_args) as dag:
    task0=BashOperator(
        task_id='first_task',
        bash_command='echo pwd;pwd '
    )
    task1= PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv_file
    )

    task2=PythonOperator(
        task_id='apply_data_cleaning',
        python_callable=apply_data_cleaning,
        provide_context=True
    )
    
    task3=PythonOperator(
        task_id='write_to_postgres',
        python_callable=write_to_postres,
        provide_context=True
    )

    
    task0>>task1>>task2>>task3
