# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:05:44 2023

@author: SOURYA
"""
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
weather_report_config = config['weather_report']
weather_report_url= weather_report_config['weather_api']
log_file = weather_report_config['weather_log']
mongo_uri = weather_report_config['mongodb_uri']
db_name=weather_report_config['mongodb_db']
server_port=weather_report_config['server_port']