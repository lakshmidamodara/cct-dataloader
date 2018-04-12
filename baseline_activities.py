'''
File Name      : baseline_activities.py
Author Name    : Lakshmi Damodara
Creation Date  : 02/02/2018
Updation Date  :
Version        : 1.0
Description    :

This program reads the Solar CCT excel file and gets the baseline data to populate public.activities table
The cell positions for data values are given in the config file excel_activity_config.ini file.

Functions:
converDate, getActivityNameCellPosition, getUnitNameCellPosition, getContractorNameCellPosition
getPlannedStartCellPosition, getPlannedEndCellPosition

Files need to run this program:
1. excel_activity_config.ini
2. excel_config.ini

Program dependencies:
1. excel_config_reader.py
2. excel_writing.py
3. excel_utilities.py

Log File
1. log_file.txt : has been set at the DEBUG level to log all activities at run time.

'''

import datetime
import xlrd

### -- Start of Functions --------
# function to convert dates to string in mmddyyyy format
def convertDate(dtt):
    return datetime.datetime.date(dtt) # returns just the date in mm-dd-yyyy format

#returns the cell position of project name from excel_activity_config.ini
def getProjectName(config):
    return config['Project']['projectName']

def getActivityNameCellPosition(config, pos): #returns the value of activities_name from excel_act_tble_config.ini
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_name']
    return cell_postion

#returns the value of unit name from excel_act_tble_config.ini
def getUnitNameCellPosition(config, pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_unit_name']
    return cell_postion

#returns the value of contractor name from excel_act_tble_config.ini
def getContractorNameCellPosition(config, pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_contractor_name']
    return cell_postion

#returns the value of planned start date from excel_act_tble_config.ini
def getPlannedStartCellPosition(config, pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_planned_start']
    return cell_postion

#returns the value of planned end date from excel_act_tble_config.ini
def getPlannedEndCellPosition(config, pos):
    keyVal = 'activities' + str(pos)
    cell_postion = config[keyVal]['activities_planned_end']
    return cell_postion

#function to get output file config, name for writing out the results csv file
#def outfile(config):
#    return config['outputFileName']['fname']

#function to get output directory file name for writing out the results csv file
#def outfileDir(config):
#    return config['outputFileName']['fdirectory']

# returns incremented value of a variable
def incrementfnc(tval):
    tval = tval + 1
    return tval

def prResultData(rList):
    print(rList)

# Function to call the activities table and insert activity_name, unit_name etc into activities table
def updateBaseLineActivities(dbh, db_conn, final_list):
    # SQL for inserting data into public.activities table
    for i in range(0, len(final_list)):
        activityName = str(final_list[i][0])
        unit_name = str(final_list[i][1])
        contractor_name = final_list[i][2]
        # convert the string to yymmdd to be inserted
        planned_start = datetime.datetime.strptime(final_list[i][3],"%m%d%Y").date().strftime('%Y%m%d')
        planned_end = datetime.datetime.strptime(final_list[i][4], "%m%d%Y").date().strftime('%Y%m%d')
        project_name = final_list[i][5]
        execSQL = "INSERT INTO temp.activities (name, unit_name, contractor_name, planned_start, planned_end, project_name) values (%s,%s,%s,%s,%s,%s);"
        execData = (activityName, unit_name, contractor_name, planned_start, planned_end,project_name)
        dbh.executeQueryWithData(db_conn, execSQL, execData)

### ---------End of Functions -----


def processBaselineActivities(act_wb, eut, dbh, config):
    ## Open db connection
    db_conn = dbh.getConn()

    print('Function: processBaselineActivities........')

    # getting the active worksheet
    wrksheet_names = act_wb.sheet_names()

    #get the total activities in the sheet
    tot_activity = config['TotalActivities']['total_activities']

    # initializing a list
    Final_List = list()

    # This for loop is to go through the excel sheet
    # Take key values of excel_act_tble_config.ini as arguments
    # search each cell to get the values
    #logging.debug('Entering into For loop to get values from excel sheet')
    print('Entering into For loop to get values from excel sheet')

    # get the active sheet
    activityName_active_sheet = wrksheet_names[0]
    # pass the active sheet name
    sheet = act_wb.sheet_by_index(0)
    L1 = []

    #-----------------------------------------
    #  Getting the project Name from the sheet
    #------------------------------------------
    projectName_cell = getProjectName(config)
    # reading the cell address and getting the value in rows,columns
    projectName_position = eut.getRowColumn(projectName_cell)
    # getting the project name
    projectName = sheet.cell_value(projectName_position[0],projectName_position[1])

    for i in range(0,int(tot_activity)):
        #getting activity name
        ancp = getActivityNameCellPosition(config, i)
        acrc = eut.getRowColumn(ancp)
        L_activityName_cell_value = sheet.cell_value(acrc[0],acrc[1])

        #getting unit name
        auncp = getUnitNameCellPosition(config, i)
        aunrc  = eut.getRowColumn(auncp)
        L_activities_unit_name_cell_value = sheet.cell_value(aunrc[0],aunrc[1])

        #getting the contractor name
        acncp = getContractorNameCellPosition(config, i)
        acnrc = eut.getRowColumn(acncp)
        L_activities_contractor_name_cell_value = sheet.cell_value(acnrc[0],acnrc[1])

        #getting the planned start date
        apscp = getPlannedStartCellPosition(config, i)
        apscrc = eut.getRowColumn(apscp)
        a1 = sheet.cell_value(apscrc[0],apscrc[1])
        a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(a1, act_wb.datemode))
        L_activities_planned_start_date = convertDate(a1_as_datetime).strftime('%m%d%Y')

        #getting the planned end date
        apecp = getPlannedEndCellPosition(config, i)
        apecrc = eut.getRowColumn(apecp)
        a1 = sheet.cell_value(apecrc[0],apecrc[1])
        a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(a1, act_wb.datemode))
        L_activities_planned_end_date = convertDate(a1_as_datetime).strftime('%m%d%Y')

        # Depending on the number of activities, the if loop will load the list
        j = i - 1
        L1.insert(j,L_activityName_cell_value)
        L1.insert(incrementfnc(j+1),L_activities_unit_name_cell_value)
        L1.insert(incrementfnc(j+2),L_activities_contractor_name_cell_value)
        L1.insert(incrementfnc(j+3),L_activities_planned_start_date)
        L1.insert(incrementfnc(j+4),L_activities_planned_end_date)
        L1.insert(incrementfnc(j+5), projectName)

        final_list = [L1]
        print(final_list)

        # output file
 #       output_FileName1 = outfileDir(config ) + str(outfile(config))
  #      output_FileName = output_FileName1.replace("'","")
        # Now pass the list along with filename to the writer python file
        #eut.writeCSVFile(output_FileName,final_list)

        updateBaseLineActivities(dbh, db_conn, final_list)
        L1 = []

    # Now update the public.activities table
    stProcedure = "SELECT update_baseline_activities()"
    dbh.executeQuery(db_conn,stProcedure)
    db_conn.close()

    # close or delete all the open instances, Lists, and connections
    # clear all the variables from memory
    del final_list
    del L1


# --- End of Program ---