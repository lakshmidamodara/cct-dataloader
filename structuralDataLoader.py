'''
File Name      : structuralDataLoader.py
Author Name    : Lakshmi Damodara
Creation Date  : 02/26/2018
Updated on     :
Version        : 1.0
Description    :
     This program calls functions to read JSON Object data stream and loads structural data into
     projects, phases, bundles, units and activities etc tables
'''

import json
import sys
import psycopg2
import db_utilities as dbu
import utilities as util
import traceback

# --------------------------------------------------------#
# Function to group the duplicate keys from JSON file     #
# This function is run first after opening the JSON file  #
# If this function is not run, python will not allow      #
# duplicate keys. The last item will be overwritten       #
#---------------------------------------------------------#
def join_duplicate_keys(ordered_pairs):
    try:
        d = {}
        for k, v in ordered_pairs:
            if k in d:
               if type(d[k]) == list:
                   d[k].append(v)
               else:
                   newlist = []
                   newlist.append(d[k])
                   newlist.append(v)
                   d[k] = newlist
            else:
               d[k] = v
        return d
    except Exception as error:
        pass

def getItemsParentLevel(lengthList,node):
    try:
        itemVar =""
        lengthList = len(d)
        for i in range(0,lengthList):
            itemVar = d[i][node]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        pass

def getItemsChildLevel(node1,node2):
    try:
        itemVar =""
        lengthList = len(d)
        for i in range(0,lengthList):
            itemVar = d[i][node1][node2]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        pass

def getItemsChildLevel_List(lengthList,node1,node2,iterationVal):
    try:
        itemVar =""
        lengthList = len(d)
        for i in range(0,lengthList):
            itemVar = d[i][node1][iterationVal][node2]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        pass

def getItemsSubChildLevel(node1,node2,node3):
    try:
        itemVar =""
        lengthList = len(d)
        for i in range(0,lengthList):
            itemVar = d[i][node1][node2][node3]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        pass

def getItemsSubChildLevel_List(lengthList,node1,node2,node3,iterationVal):
    try:
        itemVar =""
        lengthList = len(d)
        for i in range(0,lengthList):
            itemVar = d[i][node1][node2][iterationVal][node3]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        pass


# -------------- Function to get the project details ---------------------

def getProjectName():
    try:
        project_name = getItemsChildLevel("project","name")
    except Exception as error:
        pass
    else:
        return project_name

def getPortfolioDetails():
        portfolio_name = "Default"
        try:
            ## Update the details to the database temp
            connObj = dbu.getConn()

            # --------------------------------------------------------
            # Insert data to profolios table
            # --------------------------------------------------------

            execSQL = ('insert_portfolios_data')
            execData = (portfolio_name,0)
            portfolio_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
            return portfolio_id
        except psycopg2.DatabaseError as error:
            print("Database Error %s " % error)
            raise
        except Exception as error:
            print("Error %s " % error)
            raise
        else:
            connObj.close()
        finally:
            print("getPortfolioDetails")


def getProjectDetails(portfolio_id):
    try:
        # Get the project level details from the json file
        project_name = getItemsChildLevel("project", "name")
        project_start_date = getItemsChildLevel("project", "start")
        project_end_date = getItemsChildLevel("project", "end")
        project_workdays = getItemsChildLevel("project", "workdays")
        project_budget = getItemsChildLevel("project", "budget")
        project_loc_street1 = getItemsSubChildLevel("project", "location", "street1")
        project_loc_street2 = getItemsSubChildLevel("project", "location", "street2")
        project_loc_city = getItemsSubChildLevel("project", "location", "city")
        project_loc_state = getItemsSubChildLevel("project", "location", "state")
        project_loc_postal = getItemsSubChildLevel("project", "location", "postal")
        project_loc_country = getItemsSubChildLevel("project", "location", "country")
        proj_loc_street = project_loc_street1 + " " + project_loc_street2

        print(project_workdays)
    except Exception as error:
        print( "Error %s in %s at %d" %(error, util.__FILE__(), util.__LINE__()))
        raise
    try:
        ## Update the details to the database temp
        connObj = dbu.getConn()

        # --------------------------------------------------------
        # Insert data to location table and get location id
        # --------------------------------------------------------
        start_date = util.formatDate(project_start_date)
        end_date = util.formatDate(project_end_date)

        execSQL = ('insert_location_data')
        execData = (proj_loc_street, project_loc_city, project_loc_state, project_loc_country,None, None)
        project_loc_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
        print( "location id is")
        print (project_loc_id)

        execSQL = ('insert_project_data')
        execData = (project_name, start_date, end_date, json.dumps(project_workdays),int(project_budget),None, project_loc_id, None)
        project_id = dbu.fetchStoredFuncRes(connObj, execSQL,execData)[0]

        ## create a row in portfolio_projects to tie both portfolio and the project
        execSQL = ('insert_portfolio_projects_data')
        execData = (portfolio_id, project_id)
        portfolio_project_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        return project_id
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("getProjectDetails")

# -------------- Function to get the contractor details -----OLD CODE------------------
def getContractorDetails():
    try:
        lengthList = len(d)
        ## Update the details to the database temp
        connObj = dbu.getConn()
        #contractor_type = (type(d[lengthList -1]["contractors"]))
        for i in range(0,len(d[lengthList -1]["contractors"])):
            # Get the project level details from the json file
            contractor_name = d[lengthList-1]["contractors"][i]["name"]
            contractor_email = d[lengthList-1]["contractors"][i]["email"]
            contractor_phone = d[lengthList-1]["contractors"][i]["phone"]
            contractor_pcontact = d[lengthList-1]["contractors"][i]["primary_contact"]

            # --------------------------------------------------------
            # Insert data to public.contractors
            # --------------------------------------------------------
            execSQL = ('insert_contractor_data')
            execData = (contractor_name, contractor_email, contractor_phone, contractor_pcontact)
            contractor_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]


        #return contractor_id
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("getContractorDetails")

# -------------- Function to get the contractor details -----OLD CODE ENDS---------------

# -------------- Function to get the contractor details ----NEW CODE BEGINS-------------------

def getContractorDetails_List():
    try:
        connObj = dbu.getConn()
        lengthList = len(d)
        for i in range(0,len(d[lengthList -1]["contractors"])):
            # Get the project level details from the json file
            contractor_name = d[lengthList-1]["contractors"][i]["name"]
            contractor_email = d[lengthList-1]["contractors"][i]["email"]
            contractor_phone = d[lengthList-1]["contractors"][i]["phone"]
            contractor_pcontact = d[lengthList-1]["contractors"][i]["primary_contact"]

            # --------------------------------------------------------
            # Insert data to public.contractors
            # --------------------------------------------------------
            execSQL = ('insert_contractor_data')
            execData = (contractor_name, contractor_email, contractor_phone, contractor_pcontact)
            contractor_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("getContractorDetails_List")

def getContractorDetails_Dict():
    try:
        ## Update the details to the database temp
        connObj = dbu.getConn()
        # Get the project level details from the json file
        contractor_name = getItemsChildLevel("contractors","name")
        contractor_email = getItemsChildLevel("contractors","email")
        contractor_phone = getItemsChildLevel("contractors","phone")
        contractor_pcontact = getItemsChildLevel("contractors","primary_contact")

        # --------------------------------------------------------
        # Insert data to public.contractors
        # --------------------------------------------------------
        execSQL = ('insert_contractor_data')
        execData = (contractor_name, contractor_email, contractor_phone, contractor_pcontact)
        contractor_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]


    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("getContractorDetails_Dict")


# -------------- Function to get the Material details -----------------------
def getMaterialDetails_List():
    try:
        lengthList = len(d)
        ## Update the details to the database temp
        #connObj = dbu.getConn()
        for i in range(0,len(d[lengthList -1]["materials"])):
        #for i in range(0, item_contractors):
            # Get the project level details from the json file
            mat_name = d[lengthList-1]["materials"][i]["name"]
            mat_plan_delivery = d[lengthList-1]["materials"][i]["planned_delivery"]
            mat_actual_delivery = d[lengthList-1]["materials"][i]["actual_delivery"]
            mat_unit_cost = d[lengthList-1]["materials"][i]["unit_cost"]

            # # --------------------------------------------------------
            # # First truncate the data from project and location table
            # # --------------------------------------------------------
            # LsqlQuery = "TRUNCATE TABLE TEMP.MATERIALS"
            # #dbu.executeQueryString(LsqlQuery, connObj)
            #
            # # --------------------------------------------------------
            # # Insert data to project and location table
            # # --------------------------------------------------------
            # execSQL = "INSERT INTO TEMP.MATERIALS(NAME,PLANNED_DELIVERY,ACTUAL_DELIVERY,UNIT_COST) VALUES (%s,%s,%s,%s);"
            # execData = (mat_name,mat_plan_delivery, mat_actual_delivery, mat_unit_cost)
            # print(execSQL,execData)
            #dbu.executeSQLData(execSQL, execData, connObj)

        #connObj.close()
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise

def getMaterialDetails_Dict():
    try:
        ## Update the details to the database temp
        #connObj = dbu.getConn()
        # Get the project level details from the json file
        mat_name = getItemsChildLevel("materials","name")
        mat_plan_delivery = getItemsChildLevel("materials","planned_delivery")
        mat_actual_delivery = getItemsChildLevel("materials","actual_delivery")
        mat_unit_cost = getItemsChildLevel("materials","unit_cost")

        # # --------------------------------------------------------
        # # First truncate the data from project and location table
        # # --------------------------------------------------------
        # LsqlQuery = "TRUNCATE TABLE TEMP.MATERIALS"
        # #dbu.executeQueryString(LsqlQuery, connObj)
        #
        # # --------------------------------------------------------
        # # Insert data to project and location table
        # # --------------------------------------------------------
        # execSQL = "INSERT INTO TEMP.MATERIALS(NAME,PLANNED_DELIVERY,ACTUAL_DELIVERY,UNIT_COST) VALUES (%s,%s,%s,%s);"
        # execData = (mat_name,mat_plan_delivery, mat_actual_delivery, mat_unit_cost)
        # print(execSQL,execData)
        #dbu.executeSQLData(execSQL, execData, connObj)

        #connObj.close()
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise

# -------------- Function to get the Incident details -----------------------
def getIncidentDetails_List():
    try:
        lengthList = len(d)
        ## Update the details to the database temp
        #connObj = dbu.getConn()
        for i in range(0,len(d[lengthList -1]["incidents"])):
        #for i in range(0, item_contractors):
            # Get the project level details from the json file
            incident_date = d[lengthList-1]["incidents"][i]["date"]
            incident_type = d[lengthList-1]["incidents"][i]["type"]
            incident_class = d[lengthList-1]["incidents"][i]["class"]
            incident_contractor = d[lengthList-1]["incidents"][i]["contractor"]

            # # --------------------------------------------------------
            # # First truncate the data from project and location table
            # # --------------------------------------------------------
            # LsqlQuery = "TRUNCATE TABLE TEMP.INCIDENTS"
            # #dbu.executeQueryString(LsqlQuery, connObj)
            #
            # # --------------------------------------------------------
            # # Insert data to project and location table
            # # --------------------------------------------------------
            # execSQL = "INSERT INTO TEMP.INCIDENTS(DATE,TYPE,CLASS,CONTRACTOR) VALUES (%s,%s,%s,%s);"
            # execData = (incident_date,incident_type, incident_class, incident_contractor)
            # print(execSQL,execData)
            #dbu.executeSQLData(execSQL, execData, connObj)

        #connObj.close()
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise

def getIncidentDetails_Dict():
    try:
        ## Update the details to the database temp
        #connObj = dbu.getConn()
        # Get the project level details from the json file
        incident_date = getItemsChildLevel("incidents","date")
        incident_type = getItemsChildLevel("incidents","type")
        incident_class = getItemsChildLevel("incidents","class")
        incident_contractor = getItemsChildLevel("incidents","contractor")

        # # --------------------------------------------------------
        # # First truncate the data from project and location table
        # # --------------------------------------------------------
        # LsqlQuery = "TRUNCATE TABLE TEMP.INCIDENTS"
        # #dbu.executeQueryString(LsqlQuery, connObj)
        #
        # # --------------------------------------------------------
        # # Insert data to project and location table
        # # --------------------------------------------------------
        # execSQL = "INSERT INTO TEMP.INCIDENTS(DATE,TYPE,CLASS,CONTRACTOR) VALUES (%s,%s,%s,%s);"
        # execData = (incident_date, incident_type, incident_class, incident_contractor)
        # print(execSQL,execData)
        #dbu.executeSQLData(execSQL, execData, connObj)

        #connObj.close()
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise

# -------------------------------END of INCIDENTS ---- NEW CODE ENDS -------------------------

def writeActivitiesData_MultipleActivities(project_id):
    try:
        activityList = []
        connObj = dbu.getConn()

        node1 = "bundles"
        node2 = "activities"
        bundles_name = getItemsChildLevel( "bundles", "name")
        bundles_phases = getItemsChildLevel( "bundles", "phases")

        execSQL = ('insert_bundles_data')
        execData = (None, bundles_name, project_id, None)
        bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        execSQL = ('insert_phases_data')
        execData = (bundles_phases, None, None, None, None)
        phase_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        for i in range(0, len(item_activities)):
            activities_name = getItemsSubChildLevel_List(len(d),node1,node2,"name",i)
            activities_contractor = getItemsSubChildLevel_List(len(d), node1,node2, "contractor",i)
            activities_total_planned_hours = getItemsSubChildLevel_List(len(d),node1,node2, "total_planned_hours",i)
            activities_total_planned_units = getItemsSubChildLevel_List(len(d),node1,node2, "total_planned_units",i)
            activities_planned_start = getItemsSubChildLevel_List(len(d), node1,node2, "planned_start",i)
            activities_planned_end = getItemsSubChildLevel_List(len(d),node1,node2, "planned_end",i)
            activities_actual_start = getItemsSubChildLevel_List(len(d), node1,node2, "actual_start",i)
            activities_actual_end = getItemsSubChildLevel_List(len(d), node1,node2, "actual_end",i)

            activities_unit_name = d[len(d) -1]["bundles"]["activities"][i]["unit"]["name"]
            execSQL = ('insert_units_data')
            execData = (activities_unit_name,0)
            unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
            print ('units id is ')
            print (unit_id)

            activities_material = getItemsSubChildLevel_List(len(d), "bundles", "activities", "material",i)

            # --------------------------------------------------------
            # Insert data to project and location table
            # --------------------------------------------------------
            planned_start = util.formatDate(activities_planned_start)
            planned_end = util.formatDate(activities_planned_end)
            actual_start = util.formatDate(activities_actual_start)
            actual_end = util.formatDate(activities_actual_end)
            prj_name = getProjectName()

            execSQL = ('insert_activities_data')
            execData = (activities_name, unit_id, activities_contractor, None, activities_total_planned_hours, phase_id,
                        project_id, activities_total_planned_units, planned_start, planned_end, activities_unit_name,
                        actual_start, actual_end, None)
            print(execData)
            activities_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]


            print('#####################')
            print(execSQL)
            print(execData)
            print('writing values')
            print('Bundle Name : %s' %bundles_name)
            print('Bundle Phases : %s' %bundles_phases)
            print ('Activity Name : %s' %activities_name)
            print ('Activities_id : %d' %activities_id)
            print ('Activity Unit Name : %s' %activities_unit_name)
            print ('Activity Material: %s' %activities_material)
            print('#####################')
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("writeActivitiesData_MultipleActivities")

def getItems_MultiBundle_MultiActivity(node1,node2,node3,iterationVal_h,iterationVal_i):
    try:
        itemVar =""
        for i in range(0,len(d)):
            itemVar = d[i][node1][iterationVal_h][node2][iterationVal_i][node3]
            #print(itemVar)
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        print("Error %s " % error)
        raise
    finally:
        print("getItems_MultiBundle_MultiActivity")

def writeActivitiesData_MultiBundles_MultipleActivities(bundle_item, project_id):
    try:
        activityList = []
        node1 = "bundles"
        node2 = "activities"
        ## Update the details to the database temp
        connObj = dbu.getConn()

        #write the values of bundles
        bundles_name = d[len(d) -1][node1][bundle_item]["name"]
        bundles_phases = d[len(d) -1][node1][bundle_item]["phases"]

        execSQL = ('insert_bundles_data')
        execData = (None, bundles_name, project_id, None)
        bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        execSQL = ('insert_phases_data')
        execData = (bundles_phases, None, None, None, None)
        phase_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        #L_item_activities = d[lengthList - 1]["bundles"][bundle_item]["activities"]
        for i in range(0, len(item_activities)):
           activities_name = getItems_MultiBundle_MultiActivity(node1, node2, "name", bundle_item,i)
           activities_contractor = getItems_MultiBundle_MultiActivity(node1, node2, "contractor",bundle_item, i)
           activities_total_planned_hours = getItems_MultiBundle_MultiActivity(node1, node2, "total_planned_hours",bundle_item, i)
           activities_total_planned_units = getItems_MultiBundle_MultiActivity(node1, node2, "total_planned_units",bundle_item, i)
           activities_planned_start = getItems_MultiBundle_MultiActivity(node1, node2, "planned_start",bundle_item, i)
           activities_planned_end = getItems_MultiBundle_MultiActivity(node1, node2, "planned_end",bundle_item, i)
           activities_actual_start = getItems_MultiBundle_MultiActivity(node1, node2, "actual_start",bundle_item, i)
           activities_actual_end = getItems_MultiBundle_MultiActivity(node1, node2, "actual_end",bundle_item, i)

           activities_unit_name = d[len(d)-1]["bundles"][bundle_item]["activities"][i]["unit"]["name"]
           execSQL = ('insert_units_data')
           execData = (activities_unit_name,0)
           print(execData)
           print (execSQL)
           unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
           print('units id is ')
           print(unit_id)

           activities_material = getItems_MultiBundle_MultiActivity(node1, node2, "material",bundle_item, i)

           print(activities_planned_start)

           # --------------------------------------------------------
           # Insert data to project and location table
           # --------------------------------------------------------
           planned_start = util.formatDate(activities_planned_start)
           planned_end = util.formatDate(activities_planned_end)
           actual_start = util.formatDate(activities_actual_start)
           actual_end = util.formatDate(activities_actual_end)
           prj_name = getProjectName()

           execSQL = ('insert_activities_data')
           execData = (activities_name, unit_id, activities_contractor, None, activities_total_planned_hours, phase_id,
                       project_id, activities_total_planned_units, planned_start, planned_end, activities_unit_name,
                       actual_start, actual_end, None)
           print(execData)
           activities_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

           print('#####################-- MultiBundle-MultiActivity----')
           print(execSQL)
           print(execData)
           print('writing values')
           print('Bundle Name : %s' % bundles_name)
           print('Bundle Phases : %s' % bundles_phases)
           print('Activity ID : %d' %activities_id)
           print('Activity Name : %s' % activities_name)
           print('Activity Unit Name : %s' % activities_unit_name)
           print('Activity Material: %s' % activities_material)
           print('#####################')
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("writeActivitiesData_MultiBundles_MultipleActivities")


# -----------------------------------------------------------#
# This function is called when  bundles is a list  and
# activities  is dictionary                                #
#-----------------------------------------------------------#

def getwriteBundleList_DictActivity(node1,node2,node3,iterationVal):
    try:
        itemVar = ""
        for i in range(0, len(d)):
            itemVar = d[i][node1][iterationVal][node2][node3]
        if itemVar:
            return itemVar
        else:
            return None
    except Exception as error:
        print("Error %s " % error)
        raise
    finally:
        print("getwriteBundleList_DictActivity")

def writeBundleList_DictActivity(bundle_item, project_id):
    try:
        connObj = dbu.getConn()
        print('I am entering fn writeBundleList_DictActivity(i) ---')
        bundles_name = d[len(d) -1]["bundles"][bundle_item]["name"]
        bundles_phases = d[len(d) -1]["bundles"][bundle_item]["phases"]

        execSQL = ('insert_bundles_data')
        execData = (None, bundles_name, project_id, None)
        bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        execSQL = ('insert_phases_data')
        execData = (bundles_phases, None, None, None, None)
        phase_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        activities_name = getwriteBundleList_DictActivity("bundles","activities","name",bundle_item)
        activities_contractor = getwriteBundleList_DictActivity("bundles","activities", "contractor",bundle_item)
        activities_total_planned_hours = getwriteBundleList_DictActivity("bundles","activities", "total_planned_hours",bundle_item)
        activities_total_planned_units = getwriteBundleList_DictActivity("bundles","activities", "total_planned_units",bundle_item)
        activities_planned_start = getwriteBundleList_DictActivity("bundles", "activities", "planned_start",bundle_item)
        activities_planned_end = getwriteBundleList_DictActivity("bundles","activities", "planned_end",bundle_item)
        activities_actual_start = getwriteBundleList_DictActivity("bundles","activities", "actual_start",bundle_item)
        activities_actual_end = getwriteBundleList_DictActivity("bundles","activities", "actual_end",bundle_item)

        activities_unit_name = d[len(d)-1]["bundles"][bundle_item]["activities"]["unit"]["name"]
        execSQL = ('insert_units_data')
        execData = (activities_unit_name,0)
        unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
        print('units id is ')
        print(unit_id)

        activities_material = getwriteBundleList_DictActivity("bundles","activities", "material",bundle_item)

        # --------------------------------------------------------
        # Insert data to project and location table
        # --------------------------------------------------------
        planned_start = util.formatDate(activities_planned_start)
        planned_end = util.formatDate(activities_planned_end)
        actual_start = util.formatDate(activities_actual_start)
        actual_end =util.formatDate(activities_actual_end)
        prj_name = getProjectName()

        execSQL = ('insert_activities_data')
        execData = (activities_name, unit_id, activities_contractor, None, activities_total_planned_hours, phase_id,
                    project_id, activities_total_planned_units, planned_start, planned_end, activities_unit_name,
                    actual_start, actual_end, None)
        print(execData)
        activities_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]


        print('###############-- writeBundleList_DictActivity() --######')
        print('writing values')
        print('Bundle Name : %s' % bundles_name)
        print('Bundle Phases : %s' % bundles_phases)
        print('Activity Name : %s' % activities_name)
        print('Activity Unit Name : %s' % activities_unit_name)
        print('Activity Material: %s' % activities_material)
        print("Activities ID: %d" % activities_id)
        print('#####################')
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("writeBundleList_DictActivity")

# -----------------------------------------------------------#
# This function is called when both bundles and activities   #
# are dictionaries                                           #
# There is going to be only one entry in the list            #
# So directly read the values i.e: one bundle, one activity  #
#------------------------------------------------------------#
def writeBundle_Activity(project_id):
    try:
        ## Update the details to the database temp
        connObj = dbu.getConn()

        bundles_name = getItemsChildLevel("bundles","name")
        bundles_phases = getItemsChildLevel( "bundles", "phases")

        execSQL = ('insert_bundles_data')
        execData = (None, bundles_name, project_id, None)
        bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        execSQL = ('insert_phases_data')
        execData = (bundles_phases, None, None, None, None)
        phase_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

        activities_name = getItemsSubChildLevel("bundles","activities","name")
        activities_contractor = getItemsSubChildLevel("bundles", "activities", "contractor")
        activities_total_planned_hours = getItemsSubChildLevel("bundles", "activities", "total_planned_hours")
        activities_total_planned_units = getItemsSubChildLevel("bundles", "activities", "total_planned_units")
        activities_planned_start = getItemsSubChildLevel("bundles", "activities", "planned_start")
        activities_planned_end = getItemsSubChildLevel("bundles", "activities", "planned_end")
        activities_actual_start = getItemsSubChildLevel("bundles", "activities", "actual_start")
        activities_actual_end = getItemsSubChildLevel("bundles", "activities", "actual_end")

        activities_unit_name = d[len(d)-1]["bundles"]["activities"]["unit"]["name"]
        execSQL = ('insert_units_data')
        execData = (activities_unit_name,0)
        unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
        print('units id is ')
        print(unit_id)

        activities_material = getItemsSubChildLevel("bundles", "activities", "material")

        # --------------------------------------------------------
        # Insert data to activities
        # --------------------------------------------------------
        planned_start = util.formatDate(activities_planned_start)
        planned_end = util.formatDate(activities_planned_end)
        actual_start = util.formatDate(activities_actual_start)
        actual_end = util.formatDate(activities_actual_end)
        prj_name = getProjectName()

        execSQL = ('insert_activities_data')
        execData = (activities_name, unit_id, activities_contractor, None, activities_total_planned_hours, phase_id,
                    project_id, activities_total_planned_units, planned_start, planned_end, activities_unit_name,
                    actual_start, actual_end, None)
        print(execData)
        activities_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]


        print('#####################')
        print('writing values')
        print('Bundle Name : %s' % bundles_name)
        print('Bundle Phases : %s' % bundles_phases)
        print('Activity Name : %s' % activities_name)
        print('Activity Unit Name : %s' % activities_unit_name)
        print('Activity Material: %s' % activities_material)
        print('#####################')
    except psycopg2.DatabaseError as error:
        print("Database Error %s " % error)
        raise
    except Exception as error:
        print("Error %s " % error)
        raise
    else:
        connObj.close()
    finally:
        print("writeBundle_Activity")


def findKeyOccurence(listItem):
    prjLen = 0
    for track in listItem:
        if 'project' in track.keys():
            prjLen += 1

    print(prjLen)
    return prjLen

# -------------Main Program Starts --------#
try:
    ## Read the JSON Stream from stdin
    #jsonData = sys.stdin.read()
    #d = json.loads(jsonData, object_pairs_hook=join_duplicate_keys)
    with open("./str_data.json") as f:
        #Sbundle all the duplicate keys into one
        fileText = json.load(f, object_pairs_hook=join_duplicate_keys)
    print(fileText)
except ValueError as ve:
    traceback.print_exc()
    raise
except Exception as error:
    print("Error %s " % error)
    raise
finally:
    print("Read JSON data")

# Now read each value inside the bundle and the iteration value
# first get the length of the bundle
#length_of_bundles = len(d[0]["bundles"])
#length_of_items_inside_bundles = len(d[0]["bundles"])

try:
    d = []
    for listitems in range(0, len(fileText)):
        d = []
        # first get each item from the list
        d.append(fileText[listitems])
        print(d)
        print(type(d))
        occ = findKeyOccurence(d)

        item_project = getItemsParentLevel(len(d),"project")
        item_bundles = getItemsParentLevel(len(d),"bundles")
        item_contractors = getItemsParentLevel(len(d),"contractors")
        item_materials = getItemsParentLevel(len(d),"materials")
        item_incidents = getItemsParentLevel(len(d),"incidents")

        print('Bundle Type is :- %s' %type(item_bundles))
        print('Contractor Type is :- %s' %type(item_contractors))
        print('Material Type is :- %s' %type(item_materials))
        print('Incidents Type is :- %s' %type(item_incidents))

        if type(item_bundles)== list:
            lengthList = len(d)
            for i in range(0,len(item_bundles)):
                item_activities = d[lengthList - 1]["bundles"][i]["activities"]
                #print(item_activities)
                #print(type(item_activities))

        #--- get Portfolio details ---
        portfolio_id = getPortfolioDetails()

        # --- get all the project details ---
        project_id = getProjectDetails(portfolio_id)

        # -- Main Fn() get all the contractor details ---
        if type(item_contractors)== list:
            getContractorDetails_List()
        elif type(item_contractors)== dict:
            getContractorDetails_Dict()
        # -----------------------------------------------

        # -- Main Fn() get all the Material details ---
        if type(item_materials)== list:
            getMaterialDetails_List()
        elif type(item_materials)== dict:
            getMaterialDetails_Dict()
        # -----------------------------------------------

        # -- Main Fn() get all the Incident details ---
        if type(item_incidents)== list:
            getIncidentDetails_List()
        elif type(item_incidents)== dict:
            getIncidentDetails_Dict()
        # -----------------------------------------------

        #---------------------------------------------------------------
        ## Now get the values of the bundles
        # first check if it is a list or dict
        # if it is a dict, we directly read the values
        # if it is a list, then we iterate through the list and read them

        if type(item_bundles)== list:
            lengthList = len(d)
            for i in range(0,len(item_bundles)):
                # find out how many activities are there for the current bundle
                item_activities = d[lengthList - 1]["bundles"][i]["activities"]
                if type(item_activities)==list:
                    # the current index of bundle is passed
                    print('I am calling fn writeActivitiesData_MultiBundles_MultipleActivities() ---')
                    writeActivitiesData_MultiBundles_MultipleActivities(i,project_id)
                    print('I returned from writeActivitiesData_MultiBundles_MultipleActivities() ---')
                elif type(item_activities)==dict:
                    print('I am in blist and adict')
                    # get the total list of items of activities in bundles
                    print('I am calling fn writeBundleList_DictActivity(i) ---')
                    writeBundleList_DictActivity(i, project_id)
        elif type(item_bundles)== dict:
            print('Item Bundles is a dictionary ---')
            item_activities = d[len(d)-1]["bundles"]["activities"]
            if type(item_activities)==list:
                print('Item activities is a List ---')
                print('Calling func. writeActivitiesData_MultipleActivities() ---')
                writeActivitiesData_MultipleActivities(project_id)
            elif type(item_activities)==dict:
                print('Item activities is a dictionary ---')
                print('Calling func. writeBundle_Activity() ---')
                writeBundle_Activity(project_id)
except util.DLException as error:
    traceback.print_exc()
    raise
except psycopg2.DatabaseError as error:
    print("%s in %s at %d" %(error.pgerror, util.__FILE__(), util.__LINE__(), ))
    traceback.print_exc()
    raise
except ValueError as ve:
    print("%s in %s at %d" % (ve, util.__FILE__(), util.__LINE__(),))
    traceback.print_exc()
    raise
else:
    ## insert file_storage
    connObj = dbu.getConn()
    # update file_storage in db
    dbu.updateFileObjectIntoDB(dbu, str(d).encode(), 'Streaming content for BaselineData', 'Structural')
    connObj.close()
    sys.exit(0)
finally:
    print("Finished output")


'''
def main(args):
    hello(args[1])
if __name__ == '__main__':
    main(sys.argv)
'''

## End of Program ###--------------
