# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:04:51 2023

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

class GetForecastByDate:
    def __init__(self):
        pass
    def get_report(date):
        date_list=[]
        time_list=[]
        for i in range(24):
            date_list.append('2023-01-01')
            time_list.append(str(i)+":00:00")
        
        client = MongoClient(mongo_uri)
        db = client[db_name]
        temperature_archive= db["temperature_archive"]
        data = temperature_archive.find()
        #data = r.json()
        df = pd.DataFrame.from_records(data)
        df = df[['time','temperature']]
        df['time']= pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        y=df['temperature']   
           
        df=pd.DataFrame({"Date" : date_list, "Time" : time_list})
        df= pd.to_datetime(df['Date'] + df['Time'], format='%Y-%m-%d%H:%M:%S')
        df.columns=["Date"]
        
        
        SARIMAXmodel = SARIMAX(y, order = (1, 0, 1), seasonal_order=(0,0,1,12))
        SARIMAXmodel = SARIMAXmodel.fit()
        
        y_pred = SARIMAXmodel.get_forecast(len(df))
        y_pred_df = y_pred.conf_int(alpha = 0.05) 
        y_pred_df["Predictions"] = SARIMAXmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
        y_pred_df.index = df.index
        y_pred_out = y_pred_df["Predictions"] 
        
        log_report.log_msg("Data predicted for date "+ date)
        return y_pred_df.to_json()