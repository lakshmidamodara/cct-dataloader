'''
File Name      : baseline_dataloader.py
Author Name    : Lakshmi Damodara
Creation Date  : 01/28/2018
Updated on     : 02/02/2018
Version        : 1.0
Description    :
     This program calls functions to read Solar CCT excel data files and loads baseline data into
     public.activities and public.activity_data

Output File
1. Based on the number of activities, respective files are written in the output directory
2. The output directory can be configured on excel_file_config.ini file

'''

import openpyxl
import xlsxwriter
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

import baseline_activity_data as bl_act_data
import baseline_activities as bl_act

print('##-------------------- ---------------------------------........')
print('##---Program: baseline_dataloader.py..........................')
print(datetime.datetime.today())
print('##-----------------------------------------------------........')

#wbFile = ''
import sys
import pprint
streamData = sys.stdin.buffer.read()
decodedData = base64.b64decode(streamData)
excelData = io.BytesIO(decodedData)

print("Encoding is")
#workbook = xlsxwriter.Workbook(excelData, {'in_memory': True})
#pprint.pprint(workbook.__dict__)
#print (sys.stdin.buffer.encoding)
#sys.exit()

#print( excelData.getvalue())
#print(sys.stdin.buffer)

#wb = openpyxl.load_workbook(filename=excelData.getvalue())
#wb = openpyxl.load_workbook(io.BytesIO(sys.stdin.buffer.read()))
#wb = openpyxl.load_workbook(io.BufferedReader(sys.stdin.buffer))
#wb = openpyxl.load_workbook(sys.stdin.buffer)
#wb = openpyxl.load_workbook(workbook.filename)
wb = xlrd.open_workbook(file_contents=excelData.getvalue())
sheet_names = wb.sheet_names()
print('Sheet Names', sheet_names)

#for line in sys.stdin:
#	#sys.stdout.write(line)
#	wbFile += line

#sys.stdin.readlines();
#wbFile = '\0x01'.join(wbFile)
#print(wbFile)
#sys.exit()

#decoded_data = base64.b64decode(wbFile)

#xls_file = io.BytesIO(decoded_data)
#print(xls_file)

#wb = openpyxl.load_workbook(io.BytesIO(excelData).read())
#g = BytesIO( excelData)
#print(type(wb))
#temp = "temp.xlsx"
#with open(temp,'wb') as out: ## Open temporary file as bytes
#    out.write(g.read())
#print(excelData.getvalue())
excelData.seek(0)
#out = open ("test.xlsx", 'wb')

with open("test.xlsx", 'wb') as out:  ## Open temporary file as bytes
        out.write(excelData.getvalue())

sys.exit()
#L_FileName = filedata

# get the filename and directory : Excel fileName and directory for reading values
#L_FileName = efcr.fileDirectory() + efcr.fileName() # directory + filename
#print('production_activity_data.py : opening excel file name - %s'%L_FileName)
# passing the file name and creating an instance of the workbook with actual values and ignoring the formulas
#wb = openpyxl.load_workbook(L_FileName,data_only='True')

# open the config parser to read the activities config file
config = configparser.ConfigParser()

ConfigFileName = 'excel_activity_config.ini'
ConfigDirName = '.\configs\\'
config_FileName = ConfigDirName + ConfigFileName
config.read(config_FileName)

bl_act.processBaselineActivities(wb, eut, dbh, config)
bl_act_data.processBaselineActivity_data(wb, efcr, eut, dbh)

# update file_storage in db
dbh.updateFileObjectIntoDB(dbh, wb, 'Bayshore', 'BaseLine')

wb.close()
del efcr
del eut
del dbh