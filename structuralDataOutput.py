'''
File Name      : structuralDataOutput.py
Author Name    : Lakshmi Damodara
Creation Date  : 02/25/2018
Updation Date  : 03/01/2018
Version        : 1.0
Description    :
This program reads data from the view : project_activities and updates the Overview sheet.

Functions:
Main Function - To write the overview sheet
writeActivityData - To write the individual activity sheets - Only the structural data

Files need to run this program:
dib_utilities : To get the connection details and executing query.
excel_config_reader.py - to get the details of excel sheet to be written to
excel_activity_config.ini - configuration file for all the cell positions for output to be written to

'''

import io
import sys
import datetime
import psycopg2
import xlsxwriter
import db_utilities as dbu
import excel_config_reader as ecr
import utilities as util

con = None
total_activities = 0
last_activity_row = 0
activity_name = []
activity_id = []
finalList = []


#---- Activity data write ----------------------------------------------------#
# This function accepts the workbook, activityID, activityName and List data  #
# from the main program.                                                      #
# Then it creates individual sheets for each activity and writes data         #
#-----------------------------------------------------------------------------#-
def writeActivityData(wb,actId,actName,dataList):
    # first get the activity id from the activity data
    # first iterate through the actId list and get the first
    con = dbu.getConn() # get the connection details from db_utilities
    cur = con.cursor()  # create a cursor object
    print(actId)
    print(actName)
    for i in range(0,len(actId)):
        # now get the first activityID
        recList = []
        LactId = actId[i]
        LactName = actName[i]
        SheetName = LactName + "_" + str(LactId) #- creating a name for each sheet
        print(SheetName)
        # --- Create a new worksheet with name
        worksheet = wb.add_worksheet(SheetName)
        print('ACTIVITY NAME = %s' %actName[i],format_1)
        # write the activity name ------
        worksheet.write(ecr.getPrint_ActSheet_ActivityName_Heading()[0],ecr.getPrint_ActSheet_ActivityName_Heading()[1], 'ACTIVITY NAME', format)
        worksheet.write(ecr.getPrint_ActSheet_ActivityName_Value()[0],ecr.getPrint_ActSheet_ActivityName_Value()[1], LactName.upper(), format)
        worksheet.write(ecr.getPrint_ActSheet_ActivityID_Heading()[0],ecr.getPrint_ActSheet_ActivityID_Heading()[1], 'ACTIVITY ID', format)
        worksheet.write(ecr.getPrint_ActSheet_ActivityID_Value()[0],ecr.getPrint_ActSheet_ActivityID_Value()[1], dataList[i][0], format)
        worksheet.write(ecr.getPrint_ActSheet_ContractorName_Heading()[0],ecr.getPrint_ActSheet_ContractorName_Heading()[1], 'CONTRACTOR', format)
        worksheet.write(ecr.getPrint_ActSheet_ContractorName_Value()[0],ecr.getPrint_ActSheet_ContractorName_Value()[1], dataList[i][7], format)
        worksheet.write(ecr.getPrint_ActSheet_UnitName_Heading()[0],ecr.getPrint_ActSheet_UnitName_Heading()[1], 'UNIT', format)
        worksheet.write(ecr.getPrint_ActSheet_UnitName_Value()[0],ecr.getPrint_ActSheet_UnitName_Value()[1], dataList[i][5], format)

        #writing details into the activity sheet
        # setting the column widths
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)


        #writing the column headings
        worksheet.write(ecr.getPrint_Across_ActSheet_ActivityID_Heading()[0],ecr.getPrint_Across_ActSheet_ActivityID_Heading()[1], 'ACTIVITY ID', green_color_format)
        worksheet.write(ecr.getPrint_Across_ActSheet_Date_Heading()[0],ecr.getPrint_Across_ActSheet_Date_Heading()[1], 'DATE', green_color_format)
        worksheet.write(ecr.getPrint_Across_ActSheet_Installed_Heading()[0],ecr.getPrint_Across_ActSheet_Installed_Heading()[1], 'INSTALLED', green_color_format)
        worksheet.write(ecr.getPrint_Across_ActSheet_CompletedToday_Heading()[0],ecr.getPrint_Across_ActSheet_CompletedToday_Heading()[1], 'COMPLETED TODAY', green_color_format)
        worksheet.write(ecr.getPrint_Across_ActSheet_CompletedToDate_Heading()[0],ecr.getPrint_Across_ActSheet_CompletedToDate_Heading()[1], 'COMPLETE TO DATE', green_color_format)
        worksheet.write(ecr.getPrint_Across_ActSheet_PlannedToDate_Heading()[0],ecr.getPrint_Across_ActSheet_PlannedToDate_Heading()[1], 'PLANNED TO DATE', green_color_format)

## --------------End of function writeActivityData() --------------------------------------------
def openFile(output):
    try:
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    except FileNotFoundError as FOF:
        print('File Not found.<line 102>: openFile()..' %FOF)
    finally:
        return workbook

def openDatabaseConnection():
    try:
        con = dbu.getConn()
    except psycopg2.DatabaseError as error:
        print('Error Opening Database connection...<line 110>: openDatabaseConnection()' %error)
        sys.exit(1)
    finally:
        return con

def printOverviewHeaders():
    try:
        totCol = int(ecr.getTotalWorkingColumn())
        for i in range(0, totCol):
            worksheet.write(0, i, '', green_color_format)

        # Get column positions to write the heading
        dtHeading = []
        dtHeading = ecr.getPrintDateTime()

        # --- Write the heading in overview sheet
        worksheet.write(dtHeading[0], dtHeading[1], 'TODAY IS: %s' % str(dateTime), green_color_format)
        worksheet.set_column('E:E', 40)
        worksheet.set_column('F:F', 30)
        worksheet.write(ecr.getPrintProjectName_Heading()[0], ecr.getPrintProjectName_Heading()[1], 'PROJECT', format)
        worksheet.write(ecr.getPrintProjectName_Value()[0], ecr.getPrintProjectName_Value()[1], str(finalList[0][2]))
        worksheet.write(ecr.getPrintProjectID_Heading()[0], ecr.getPrintProjectID_Heading()[1], 'PROJECT#', format)
        worksheet.write(ecr.getPrintProjectID_Value()[0], ecr.getPrintProjectID_Value()[1], str(finalList[0][1]))
        worksheet.write(ecr.getPrint_ContractorName_Heading()[0], ecr.getPrint_ContractorName_Heading()[1],
                        'SUBCONTRACTOR', format)
        worksheet.write(ecr.getPrint_ContractorName_Value()[0], ecr.getPrint_ContractorName_Value()[1],
                        str(finalList[0][7]))
        worksheet.write(ecr.getPrint_Updated_Heading()[0], ecr.getPrint_Updated_Heading()[1], 'UPDATED', format)
        worksheet.write(ecr.getPrint_Updated_Value()[0], ecr.getPrint_Updated_Value()[1], str(dateTime))
    except Exception as e:
        print('Error while writing Overview Heading <line 140>: printOverviewHeaders()...%s' %e)

def printOverviewActivityHeading():
    try:
        worksheet.set_column(ecr.getPrint_ActivityID_Heading()[0], ecr.getPrint_ActivityID_Heading()[1], 10)
        worksheet.write(ecr.getPrint_ActivityID_Heading()[0], ecr.getPrint_ActivityID_Heading()[1], 'ACTIVITY ID',format)
        worksheet.set_column(ecr.getPrint_ActivityName_Heading()[0], ecr.getPrint_ActivityName_Heading()[1], 30)
        worksheet.write(ecr.getPrint_ActivityName_Heading()[0], ecr.getPrint_ActivityName_Heading()[1], 'ACTIVITIES',format)
        worksheet.set_column(ecr.getPrint_TotalQuantities_Heading()[0], ecr.getPrint_TotalQuantities_Heading()[1], 15)
        worksheet.write(ecr.getPrint_TotalQuantities_Heading()[0], ecr.getPrint_TotalQuantities_Heading()[1],'TOTAL QUANTITIES', format)
        worksheet.set_column(ecr.getPrint_UnitID_Heading()[0], ecr.getPrint_UnitID_Heading()[1], 7)
        worksheet.write(ecr.getPrint_UnitID_Heading()[0], ecr.getPrint_UnitID_Heading()[1], 'UNIT ID', format)
        worksheet.write(ecr.getPrint_UnitName_Heading()[0], ecr.getPrint_UnitName_Heading()[1], 'UNITS', format)
        worksheet.set_column(ecr.getPrint_Planned_Heading()[0], ecr.getPrint_Planned_Heading()[1], 15)
        worksheet.write(ecr.getPrint_Planned_Heading()[0], ecr.getPrint_Planned_Heading()[1], 'PLANNED', format)
        worksheet.set_column(ecr.getPrint_Actual_Heading()[0], ecr.getPrint_Actual_Heading()[1], 15)
        worksheet.write(ecr.getPrint_Actual_Heading()[0], ecr.getPrint_Actual_Heading()[1], 'ACTUAL', format)
    except Exception as e:
        print('Error while writing activity header in overview <line 158> :printOverviewActivityHeading() ..%s' %e)

def writeActivityDetails():
    try:
        global last_activity_row
        j = int(ecr.getPrint_Activity_Heading())
        for i in range(0, total_activities):
            col = 0
            worksheet.write(j, col, finalList[i][0], format_1)
            worksheet.write(j, col + 1, finalList[i][3], format_1)
            worksheet.write(j, col + 3, finalList[i][4], format_1)
            worksheet.write(j, col + 4, finalList[i][5], format_1)
            # Draw the grey color in between the activities
            for k in range(0, 7):
                worksheet.write(j + 1, k, '', yellow_color_format)
            j = j + 2

        last_activity_row = j  # set the last row that was written to
    except Exception as e:
        print('Error while writing activity data details on overview sheet <line 177>: writeActivityDetails()...%s' %e)

def writeActivityOverview():
    try:
        global  last_activity_row
        for i in range(0, total_activities):
            last_activity_row = last_activity_row + 1
            for k in range(0, 7):
                worksheet.write(k, last_activity_row, '', green_color_format)
            worksheet.write(last_activity_row, 1, str(finalList[i][3]), green_color_format)
            last_activity_row = last_activity_row + 2

            # ---- Write the activity details
            worksheet.write(last_activity_row + 1, 1, 'SUBCONTRACTOR:', format)
            worksheet.write(last_activity_row + 1, 2, str(finalList[i][7]))
            last_activity_row = last_activity_row + 1

            worksheet.write(last_activity_row + 1, 1, 'MILESTONE START:', format)
            worksheet.write(last_activity_row + 1, 2, str(finalList[i][8]))
            last_activity_row = last_activity_row + 1

            worksheet.write(last_activity_row + 1, 1, 'MILESTONE END:', format)
            worksheet.write(last_activity_row + 1, 2, str(finalList[i][9]))
            last_activity_row = last_activity_row + 1
            # worksheet.write(6, 5, str(finalList[0][7]))
            worksheet.write(last_activity_row + 1, 1, 'PLANNED DAILY AVG.', format)
            last_activity_row = last_activity_row + 1
            worksheet.write(last_activity_row + 1, 1, 'ACTUAL DAILY AVG.', format)
            # last_activity_row = last_activity_row + 1
    except Exception as e:
        raise util.DLException(util.__FILE__(),util.__LINE__(), e)

## --------------------------Main Program starts --------------------------------------------------
try:
    rstList = []
    conn = openDatabaseConnection()
    cur = conn.cursor()
    cur1 = conn.cursor()
    cur.execute("SELECT DISTINCT ACTIVITY_ID,PROJ_ID,PROJ_NAME,ACTIVITY_NAME,UNIT_ID,UNIT_NAME,CONTRACTOR_ID,CONTRACTOR_NAME,PROJ_START,PROJ_END FROM TEMP.PROJECT_ACTIVITIES WHERE ACTIVITY_ID IS NOT NULL ORDER BY ACTIVITY_ID")
    cur1.execute("SELECT COUNT(*) FROM TEMP.PROJECT_ACTIVITIES WHERE ACTIVITY_ID IS NOT NULL")

    try:
        # raise the exception if there is no data fetch from the database
        # Throw user-defined exception
        lrow = cur1.fetchone()
        if lrow[0] == 0:
            raise util.DLException(util.__FILE__(), util.__LINE__(),'No data in view project_activities')
    except Exception as e:
        raise util.DLException(util.__FILE__(), util.__LINE__(),e)
    # check whether records received from database based on the query
    while True:
        row = cur.fetchone()
        rstList = []
        if row == None:
            break

        try:
            rstList.append(row[0]) #- Activity ID
            if row[0] == "":
                raise MyException('<line 236> Main(): Null Value in ActivityID' %row[0])
        except MyException as e:
            print('Activity ID cannot be null ',e.value)
        rstList.append(row[1]) #- Project ID
        rstList.append(row[2]) #- Project Name
        rstList.append(row[3]) #- Activity Name
        rstList.append(row[4]) #- Unit ID
        rstList.append(row[5]) #- Unit Name
        rstList.append(row[6]) # Contractor ID
        rstList.append(row[7]) #- Contractor Name
        rstList.append(row[8]) # Project Start
        rstList.append(row[9]) #- Project End

        activity_id.append(row[0]) #- add the activity id to the list
        activity_name.append(row[3]) #- add the activity_name to the list
        finalList.append(rstList)
        #print("ProjectID: " + row[1] + "\t\tProjectName: " + str(row[2]))
    print (finalList)
    total_activities = len(finalList)

    # Create excel workbook using xlswriter
    output = io.BytesIO()
    workbook = openFile(output)

    # create the first sheet - Overview
    sheetN = ecr.getOverviewSheetName()
    worksheet = workbook.add_worksheet(sheetN)
    worksheet = workbook.get_worksheet_by_name(sheetN)

    # --- Create excel sheets inside workbook ----- #
    # first get the number of activities
    # --- Printing date and time in 1st cell
    dateTime = datetime.datetime.now().date()
    totCol = int(ecr.getTotalWorkingColumn())

    #Create format templates to be used in cells
    form_at = workbook.add_format()
    format = workbook.add_format({'bold': True, 'font_color': 'black', 'align':'center' ,'font_size': 10})
    format_1 = workbook.add_format({'font_color': 'black', 'align': 'center', 'font_size': 10})
    green_color_format = workbook.add_format({'fg_color': '#58D68D'})
    yellow_color_format = workbook.add_format({'bg_color': '#F7DC6F'})

    # create the background color to green
    # Writing the overview project header
    printOverviewHeaders()

    ## Project Summary heading
    # Color the cell with green
    for i in range(0,totCol):
        worksheet.write(8,i,'', green_color_format)
    # printing the project summary heading
    worksheet.write(ecr.getPrint_ProjectSummary_Heading()[0],ecr.getPrint_ProjectSummary_Heading()[1], 'PROJECT SUMMARY',green_color_format)

    #--- Now write the heading for activities-------------------------
    printOverviewActivityHeading()

    # --- Write the activity list from the list and color the subsequent row with magenta color
    writeActivityDetails()
    # ---- Print the details on the cells based on the resultList
    writeActivityOverview()

    ## ------- Writing the individual sheet - Activity data ---------------
    for i in range(0, 1):
        writeActivityData(workbook,activity_id,activity_name,finalList)

    # close the workbook
    #workbook.close()

except psycopg2.DatabaseError as error:
    print (error)
    if con:
        con.rollback()

    print
    'Error %s' % psycopg2.DatabaseError
    sys.exit(1)

finally:
    if con:
        #print (total_activities)
        con.close()
    workbook.close()
    #xcl_data = output.getvalue()
    output.seek(0)
    try:
        with open("demo.xlsx", 'wb') as out:  ## Open temporary file as bytes
            out.write(output.getvalue())
    except Exception as e:
        print('Error in <line 324> while writing to demo.xlsx : main()>', e)
## ------------- End of Program ----------------------