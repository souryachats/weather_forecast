# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:02:37 2023

@author: SOURYA
"""
import requests 
import pandas as pd 
import json
from datetime import datetime
from pymongo import MongoClient
from config import *
from logger import log_report

class GetReportFromAPI:
    def __init__(self):
        pass
    def get_report():
        client = MongoClient(mongo_uri)
        db = client[db_name]
        temperature_archive= db["temperature_archive"]
        latitude=str(52.52)
        longitude=str(13.41)
        url = weather_report_url+"?latitude="+latitude+"&longitude="+longitude+"&start_date=2011-01-01&end_date=2022-12-31&hourly=temperature_2m"
        r = requests.get(url)
        if (r.status_code == 200):   
            data = r.json()
            temperature_list=[]
            temperature_document={}
            for temp in range(len(data['hourly']['time'])):
                temperature_document['time']=data['hourly']['time'][temp]
                temperature_document['temperature']=data['hourly']['temperature_2m'][temp]
                temperature_document['latitude'] = latitude
                temperature_document['longitude'] = longitude
                temperature_list.append(temperature_document)
                temperature_document={}
                
            #df = pd.DataFrame(list(zip(data['hourly']['time'], data['hourly']['temperature_2m'])))
            #df.columns = ['time','temperature']
            #print(df.head())
            x = temperature_archive.insert_many(temperature_list)
        
            #print list of the _id values of the inserted documents:
            #print(x.inserted_ids)
            log_report.log_msg("Data Inserted for latitude "+latitude+" and longitude "+ longitude)

