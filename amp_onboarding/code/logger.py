# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:27:25 2023

@author: SOURYA
"""
from config import *
import logging

class log_report:
    def __init__(self):
        pass
    
    def log_msg(message):
        logging.basicConfig(filename= log_file,
                					format='%(asctime)s %(message)s',
                					filemode='a', force= True)
                
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.info(message)