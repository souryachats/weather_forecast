import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45',
                     'Compression': 'yes',
                     'CompressionLevel': '9'}
config['weather_report'] ={} 
config['weather_report']['mongodb_uri'] = 'mongodb://localhost:27017'
config['weather_report']['mongodb_db'] = 'weather_report'
config['weather_report']['weather_api'] ='https://archive-api.open-meteo.com/v1/era5'
config['weather_report']['server_port'] = '8080'
config['weather_report']['weather_log']= '..\logs\weather.log'

with open('config.ini', 'w') as configfile:
  config.write(configfile)