# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 18:35:48 2023

@author: SOURYA
"""

import requests 
import pandas as pd 
import json
from datetime import datetime
from pymongo import MongoClient
from config import *
from logger import log_report
class GetReportByDate:
    def __init__(self):
        pass
    def get_report(date):
        client = MongoClient(mongo_uri)
        db = client[db_name]
        temperature_archive= db["temperature_archive"]
        #date = "2011-01-01"
        mydoc = temperature_archive.find({'time' : {"$regex" : date }})
        temp_list={}
        for x in mydoc:
          temp_list[x['time']]=x['temperature']
          
        log_report.log_msg("Data got for date "+ date)
        return temp_list