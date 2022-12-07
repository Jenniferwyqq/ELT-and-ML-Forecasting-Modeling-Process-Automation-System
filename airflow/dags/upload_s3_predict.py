import pandas as pd
import boto3

def upload_s3_predict():
	# REGION = 'ap-northeast-1'
  ACCESS_KEY_ID='AKIA3OITEBE35PXEBLUV'
  SECRET_ACCESS_KEY='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'
  BUCKET_NAME = '597projectdata'
  KEY = 'test.csv' # file path in S3

  data = pd.read_csv('test.csv')
  data.drop(data[data['Date'] == data["Date"].min()].index, inplace = True)
  data.to_csv('test.csv',header=True,index=False)
  
  s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
  s3.upload_file(KEY, BUCKET_NAME, KEY)