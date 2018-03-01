''''
File Name      : jason_config_reader.py
Author Name    : Lakshmi Damodara
Date           : 03/1/2018
Version        : 1.0
Description    :
This program is a basic function file to return the excel information like
filename, filedirectory, sheet information, cell information etc..

The hard-coded value is the directory and the file of the jason_writer_config.ini file.
The config file should be in the same directory as this file, if it is not, provide the right directory paths.

Files need to run this program:
1. jason_writer_config.ini

'''

# Library configparser is used to parse the config file
import configparser
import string

# creating an instance of the configparser
config = configparser.ConfigParser()
config_act_tbl_config = configparser.ConfigParser()

# hard-coded config file to be read by this program
ConfigFileName = 'Jason_writer.ini'
#ConfigDirName = '..\\'
L_FileName = ConfigFileName
config.read(L_FileName)

# returns the excel output filename to be written to
def getoutfileName():
    return config['OUTPUTFILE']['fName']

# returns the excel directory to be read
def getfileDirectory():
    output_dirName1 = config['OUTPUTFILE']['directory']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

def getOverviewSheetName():
    return config['PROJECT_OVERVIEW_SHEET']['shName']

def getTotalWorkingColumn():
    return config['PROJECT_OVERVIEW_SHEET']['totalWorkingColumn']

def getPrintDateTime():
    dtPrint = []
    dt = config['PROJECT_OVERVIEW_SHEET']['dateTm']
    dtPrint = getRowColumn(str(dt))
    return dtPrint

def getPrintProjectName_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_ProjectName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrintProjectID_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_ProjectId']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ContractorName_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_ContractorName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Updated_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Updated']
    tpr = getRowColumn(str(pr))
    return tpr

# --- Functions to get the values for headings --------------------

def getPrintProjectName_Value():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['value_ProjectName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrintProjectID_Value():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['value_ProjectId']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ContractorName_Value():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['value_ContractorName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Updated_Value():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['value_Updated']
    tpr = getRowColumn(str(pr))
    return tpr

# ---------------End of value functions ---

def getPrint_ProjectSummary_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Project_Summary']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActivityID_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_ActivityID']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActivityName_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_ActivityName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_TotalQuantities_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Total_Quantities']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_UnitID_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_UnitId']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_UnitName_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Units']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Planned_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Planned']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Actual_Heading():
    tpr = []
    pr = config['PROJECT_OVERVIEW_SHEET']['heading_Actual']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Activity_Heading():
    return config['PROJECT_OVERVIEW_SHEET']['activity_Heading_Column']

#--------------------End of Overview sheet ----------

#----------- Start - Acvitiviy Sheet --------
def getPrint_ActSheet_ActivityID_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['heading_ActivityID']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_ActivityName_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['heading_ActivityName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_ContractorName_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['heading_ContractorName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_UnitName_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['heading_Units']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_ActivityID_Value():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['value_ActivityID']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_ActivityName_Value():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['value_ActivityName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_ContractorName_Value():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['value_ContractorName']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_ActSheet_UnitName_Value():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['value_Units']
    tpr = getRowColumn(str(pr))
    return tpr

# ------------ Printing Across columns -----------------------------
def getPrint_Across_ActSheet_ActivityID_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_ActivityID']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Across_ActSheet_Date_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Date']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Across_ActSheet_Installed_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Installed']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Across_ActSheet_CompletedToday_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Completed_Today']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Across_ActSheet_CompletedToDate_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Completed_To_Date']
    tpr = getRowColumn(str(pr))
    return tpr

def getPrint_Across_ActSheet_PlannedToDate_Heading():
    tpr = []
    pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Planned_To_Date']
    tpr = getRowColumn(str(pr))
    return tpr

def getLowerAlphabetDictionary():
    letter_count = dict(zip(string.ascii_lowercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
    return letter_count

def getUpperAlphabetDictionary():
    letter_count = dict(zip(string.ascii_uppercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
    return letter_count

def getRowColumn(strVal):
    rowCol = []
    Tcol = strVal[0]
    T1col = getUpperAlphabetDictionary()
    col = T1col[Tcol]
    Trow = int(strVal[1:])
    row = Trow -1
    rowCol.append(row)
    rowCol.append(col)
    return rowCol

'''
# get file name and directory
fname = getoutfileName()
print(fname)
mt=getPrintDateTime()
print(getRowColumn(mt))
print(getfileDirectory())
print(getPrint_ActivityID_Heading())
print(getPrint_Actual_Heading())
print(getUpperAlphabetDictionary())

'''
# --- End of Program ---
