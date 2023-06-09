# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 22:19:53 2023

@author: SOURYA
"""

from get_report_from_api import GetReportFromAPI
from get_report_bydate import GetReportByDate
from get_forecast_bydate import GetForecastByDate
from flask import Flask,request
import requests
import json
from config import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
auth = HTTPBasicAuth()


users = {
    "dev": generate_password_hash("test_password"),
    "sit": generate_password_hash("sit_password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.current_user()

@app.route('/report/api', methods=['POST'])
@auth.login_required
def report_api():
    result= GetReportFromAPI.get_report()
    return result.to_json()

@app.route('/report/date', methods=['POST'])
@auth.login_required
def report_bydate():
    data = request.json
    date = data.get('date')
    result= GetReportByDate.get_report(date)
    return result

@app.route('/forecast/date', methods=['POST'])
@auth.login_required
def forecast_bydate():
    data = request.json
    date = data.get('date')
    result= GetForecastByDate.get_report(date)
    return result

if __name__ == "__main__":
    port = server_port
    app.run(host='0.0.0.0', port=port,debug=True)
