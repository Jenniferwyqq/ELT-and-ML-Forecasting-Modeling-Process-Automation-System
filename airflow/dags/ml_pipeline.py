from datetime import datetime
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from extract import extract_train, extract_s3, extract_gdrive, extract_redshift
from transform import transform
from ml_forecasting_model import mlModel
from send_email import send_email
from upload_s3_train import upload_s3_train
from upload_s3_predict import upload_s3_predict

default_args={
    'owner':'Jennifer',
    'email_on_failure':False,
    'email': ['chihyi1126@gmail.com', 'chihyi88@gmail.com'],
    'start_date':datetime(2022, 12, 6)
}

# "0 0 * * 0,  catchup=false "*/5 * * * *"
with DAG(
    "airflow_docker_ml_pipeline",
    description = 'End-to-End',
    default_args=default_args,
    schedule_interval="*/5 * * * *",
    catchup=False) as dag:

    # Extract redshift
    extract_redshift=PythonOperator(
        task_id='extract_newest_weekly_train_data_from_redshift',
        python_callable=extract_redshift
    )
    
    # Extract google sheet
    extract_gdrive=PythonOperator(
        task_id='extract_newest_weekly_train_data_from_google_drive',
        python_callable=extract_gdrive
    )  
    
    # Extract S3
    extract_s3=PythonOperator(
        task_id='extract_newest_weekly_train_data_from_S3',
        python_callable=extract_s3
    )  
    
    # Transform
    transform=PythonOperator(
        task_id='transform_data',
        python_callable=transform
    )
    
    # execute ml model
    ml_model=PythonOperator(
        task_id='execute_ml_model',
        python_callable=mlModel
    )

    # Extract train
    extract_train=PythonOperator(
        task_id='extract_old_train_data_from_S3',
        python_callable=extract_train
    )
    
    # upload S3 train
    load_s3_train=PythonOperator(
        task_id='load_data_to_S3',
        python_callable=upload_s3_train
    )

    # send email
    email_send=PythonOperator(
        task_id='send_email_to_owner',
        python_callable=send_email
    )
    
    # upload S3 predict
    load_s3_predict=PythonOperator(
        task_id='load_predict_results_to_S3',
        python_callable=upload_s3_predict
    )

    [[extract_gdrive, extract_s3, extract_redshift] >> transform, extract_train] >> load_s3_train >> ml_model >> [load_s3_predict, email_send]
   