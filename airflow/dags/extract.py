import boto3
import pandas as pd
import io
import psycopg2
import boto3
import numpy as np

def extract_gdrive():
  sheet_id = "1QFkZ5rOpTx44aB_rHsS-BrN6Nx1rqCB5_J5u0u2Fk5k"
  sheet_name = "weekly_sales"
  url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
  gdrive_df = pd.read_csv(url) 
  gdrive_df.to_csv('gdrive.csv',index=False)
  print("gdrive", len(gdrive_df))
  
def extract_s3():
  REGION = 'ap-northeast-1'
  ACCESS_KEY_ID='AKIA3OITEBE35PXEBLUV'
  SECRET_ACCESS_KEY='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'
  BUCKET_NAME = '597projectdata'
  KEY = 'new_s3_train.csv'
  s3c = boto3.client(
        's3', 
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
  )
  obj = s3c.get_object(Bucket= BUCKET_NAME , Key = KEY)
  s3_df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
  s3_df.to_csv('s3.csv',index=False)
  print("S3", len(s3_df))

  
def extract_redshift():  
  schema_name = 'new_weekly_data_redshift'
  dbname = 'dev'
  port = 5439
  user = 'jennifer'
  password = 'Hinagiku12'
  host_url = 'redshift.caxai5r7owzr.ap-northeast-1.redshift.amazonaws.com'
  #host_url = '54.199.0.252'  
  s3_bucket_name = '597projectdata'
  aws_access_key_id = 'AKIA3OITEBE35PXEBLUV'
  aws_secret_access_key = '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'
  
  conn_string = "dbname='{}' port='{}' user='{}' password='{}' host='{}'"\
      .format(dbname,port,user,password,host_url)  

  sql2 = "select * from new_weekly_data_redshift where Date = '2020-10-05'"
  con = psycopg2.connect(conn_string)

  cur = con.cursor()
  cur.execute(sql2)
  res = cur.fetchall()
  
  data = np.array(res)
  df = pd.DataFrame(data, columns = ['Date','Weekly_sale','Category', 'Color', 'Material'])
  df.to_csv('redshift.csv',index=False)
  print("df", len(df))
  
  cur.close()
  con.close()
  


def extract_train():
  REGION = 'ap-northeast-1'
  ACCESS_KEY_ID='AKIA3OITEBE35PXEBLUV'
  SECRET_ACCESS_KEY='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'
  BUCKET_NAME = '597projectdata'
  KEY = 'train.csv' 
  s3c = boto3.client(
        's3', 
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
  )
  obj = s3c.get_object(Bucket= BUCKET_NAME , Key = KEY)
  train_df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
  train_df.to_csv('train.csv',index=False)
  
  REGION = 'ap-northeast-1'
  ACCESS_KEY_ID='AKIA3OITEBE35PXEBLUV'
  SECRET_ACCESS_KEY='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'
  BUCKET_NAME = '597projectdata'
  KEY = 'test.csv'
  s3c = boto3.client(
        's3', 
        region_name = REGION,
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = SECRET_ACCESS_KEY
  )
  obj = s3c.get_object(Bucket= BUCKET_NAME , Key = KEY)
  test_df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
  test_df.to_csv('test.csv',index=False)
