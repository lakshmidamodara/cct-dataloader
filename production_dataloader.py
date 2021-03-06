#!python
'''
File Name      : production_dataloader.py
Author Name    : Lakshmi Damodara
Creation Date  : 01/28/2018
Updated on     : 02/02/2018
Version        : 1.0
Description    :
     This program calls functions to read Solar CCT excel data files and loads actuals data into
     public.activities and public.activity_data

Output File
1. Based on the number of activities, respective files are written in the output directory
2. The output directory can be configured on excel_file_config.ini file

'''

import configparser
import datetime
import sys
import base64
import io
import xlrd

#import excel_writing as ewWriter
import excel_utilities as eut
import excel_config_reader as efcr
import db_utilities as dbh

# These modules below provide the loaders for each of the tables
import production_activity_data as prod_act_data
import production_activities as prod_act

print('##-------------------- ---------------------------------........')
print('##---Program: production_dataloader.py..........................')
print(datetime.datetime.today())
print('##-----------------------------------------------------........')

streamData = sys.stdin.read()
decodedData = base64.b64decode(streamData)
excelData = io.BytesIO(decodedData)

wb = xlrd.open_workbook(file_contents=excelData.getvalue())
#wb = xlrd.open_workbook('Bayshore A-Mechanical Tracker v5.xlsx')

# open the config parser to read the activities config file
config = configparser.ConfigParser()

ConfigFileName = 'excel_activity_config.ini'
ConfigDirName = '.\configs\\'
config_FileName = ConfigDirName + ConfigFileName
config.read(config_FileName)


prod_act.processProductionActivities(wb, efcr, eut, dbh, config)
prod_act_data.processProductionActivity_data(wb, efcr, eut, dbh)

# update file_storage in db
dbh.updateFileObjectIntoDB(dbh, excelData.getvalue(), 'Streaming content for Actuals Data', 'Production')

del efcr
del eut
del dbh