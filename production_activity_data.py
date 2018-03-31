'''
File Name      : production_activity_data.py
Author Name    : Lakshmi Damodara
Creation Date  : 01/28/2018
Updated on     : 02/02/2018
Version        : 1.0
Description    :
This program reads the individual sheets from Solar CCT mechanical tracker file and gets the values
for the public.activity_data table
The hard-coded value is the directory and the file of the excel_act_tble_config.ini file.
The cell positions are given in the config file.

The program reads the various attributes of the cell for activity columns and writes to output file
using the program excel_writing.py

Functions:

Files need to run this program:
1. excel_file_config.ini

Program dependencies:
1. excel_config_reader.py
2. excel_writing.py

Log File
1. log_file.txt : has been set at the DEBUG level to log all activities for the run time.

Output File
1. Based on the number of activities, respective files are written in the output directory
2. The output directory can be configured on excel_file_config.ini file

'''

import datetime

### -- Start of Functions --------
def updateProductionActivity_data( dbh, db_conn, rListDaily):
    for i in range(0, len(rListDaily)):
        activityName = str(rListDaily[i][0])
        activityDate = datetime.datetime.strptime(rListDaily[i][1], "%m%d%Y").date().strftime('%Y%m%d')
        activityActualUnits = rListDaily[i][5]
        execSQL = "INSERT INTO TEMP.ACTIVITY_DATA (ACTIVITY_NAME,DATE,ACTUAL_UNITS) VALUES (%s,%s,%s);"
        execData = (activityName,activityDate,activityActualUnits)
        dbh.executeQueryWithData(db_conn, execSQL, execData)

### ---------End of Functions -----

def processProductionActivity_data(wb, efcr, eut, dbh):
    ## Open db connection
    db_conn = dbh.getConn()

    # Fist get the active range sheets from excel_file_config.ini using excel_config_reader.py
    asheets = []
    result_data_sheet = []

    #----------------------------------------------------------------------------------------------
    # -- This section is to collect all the data from various activity sheet
    # -- Call the excel writing.py program to write the file into a csv format
    # -- The information about sheetname, total sheets etc are derived from excel_file_config.ini
    # -- The output file is determined by the name of the sheet.csv
    #----------------------------------------------------------------------------------------------

    #Truncate temp.activity_data
    LsqlQuery = "TRUNCATE TABLE temp.activity_data"
    dbh.executeQuery(db_conn, LsqlQuery)

    asheets = efcr.getActivitySheets() # get the list of activity sheets from excel_file_config.ini
    len_asheets = len((asheets))
    for i in range(0,len_asheets,2):
        sheet_val = asheets[i] # getting the active worksheet number
        result_data_sheet = eut.getSheetResult(wb,sheet_val) # calling function getSheetResult()
        #loc_fname = efcr.outputDirectory() + efcr.outputfileName() # getting the output directory and filename
        # calling the excel_writing.py to write the data to the file
        #eut.write_activity_daily_data_CSV(loc_fname, result_data_sheet)
        updateProductionActivity_data(dbh, db_conn,result_data_sheet)


    ##Function to update public.activity_data
    stProc = "SELECT update_production_activity_data()"
    dbh.executeQuery(db_conn, stProc)

    # close all the connections
    # close or delete all the open instances, Lists, and connections
    # clears all the variables from memory

    del result_data_sheet
    del asheets


#---- End of Program ------