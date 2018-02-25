'''
File Name      : writeOutputExcel.py
Author Name    : Lakshmi Damodara
Creation Date  : 02/25/2018
Updation Date  : 02/25/2018
Version        : 1.0
Description    :
This program reads data from the view : project_activities and updates the Overview sheet.
Then it reads the activity_data table to write the data to individual activity sheets.

Functions:
Main Function - To write the overview sheet
writeActivityData - To write the individual activity sheets

Files need to run this program:
dib_utilities : To get the connection details and executing query.

'''

import sys
import datetime
import psycopg2
import xlsxwriter
import db_utilities as dbu

con = None
total_activities = 0
last_activity_row = 0
activity_name = []
activity_id = []

#---- Activity data write ----------------------------------------------------#
# This function accepts the workbook, activityID, activityName and List data  #
# from the main program.                                                      #
# Then it creates individual sheets for each activity and writes data         #
#-----------------------------------------------------------------------------#-
def writeActivityData(wb,actId,actName,Llist):
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
        print('Activity Name = %s' %actName[i])
        # write the activity name ------
        worksheet.write(4, 4, LactName, format)

        #writing the column headings
        worksheet.write(6, 0, 'ACTIVITY ID', format)
        worksheet.write(6, 1, 'DATE', format)
        worksheet.write(6, 2, 'INSTALLED', format)
        worksheet.write(6, 3, 'COMPLETED TODAY', format)
        worksheet.write(6, 4, 'COMPLETE TO DATE', format)
        worksheet.write(6, 5, 'PLANNED TO DATE', format)

        # -- First get the count of records for the particular activity
        LsqlCountQuery = "SELECT COUNT(*) FROM TEMP.ACTIVITY_DATA WHERE ACTIVITY_ID = %s" % LactId
        cur.execute(LsqlCountQuery)
        rec_cnt = 0
        # get the total count of records
        for rec in cur:
            rec_cnt = rec
        print('record count %s' %rec_cnt[0])
        # now iterate through the activity_data table to get the activity data details
        LsqlQuery = "SELECT ACTIVITY_ID,DATE,ACTUAL_HOURS,ACTUAL_UNITS, PLANNED_HOURS, PLANNED_UNITS FROM TEMP.ACTIVITY_DATA WHERE ACTIVITY_ID = %s ORDER BY DATE" %LactId
        print(LsqlQuery)
        cur.execute(LsqlQuery)

        for record in cur:
            recList.append(record[0])
            recList.append(record[1])
            recList.append(record[2])
            recList.append(record[3])
            recList.append(record[4])
            recList.append(record[5])
            # The entire set of record is stored as 1 list.
        print(recList)

        # Writing the values to the sheet from Activity_Data
        # Adding 8 to iterate through the entire records
        # as we are starting out count from 8 - rows to be printed
        recCount = rec_cnt[0] + 8
        for i in range(8,recCount): # - positioning the row from 8th
            for j in range(0,6):  # writing the column data
                if j == 1:
                    dt = datetime.datetime.strptime(str(recList[j]),'%Y-%m-%d').date().strftime('%m-%d-%Y')
                    worksheet.write(i,j,str(dt))
                else:
                    worksheet.write(i, j, recList[j])
            n =6
            del recList[:n] # after writing into excel, delete first 6 items from list for each iteration

    con.close() # - close the connection of DB

## --------------End of function writeActivityData() --------------------------------------------

## --------------------------Main Program starts --------------------------------------------------
try:
    rstList = []
    finalList = []
    con = dbu.getConn()
    cur = con.cursor()
    cur.execute("SELECT DISTINCT ACTIVITY_ID,PROJ_ID,PROJ_NAME,ACTIVITY_NAME,UNIT_ID,UNIT_NAME,CONTRACTOR_ID,CONTRACTOR_NAME,PROJ_START,PROJ_END FROM TEMP.PROJECT_ACTIVITIES ORDER BY ACTIVITY_ID")

    while True:
        row = cur.fetchone()
        rstList = []
        if row == None:
            break

        #print("ProjID: " + str(row[0]) + "\t\tProjName: " + str(row[1] + "\t\tAName: " + str(row[2])))
        rstList.append(row[0]) #- Activity ID
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
    workbook = xlsxwriter.Workbook('demo.xlsx')
    # create the first sheet - Overview
    worksheet = workbook.add_worksheet('Overview')
    worksheet = workbook.get_worksheet_by_name('Overview')

    # --- Create excel sheets inside workbook ----- #
    # first get the number of activities
    # --- Printing date and time in 1st cell
    dateTime = datetime.datetime.now().date()
    print('Today is : %s' %dateTime)

    #Create format templates to be used in cells
    form_at = workbook.add_format()
    format = workbook.add_format({'bold': True, 'font_color': 'black', 'align':'center' ,'font_size': 10})
    format_1 = workbook.add_format({'font_color': 'black', 'align': 'center', 'font_size': 9})
    green_color_format = workbook.add_format({'fg_color': '#708090'})
    yellow_color_format = workbook.add_format({'bg_color': '#D3D3D3'})

    # create the background color to green
    for i in range(0,8):
        worksheet.write(0,i,'', green_color_format)

    # --- Write the heading in overview sheet
    worksheet.write(0, 0, 'Today is : %s'%str(dateTime),green_color_format)
    worksheet.set_column('E:E',40)
    worksheet.set_column('F:F', 30)
    worksheet.write(4,4,'PROJECT',format)
    worksheet.write(4,5,str(finalList[0][2]))
    worksheet.write(5, 4, 'PROJECT#',format)
    worksheet.write(5, 5, str(finalList[0][1]))
    worksheet.write(6, 4, 'SUBCONTRACTOR',format)
    worksheet.write(6, 5, str(finalList[0][7]))
    worksheet.write(7, 4, 'UPDATED',format)
    worksheet.write(7,5, str(dateTime))

    ## Project Summary heading
    #worksheet.merge_range('A9:I9', '', green_color_format)
    for i in range(0,8):
        worksheet.write(8,i,'', green_color_format)

    worksheet.write(8, 4, 'PROJECT SUMMARY',green_color_format)

    #--- Now write the heading for activities-------------------------
    worksheet.set_column(10,0,10)
    worksheet.write(10, 0, 'ACTIVITY ID', format)
    worksheet.set_column(10, 1, 30)
    worksheet.write(10,1,'ACTIVITIES',format)
    worksheet.set_column(10, 2, 15)
    worksheet.write(10,2, 'TOTAL QUANTITIES',format)
    worksheet.set_column(10, 3, 7)
    worksheet.write(10, 3, 'UNIT ID', format)
    #worksheet.set_column(10, 4, 10)
    worksheet.write(10, 4, 'UNITS', format)
    worksheet.set_column(10, 5, 15)
    worksheet.write(10, 5, 'PLANNED', format)
    worksheet.set_column(10, 6, 15)
    worksheet.write(10, 6, 'ACTUAL', format)

    # --- Write the activity list from the list and color the subsequent row with magenta color
    j = 11
    for i in range(0, total_activities):
        col = 0
        worksheet.write(j, col, finalList[i][0],format_1)
        worksheet.write(j,col+1,finalList[i][3],format_1)
        worksheet.write(j, col + 3, finalList[i][4],format_1)
        worksheet.write(j, col + 4, finalList[i][5],format_1)
        # Draw the grey color in between the activities
        for k in range(0,7):
            worksheet.write(j+1,k,'',yellow_color_format)
        j = j+2
    last_activity_row = j # set the last row that was written to

    # ---- Print the details on the cells based on the resultList
    for i in range(0,total_activities):
        last_activity_row = last_activity_row + 1
        for k in range(0,7):
            worksheet.write(k,last_activity_row,'',green_color_format)
        worksheet.write(last_activity_row,1,str(finalList[i][3]),green_color_format)
        last_activity_row = last_activity_row + 2

        # ---- Write the activity details
        worksheet.write(last_activity_row +1, 1, 'SUBCONTRACTOR:', format)
        worksheet.write(last_activity_row +1, 2, str(finalList[i][7]))
        last_activity_row = last_activity_row + 1

        worksheet.write(last_activity_row +1, 1, 'MILESTONE START:', format)
        worksheet.write(last_activity_row + 1, 2, str(finalList[i][8]))
        last_activity_row = last_activity_row + 1

        worksheet.write(last_activity_row +1, 1, 'MILESTONE END:', format)
        worksheet.write(last_activity_row + 1, 2, str(finalList[i][9]))
        last_activity_row = last_activity_row + 1
        #worksheet.write(6, 5, str(finalList[0][7]))
        worksheet.write(last_activity_row +1, 1, 'PLANNED DAILY AVG.', format)
        last_activity_row = last_activity_row + 1
        worksheet.write(last_activity_row + 1, 1, 'ACTUAL DAILY AVG.', format)
        #last_activity_row = last_activity_row + 1

    ## ------- Writing the individual sheet - Activity data ---------------
    for i in range(0, 1):
        writeActivityData(workbook,activity_id,activity_name,finalList)


except psycopg2.DatabaseError :
    if con:
        con.rollback()

    print
    'Error %s' % psycopg2.DatabaseError
    sys.exit(1)

finally:
    if con:
        print (total_activities)
        workbook.close()
        con.close()