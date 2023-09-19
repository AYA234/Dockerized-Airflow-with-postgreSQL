
# import pandas as pd
# import os
# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.utils.dates import days_ago

# def read_files_from_shared_memory():
#     shared_volume_path = './shared_volume/'
#     csv_files = [file for file in os.listdir(shared_volume_path) if file.endswith('.csv')]

#     if not csv_files:
#         print("No CSV files found in the shared volume. Skipping processing.")
#         return

#     dfs = []

#     for csv_file in csv_files:
#         file_path = os.path.join(shared_volume_path, csv_file)
#         df = pd.read_csv(file_path)
#         dfs.append(df)

#     if dfs:
#         combined_df = pd.concat(dfs)
#         # Perform any additional processing on the combined_df as needed
#         # For example, data cleaning and validation

#         print("Data processing completed successfully.")
#     else:
#         print("No data found in the CSV files. Skipping processing.")

# def apply_data_cleaning(**context):
#     df = context['ti'].xcom_pull(task_ids='read_csv_file')
#     df_cleaned=df.dropna()
#     df_cleaned.drop(df_cleaned[df_cleaned['price'] <=0].index, inplace = True)
#     df_cleaned.drop(df_cleaned[(df_cleaned['points'] > 100) | (df_cleaned['points'] < 0)].index,inplace=True)

#     print("Applying data cleaning.")
#     return df_cleaned

# def write_to_postres(**context):
#     df = context['ti'].xcom_pull(task_ids='apply_data_cleaning')
#     print('Writing to postgres.')


# # Define the DAG's default arguments
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': days_ago(1),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# # Create the DAG
# dag = DAG(
#     'consumer',
#     default_args=default_args,
#     description='Consumer DAG to read and process CSVs from Producer',
#     schedule_interval=timedelta(hours=1),  # Adjust the interval as needed
# )

# # Task to read and process CSVs from Producer
# process_csv = PythonOperator(
#     task_id='process_csv2',
#     python_callable=read_files_from_shared_memory,
#     dag=dag
# )

# data_cleaning=PythonOperator(
#     task_id='apply_data_cleaning',
#     python_callable=apply_data_cleaning,
#     provide_context=True
# )

# write_to_postgres=PythonOperator(
#     task_id='write_to_postgres',
#     python_callable=write_to_postres,
#     provide_context=True
# )

# process_csv<< data_cleaning<<write_to_postgres

