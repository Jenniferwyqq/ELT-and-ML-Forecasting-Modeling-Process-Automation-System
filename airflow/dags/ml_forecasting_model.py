
def mlModel(): 
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    import pandas as pd
    import calendar
    from sklearn import metrics

    data = pd.read_csv('train_df.csv')

    def replace_value(df):
        df['Material'] = df['Material'].replace('IMSU', 1)
        df['Material'] = df['Material'].replace('NBPU', 2)
        df['Material'] = df['Material'].replace('PU', 3)
        df['Material'] = df['Material'].replace('PAT', 4)
        df['Material'] = df['Material'].replace('LEATHER', 5)

        df['Category'] = df['Category'].replace('BOOT', 1)
        df['Category'] = df['Category'].replace('SANDAL', 2)
        df['Category'] = df['Category'].replace('HEEL_PUMP', 3)
        df['Category'] = df['Category'].replace('SLIPPER', 4)
        df['Category'] = df['Category'].replace('SNEAKER', 5)

        df['Color'] = df['Color'].replace('BLACK', 1)
        df['Color'] = df['Color'].replace('DARK-BROWN', 2)
        df['Color'] = df['Color'].replace('LIGHT-BROWN', 3)
        df['Color'] = df['Color'].replace('NEON-YELLOW', 4)
        df['Color'] = df['Color'].replace('WHITE', 5)
        df['Color'] = df['Color'].replace('GRAY', 6)
        df['Color'] = df['Color'].replace('SILVER', 7)
        df['Color'] = df['Color'].replace('GOLD', 8)
        df['Color'] = df['Color'].replace('BLUE', 9)
        df['Color'] = df['Color'].replace('NEON-PINK', 10)
        df['Color'] = df['Color'].replace('KHAKI-CAMO', 11)
        df['Color'] = df['Color'].replace('PURPLE', 12)
        df['Color'] = df['Color'].replace('RED', 13)
        df['Color'] = df['Color'].replace('SKIN', 14)
        df['Color'] = df['Color'].replace('YELLOW', 15)
        df['Color'] = df['Color'].replace('GREEN', 16)
    
    replace_value(data)
    
    total = data.isnull().sum(axis=0).sort_values(ascending=False)
    percent = ((data.isnull().sum(axis=0)/data.isnull().count(axis=0))*100).sort_values(ascending=False)

    # count the number of null values in the column and their perecentage of the total data
    missing_data_columns = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

    data['Date']=pd.to_datetime(data['Date'])

    copy_data=data.copy()
    copy_data['Month'] = pd.DatetimeIndex(copy_data['Date']).month
    copy_data['Month'] = copy_data['Month'].apply(lambda x: calendar.month_abbr[x])
    copy_data['Year'] = pd.DatetimeIndex(copy_data['Date']).year
    copy_data['Day']=pd.DatetimeIndex(copy_data['Date']).day

    copy_data.index=range(len(copy_data))
    copy_data.drop(columns={'Date'},axis=1,inplace=True)
    copy_data=copy_data.join(pd.get_dummies(copy_data['Month']))
    copy_data.drop(columns={'Month'},axis=1,inplace=True)

    X_train, X_test, y_train, y_test= train_test_split(copy_data.drop(columns={'Weekly_Sale'},axis=1),copy_data['Weekly_Sale'],test_size=0.2,random_state=0)

    model = RandomForestRegressor(n_estimators=100,n_jobs=-1)
    X, y = X_train, y_train

    model.fit(X,y)

    y_pred=model.predict(X_test)
    y_pred=pd.DataFrame(data=y_pred,index=X_test.index)

    data_test = pd.read_csv('test.csv')
    data_test2 = data_test.copy()
    replace_value(data_test)

    data_test['Month'] = pd.DatetimeIndex(data_test['Date']).month
    data_test['Month'] = data_test['Month'].apply(lambda x: calendar.month_abbr[x])
    data_test['Year'] = pd.DatetimeIndex(data_test['Date']).year
    data_test['Day']=pd.DatetimeIndex(data_test['Date']).day

    data_test=data_test.join(pd.get_dummies(data_test['Month']))
    data_test.drop(columns={'Month','Date'},axis=1,inplace=True)

    data_test['Jan']=0
    data_test['Feb']=0
    data_test['Mar']=0
    data_test['Apr']=0
    data_test['May']=0
    data_test['Jun']=0
    data_test['Jul']=0
    data_test['Aug']=0
    data_test['Sep']=0
    data_test['Nov']=0
    data_test['Dec']=0

    data_test=data_test[X_test.columns]

    pred=pd.DataFrame(index=data_test.index)
    data=model.predict(data_test)
    pred['quantity'] = data

    pred=pred.join(data_test2['Date'])
    pred=pred.join(data_test2['Category'])
    pred=pred.join(data_test2['Color'])
    pred=pred.join(data_test2['Material'])
    pred.index=pred.Date
    pred['quantity'] = pred['quantity'].astype(int)

    output = pred.loc[pred['Date'] == pred["Date"].min()]
    output=output.sort_values(by="quantity", ascending=False)
    output=output.iloc[:25]
    output.to_csv('Results.csv', header=False,index=False)
    df_output = pd.read_csv('Results.csv')

    print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error (RMSE):', metrics.mean_squared_error(y_test, y_pred, squared=False))
    print('Mean Absolute Percentage Error (MAPE):', metrics.mean_absolute_percentage_error(y_test, y_pred))
    print('Explained Variance Score:', metrics.explained_variance_score(y_test, y_pred))
    print('Max Error:', metrics.max_error(y_test, y_pred))
    print('Median Absolute Error:', metrics.median_absolute_error(y_test, y_pred))
    print('R^2:', metrics.r2_score(y_test, y_pred))