import pandas as pd

def transform():
  for i in range(100):
    print(5)
  # concat multiple train data cv
  csv_files = ['s3.csv', 'gdrive.csv', 'redshift.csv']
  train_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
  
  # transform value
  train_df['Category'] = train_df['Category'].str.upper()  
  train_df['Color'] = train_df['Color'].str.upper() 
  train_df['Material'] = train_df['Material'].str.upper()
  
  # transform color
  # train_df['Color'] = train_df['Color'].replace(['30days','35days'],'40days')
  
  # transform category
  # train_df['Category'] = train_df['Category'].replace(['30days','35days'],'40days')
  
  # transform material
  # train_df['Material'] = train_df['Material'].replace(['30days','35days'],'40days')
  
  
  # groupby the df
  train_df = pd.concat([train_df]).groupby(['Date', 'Category', 'Color', 'Material'])['Weekly_Sale'].sum().reset_index()
  train_df['Weekly_Sale'] = train_df['Weekly_Sale'].astype(int)
  
  print(train_df.info())
  
  # save into train.csv in local
  train_df.to_csv('new_train.csv', header=True,index=False)