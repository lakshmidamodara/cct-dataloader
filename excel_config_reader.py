''''
File Name      : excel_config_reader.py
Author Name    : Lakshmi Damodara
Date           : 01/23/2018
Version        : 1.0
Description    :
This program contains utility functions to read config files and return information like
filename, filedirectory, sheet information etc..

Files needed to run this program:
1. excel_file_config.ini

'''

# Library configparser is used to parse the config file
import configparser

# creating an instance of the configparser
config = configparser.ConfigParser()
config_act_tbl_config = configparser.ConfigParser()

# hard-coded config file to be read by this program
ConfigFileName = 'excel_config.ini'
ConfigDirName = '.\configs\\'
L_FileName = ConfigDirName + ConfigFileName
print(L_FileName)

config.read(L_FileName)

# returns the excel filename to be read
def fileName():
    return config['fileDetails']['fName']

# returns the excel directory to be read
def fileDirectory():
    output_dirName1 = config['fileDetails']['directory']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

# returns the total sheets within the excel workbook
def totalNoSheets():
    return config['fileDetails']['TotalSheets']

# returns the database name of the database
def shName(num):
    sheetseq = 'sheet' + str(num) # convert the num to string before passing the argument
    return config['ARelated'][sheetseq]

def getActivitySheets():
    #first get active range sheet
    list_sheets = config['ARelated']['Activity_Sheet_Range']
    return list_sheets

def getTotalWorkdays():
    getWorkdays = config['TotalWorkDays']['workdays']
    return getWorkdays

def outlineLevel():
    outlineLevel = config['OUTLINELEVEL']['outline_level']
    return outlineLevel

'''
# Testing the program
# get total sheets
sheetNum = totalNoSheets()
print (sheetNum)

# get sheet Names
for i in range(1, int(sheetNum)):
        sN = shName(i)
        # sheeNme = sheetNum(i)
        print(sN)

# get file name and directory
print(fileName())
print(fileDirectory())
'''

# --- End of Program ---
