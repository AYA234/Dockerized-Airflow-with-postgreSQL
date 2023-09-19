
import pandas as pd
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine


def read_files_from_shared_memory():
    shared_volume_path = '../../../shared_volume/'
    csv_files = [file for file in os.listdir(shared_volume_path) if file.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the shared volume. Skipping processing.")
        return

    dfs = []

    for csv_file in csv_files:
        file_path = os.path.join(shared_volume_path, csv_file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    if dfs:
        combined_df = pd.concat(dfs)
        print("Data processing completed successfully.")
        return(combined_df)
    else:
        print("No data found in the CSV files. Skipping processing.")
        return

def apply_data_cleaning(**context):
    df = context['ti'].xcom_pull(task_ids='process_csv')
    print("df",df)
    df_cleaned = df.dropna()
    df_cleaned.drop(df_cleaned[df_cleaned['price'] <= 0].index, inplace=True)
    df_cleaned.drop(df_cleaned[(df_cleaned['points'] > 100) | (df_cleaned['points'] < 0)].index, inplace=True)

    print("Applying data cleaning.")
    return df_cleaned

def write_to_postgres(**context):
    db_string = "postgresql://postgres:123@db:5432/postgres"
    engine = create_engine(db_string)
    df = context['ti'].xcom_pull(task_ids='apply_data_cleaning')
    print('Writing to postgres.')
    df.to_sql('winmag', engine, if_exists='replace')
    print('Data written successfully to PostgreSQL.')

    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM winmag LIMIT 10")
        print("Selected data from PostgreSQL:")
        for row in result:
            print(row)



default_args = {
    'owner': 'Ayala',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 17),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'Data_streaming',
    default_args=default_args,
    description='Data streaming with postgresql.',
    schedule_interval=timedelta(days=1),
)

process_csv = PythonOperator(
    task_id='process_csv',
    python_callable=read_files_from_shared_memory,
    dag=dag,
)

data_cleaning = PythonOperator(
    task_id='apply_data_cleaning',
    python_callable=apply_data_cleaning,
    provide_context=True,
    dag=dag,
)

write = PythonOperator(
    task_id='write_to_postgres',
    python_callable=write_to_postgres,
    provide_context=True,
    dag=dag,
)




# Define task dependencies
process_csv >> data_cleaning >> write 
