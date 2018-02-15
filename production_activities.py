'''
File Name      : production_activities.py
Author Name    : Lakshmi Damodara
Date           : 01/24/2018
Version        : 1.0
Description    :
This program reads Solar CCT excel file and gets the production/actual data and
populates public.activities table. The cell positions are given in the config file.

The program reads the various attributes of the cell for activity columns and writes to output file
using the program excel_writing.py

Functions:
converDate, getActivityNameCellPosition, getUnitNameCellPosition, getContractorNameCellPosition
getPlannedStartCellPosition, getPlannedEndCellPosition

Files need to run this program:
1. excel_activity_config.ini
2. excel_file_config.ini

Program dependencies:
1. excel_config_reader.py
2. excel_writing.py
3. excel_utilities.py

Log File
1. log_file.txt : has been set at the DEBUG level to log all activities for the run time.

'''

#import openpyxl
import configparser
import datetime
#import logging

#import excel_writing as gwWriter
#import excel_utilities as eu
#import db_utilities as dbh

### -- Start of Functions --------
# function to convert dates to string in mmddyyyy format
def convertDate(dtt):
    return datetime.datetime.date(dtt) # returns just the date in mm-dd-yyyy format

#returns the cell position of project name from excel_activity_config.ini
def getProjectName(config):
    return config['Project']['projectName']

def getActivityNameCellPosition(config,pos): #returns the value of activities_name from excel_act_tble_config.ini
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_name']
    return cell_postion

#returns the value of unit name from excel_act_tble_config.ini
def getUnitNameCellPosition(config,pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_unit_name']
    return cell_postion

#returns the value of contractor name from excel_act_tble_config.ini
def getContractorNameCellPosition(config,pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_contractor_name']
    return cell_postion

#returns the value of planned start date from excel_act_tble_config.ini
def getPlannedStartCellPosition(config,pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_planned_start']
    return cell_postion

#returns the value of planned end date from excel_act_tble_config.ini
def getPlannedEndCellPosition(config,pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_planned_end']
    return cell_postion

#function to get output file name for writing out the results csv file
#def outfile(config):
#    return config['outputFileName']['fname']

#function to get output directory file name for writing out the results csv file
#def outfileDir(config):
#    return config['outputFileName']['fdirectory']

# returns incremented value of a variable
def incrementfnc(tval):
    tval = tval + 1
    return tval

def extractActualStartDate(L_actual_start_date,rList):
     data = rList[0][1]
     L_actual_start_date.append(data)
     return data

def extractActualEndDate(L_actual_end_date,rList):
        leng_list = len(rList)
        data = rList[leng_list -1][1]
        L_actual_end_date.append(data)
        return data

def updateProductionActivities(dbh, db_conn, rList):
    for i in range(0, len(rList)):
        activityName = str(rList[i][0])
        unit_name = str(rList[i][1])
        contractor_name = rList[i][2]
        # converts the string to YYMMDD format to be inserted into Progresql database
        planned_start = datetime.datetime.strptime(rList[i][3], "%m%d%Y").date().strftime('%Y%m%d')
        planned_end = datetime.datetime.strptime(rList[i][4], "%m%d%Y").date().strftime('%Y%m%d')
        actual_start = datetime.datetime.strptime(rList[i][5], "%m%d%Y").date().strftime('%Y%m%d')
        actual_end = datetime.datetime.strptime(rList[i][6], "%m%d%Y").date().strftime('%Y%m%d')
        projectName = rList[i][7]

        execSQL = "INSERT INTO TEMP.ACTIVITIES (NAME,UNIT_NAME,CONTRACTOR_NAME,PLANNED_START,PLANNED_END,ACTUAL_START,ACTUAL_END,PROJECT_NAME) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        execData = (activityName,unit_name,contractor_name, planned_start,planned_end,actual_start,actual_end,projectName)
        dbh.executeQueryWithData(db_conn, execSQL, execData)

### ---------End of Functions -----


def processProductionActivities(act_wb, efcr_activities, eut, dbh, config):

    print('Function: processProductionActivities........')

    ## Open db connection
    db_conn = dbh.getConn()
    # getting the active worksheet
    wrksheet_names = act_wb.sheetnames

    L_result_data_sheet = []
    L_actual_start_date = []
    L_actual_end_date = []

    asheets = efcr_activities.getActivitySheets() # get the list of activity sheets from excel_file_config.ini
    len_asheets = len((asheets))
    for i in range(0,len_asheets,2):
        sheet_val = asheets[i] # getting the active worksheet number
        L_result_data_sheet = eut.getSheetResult(act_wb,sheet_val) # calling function getSheetResult()
        L_actual_start_date.append(L_result_data_sheet[0][1])
        L_actual_end_date.append(L_result_data_sheet[len(L_result_data_sheet) -1][1])

    #get the total activities in the sheet
    tot_activity = config['TotalActivities']['total_activities']

    # initializing a list
    Final_List = list()

    # This for loop is to go through the excel sheet
    # Take key values of excel_act_tble_config.ini as arguments
    # search each cell to get the values
    print('Entering into For loop to get values from excel sheet')
    #logging.debug('Entering into For loop to get values from excel sheet')

    # get the active sheet
    activityName_active_sheet = wrksheet_names[0]
    # pass the active sheet name
    sheet = act_wb[activityName_active_sheet]

    L1 = []

    #-----------------------------------------
    #  First truncate the data from activities table
    #------------------------------------------
    LsqlQuery = "TRUNCATE TABLE temp.activities"
    dbh.executeQuery(db_conn, LsqlQuery)

    #-----------------------------------------
    #  Getting the project Name from the sheet
    #------------------------------------------
    projectName_cell = getProjectName(config)
    projectName = sheet[projectName_cell].value
    print(projectName)

    # -------------------------------------------------------------
    # Getting other values from the worksheet
    #--------------------------------------------------------------
    for i in range(0,int(tot_activity)):
        L_activityName_cell_value = sheet[getActivityNameCellPosition(config, i)]
        L_activities_unit_name_cell_value = sheet[getUnitNameCellPosition(config,i)]
        L_activities_contractor_name_cell_value = sheet[getContractorNameCellPosition(config,i)]
        LC_activities_planned_start_cell_value = sheet[getPlannedStartCellPosition(config,i)]
        L_activities_planned_start_date = convertDate(LC_activities_planned_start_cell_value.value).strftime('%m%d%Y')
        LC_activities_planned_end_cell_value = sheet[getPlannedEndCellPosition(config,i)]
        L_activities_planned_end_date = convertDate(LC_activities_planned_end_cell_value.value).strftime('%m%d%Y')
        L_activities_actual_start_date = L_actual_start_date[i]
        L_activities_actual_end_date = L_actual_end_date[i]

        # Depending on the number of activities, the if loop will load the list
        j = i - 1
        L1.insert(j,L_activityName_cell_value.value)
        L1.insert(incrementfnc(j+1),L_activities_unit_name_cell_value.value)
        L1.insert(incrementfnc(j+2),L_activities_contractor_name_cell_value.value)
        L1.insert(incrementfnc(j+3),L_activities_planned_start_date)
        L1.insert(incrementfnc(j+4),L_activities_planned_end_date)
        L1.insert(incrementfnc(j+5),L_activities_actual_start_date)
        L1.insert(incrementfnc(j+6), L_activities_actual_end_date)
        L1.insert(incrementfnc(j+7), projectName)
        final_list = [L1]

        # output file
        #output_FileName1 = outfileDir(config) + str(outfile(config))
        #output_FileName = output_FileName1.replace("'","")
        # Now pass the list along with filename to the writer python file
        #eut.writeCSVFile(output_FileName,final_list)
        updateProductionActivities(dbh, db_conn, final_list)
        L1 = []

    # now run the query to update public.activities table
    stProc = "SELECT update_production_activities()"
    dbh.executeQuery(db_conn, stProc)

    # close or delete all the open instances, Lists, and connections
    # clears all the variables from memory
    #db_conn.close()
    del final_list
    del L1
    del L_result_data_sheet
    del L_actual_start_date
    del L_actual_end_date


# --- End of Program ---