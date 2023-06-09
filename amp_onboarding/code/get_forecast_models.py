# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 20:41:13 2023

@author: SOURYA
"""

from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import *
from logger import log_report
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

client = MongoClient(mongo_uri)
db = client[db_name]
temperature_archive= db["temperature_archive"]
data = temperature_archive.find()
#data = r.json()
df = pd.DataFrame.from_records(data)
df = df[['time','temperature']]
df['time']= pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

sns.set()
plt.ylabel('Temperature')
plt.xlabel('Date-Time')
plt.xticks(rotation=45)
plt.plot(df.index, df['temperature'], )
plt.show()

train = df[df.index < pd.to_datetime("2022-12-25", format='%Y-%m-%d')]
test = df[df.index > pd.to_datetime("2022-12-25", format='%Y-%m-%d')]

plt.plot(train, color = "black")
plt.plot(test, color = "red")
plt.ylabel('temperature')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.title("Train/Test split for Temperature Data")


y = train['temperature']
ARMAmodel = SARIMAX(y, order = (1, 0, 1))

ARMAmodel = ARMAmodel.fit()

y_pred = ARMAmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05) 
y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"] 
plt.plot(y_pred_out, color='green', label = 'ARMA Predictions')
plt.legend()

arma_rmse = np.sqrt(mean_squared_error(test["temperature"].values, y_pred_df["Predictions"]))
print("ARMA RMSE: ",arma_rmse)

ARIMAmodel = ARIMA(y, order = (1,0,1))
ARIMAmodel = ARIMAmodel.fit()

y_pred = ARIMAmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05) 
y_pred_df["Predictions"] = ARIMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"] 
plt.plot(y_pred_out, color='Yellow', label = 'ARIMA Predictions')
plt.legend()

arima_rmse = np.sqrt(mean_squared_error(test["temperature"].values, y_pred_df["Predictions"]))
print("ARIMA RMSE: ",arima_rmse)

SARIMAXmodel = SARIMAX(y, order = (1, 0, 1), seasonal_order=(0,0,1,12))
SARIMAXmodel = SARIMAXmodel.fit()

y_pred = SARIMAXmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05) 
y_pred_df["Predictions"] = SARIMAXmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"] 
plt.plot(y_pred_out, color='Blue', label = 'SARIMA Predictions')
plt.legend()

sarima_rmse = np.sqrt(mean_squared_error(test["temperature"].values, y_pred_df["Predictions"]))
print("SARIMA RMSE: ",sarima_rmse)
#print(y_pred_df["Predictions"][0])
print(test.head())