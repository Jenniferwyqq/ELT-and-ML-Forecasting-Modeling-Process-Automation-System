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
  train_df['Color'] = train_df['Color'].replace(['LIGHT-BLUE', 'DARK-BLUE', 'NAVY'],'BLUE')
  train_df['Color'] = train_df['Color'].replace(['BACK','CROCO-BLACK'],'BLACK')
  train_df['Color'] = train_df['Color'].replace(['D-BROWN', 'DARK-TAN', 'DK-NAT'],'DARK-BROWN')
  train_df['Color'] = train_df['Color'].replace(['DURSTY', 'L-GREY', 'D-GREY', 'GREY'],'GRAY')
  train_df['Color'] = train_df['Color'].replace(['OLIVE', 'GRASS'],'GREEN')
  train_df['Color'] = train_df['Color'].replace(['OAT-CHEET', 'KHAK'],'KHAKI-CAMO')
  train_df['Color'] = train_df['Color'].replace(['L-BROWN', 'NAT', 'TAN'],'LIGHT-BROWN')
  train_df['Color'] = train_df['Color'].replace(['LIGHT PINK', 'L-PINK', 'N-PINK'],'NEON-PINK')
  train_df['Color'] = train_df['Color'].replace(['LIGHT YELLOW', 'L-YELLOW', 'N-YELLOW'],'NRON-YELLOW')
  train_df['Color'] = train_df['Color'].replace(['WINE', 'LIPS', 'DARK-RED'],'RED')
  train_df['Color'] = train_df['Color'].replace(['O-RG', 'ORANGE', 'YEL'],'YELLOW')
  
  
  # transform category
  train_df['Category'] = train_df['Category'].replace(['S-BOOT', 'BOOTS'],'BOOT')
  train_df['Category'] = train_df['Category'].replace(['HEEL PUMP', 'HEELS'],'HEEL_PUNP')
  train_df['Category'] = train_df['Category'].replace(['LOWER SANDAL', 'HEEL SAMDAL', 'SAND'],'SANDAL')
  train_df['Category'] = train_df['Category'].replace(['SHOE', 'SNEAK', 'FLAT', 'FLAT SNEAKER'],'SNEAKER')
  
  # transform material
  train_df['Material'] = train_df['Material'].replace(['LEA', 'LEATH'],'LEATHER')
  train_df['Material'] = train_df['Material'].replace(['NB', 'NPU'],'NBPU')
  train_df['Material'] = train_df['Material'].replace(['ISU', 'SU', 'SUEDE'],'IMSU')
  train_df['Material'] = train_df['Material'].replace(['BRIGHT-PAT', 'P'],'PAT')
  
  
  # groupby the df
  train_df = pd.concat([train_df]).groupby(['Date', 'Category', 'Color', 'Material'])['Weekly_Sale'].sum().reset_index()
  train_df['Weekly_Sale'] = train_df['Weekly_Sale'].astype(int)
  
  print(train_df.info())
  
  # save into train.csv in local
  train_df.to_csv('new_train.csv', header=True,index=False)
