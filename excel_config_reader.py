''''
File Name      : excel_file_config_reader.py
Author Name    : Lakshmi Damodara
Date           : 01/23/2018
Version        : 1.0
Description    :
This program is a basic function file to return the excel information like
filename, filedirectory, sheet information etc..

The hard-coded value is the directory and the file of the excel_file_config.ini file.
The config file should be in the same directory as this file, if it is not, provide the right directory paths.

Files need to run this program:
1. excel_act_tble_config.ini
2. excel_file_config.ini

'''

# Library configparser is used to parse the config file
import configparser
import string

# creating an instance of the configparser
config = configparser.ConfigParser()
config_act_tbl_config = configparser.ConfigParser()

# hard-coded config file to be read by this program
ConfigFileName = 'excel_activity_config.ini'
#ConfigDirName = '..\\'
#L_FileName = ConfigDirName + ConfigFileName
L_FileName = ConfigFileName
config.read(L_FileName)

# returns the excel filename to be read
def fileName():
    return config['fileDetails']['fName']

# returns the excel directory to be read
def fileDirectory():
    output_dirName1 = config['fileDetails']['directory']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

def logfileName():
    return config['logFile']['fname']

# returns the excel directory to be read
def logfileDirectory():
    output_dirName1 = config['logFile']['directory']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

def outputDirectory():
    output_dirName1 = config['OutputDir']['outdir']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

def outputfileName():
    return config['OutputFile']['outfile']

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

def getoutfileName():
    try:
        return config['OUTPUTFILE']['fName']
    except Exception as e:
        print('Error in function getoutfileName() %s' %e)

# returns the excel directory to be read
def getfileDirectory():
    output_dirName1 = config['OUTPUTFILE']['directory']
    output_dirName = output_dirName1.replace("'", "")
    return output_dirName

def getOverviewSheetName():
    try:
        return config['PROJECT_OVERVIEW_SHEET']['shName']
    except Exception as e:
        print('Error in function getOverviewSheetName() %s' %e)

def getTotalWorkingColumn():
    try:
        return config['PROJECT_OVERVIEW_SHEET']['totalWorkingColumn']
    except Exception as e:
        print('Error in function getTotalWorkingColumn() %s' % e)

def getPrintDateTime():
    try:
        dtPrint = []
        dt = config['PROJECT_OVERVIEW_SHEET']['dateTm']
        dtPrint = getRowColumn(str(dt))
        return dtPrint
    except Exception as e:
        print('Error in getPrintDateTime() %s' %e)

def getPrintProjectName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_ProjectName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrintProjectName_Heading() %s' % e)

def getPrintProjectID_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_ProjectId']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrintProjectID_Heading() %s' % e)

def getPrint_ContractorName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_ContractorName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ContractorName_Heading() %s' %e)

def getPrint_Updated_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Updated']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Updated_Heading() %s' % e)

# --- Functions to get the values for headings --------------------

def getPrintProjectName_Value():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['value_ProjectName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrintProjectName_Value() %s' % e)

def getPrintProjectID_Value():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['value_ProjectId']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrintProjectID_Value() %s' % e)

def getPrint_ContractorName_Value():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['value_ContractorName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ContractorName_Value() %s' % e)

def getPrint_Updated_Value():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['value_Updated']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Updated_Value() %s' % e)

# ---------------End of value functions ---

def getPrint_ProjectSummary_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Project_Summary']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ProjectSummary_Heading() %s' % e)

def getPrint_ActivityID_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_ActivityID']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActivityID_Heading() %s' % e)


def getPrint_ActivityName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_ActivityName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActivityName_Heading() %s' % e)

def getPrint_TotalQuantities_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Total_Quantities']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_TotalQuantities_Heading() %s' % e)

def getPrint_UnitID_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_UnitId']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_UnitID_Heading() %s' % e)


def getPrint_UnitName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Units']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_UnitName_Heading() %s' % e)

def getPrint_Planned_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Planned']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Planned_Heading() %s' % e)

def getPrint_Actual_Heading():
    try:
        tpr = []
        pr = config['PROJECT_OVERVIEW_SHEET']['heading_Actual']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Actual_Heading() %s' % e)


def getPrint_Activity_Heading():
    try:
        return config['PROJECT_OVERVIEW_SHEET']['activity_Heading_Column']
    except Exception as e:
        print('Error in getPrint_Activity_Heading() %s' % e)


#--------------------End of Overview sheet ----------

#----------- Start - Acvitiviy Sheet --------
def getPrint_ActSheet_ActivityID_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['heading_ActivityID']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ActivityID_Heading() %s' % e)


def getPrint_ActSheet_ActivityName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['heading_ActivityName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ActivityName_Heading() %s' % e)

def getPrint_ActSheet_ContractorName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['heading_ContractorName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ContractorName_Heading() %s' % e)

def getPrint_ActSheet_UnitName_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['heading_Units']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_UnitName_Heading() %s' % e)

def getPrint_ActSheet_ActivityID_Value():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['value_ActivityID']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ActivityID_Value() %s' % e)

def getPrint_ActSheet_ActivityName_Value():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['value_ActivityName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ActivityName_Value() %s' % e)

def getPrint_ActSheet_ContractorName_Value():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['value_ContractorName']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_ContractorName_Value() %s' % e)

def getPrint_ActSheet_UnitName_Value():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['value_Units']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_ActSheet_UnitName_Value() %s' % e)

# ------------ Printing Across columns -----------------------------
def getPrint_Across_ActSheet_ActivityID_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_ActivityID']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_ActivityID_Heading() %s' % e)

def getPrint_Across_ActSheet_Date_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Date']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_Date_Heading() %s' % e)

def getPrint_Across_ActSheet_Installed_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Installed']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_Installed_Heading() %s' % e)

def getPrint_Across_ActSheet_CompletedToday_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Completed_Today']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_CompletedToday_Heading() %s' % e)

def getPrint_Across_ActSheet_CompletedToDate_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Completed_To_Date']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_CompletedToDate_Heading() %s' % e)

def getPrint_Across_ActSheet_PlannedToDate_Heading():
    try:
        tpr = []
        pr = config['PROJECT_ACTIVITY_SHEET']['across_heading_Planned_To_Date']
        tpr = getRowColumn(str(pr))
        return tpr
    except Exception as e:
        print('Error in getPrint_Across_ActSheet_PlannedToDate_Heading() %s' % e)

def getLowerAlphabetDictionary():
    try:
        letter_count = dict(zip(string.ascii_lowercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
        return letter_count
    except Exception as e:
        print('Error in getLowerAlphabetDictionary() %s' % e)

def getUpperAlphabetDictionary():
    try:
        letter_count = dict(zip(string.ascii_uppercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
        return letter_count
    except Exception as e:
        print('Error in getUpperAlphabetDictionary() %s' % e)

def getRowColumn(strVal):
    try:
        rowCol = []
        Tcol = strVal[0]
        T1col = getUpperAlphabetDictionary()
        col = T1col[Tcol]
        Trow = int(strVal[1:])
        row = Trow -1
        rowCol.append(row)
        rowCol.append(col)
        return rowCol
    except Exception as e:
        print('Error in getRowColumn() %s' % e)
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
