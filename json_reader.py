import json
import datetime
import db_utilities as dbu

# --------------------------------------------------------#
# Function to group the duplicate keys from JSON file     #
# This function is run first after opening the JSON file  #
# If this function is not run, python will not allow      #
# duplicate keys. The last item will be overwritten       #
#---------------------------------------------------------#
def join_duplicate_keys(ordered_pairs):
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

def getItemsParentLevel(lengthList,node):
    itemVar =""
    for i in range(0,lengthList):
        itemVar = d[i][node]
    return itemVar

def getItemsChildLevel(node1,node2):
    itemVar =""
    lengthList = len(d)
    for i in range(0,lengthList):
        itemVar = d[i][node1][node2]
    return itemVar

def getItemsChildLevel_List(lengthList,node1,node2,iterationVal):
    itemVar =""
    for i in range(0,lengthList):
        itemVar = d[i][node1][iterationVal][node2]
    return itemVar

def getItemsSubChildLevel(node1,node2,node3):
    itemVar =""
    lengthList = len(d)
    for i in range(0,lengthList):
        itemVar = d[i][node1][node2][node3]
    return itemVar

def getItemsSubChildLevel_List(lengthList,node1,node2,node3,iterationVal):
    itemVar =""
    for i in range(0,lengthList):
        itemVar = d[i][node1][node2][iterationVal][node3]
    return itemVar



# -------------- Function to get the project details -----------------------

def getProjectName():
    project_name = getItemsChildLevel("project","name")

def getProjectDetails():
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

    ## Update the details to the database temp
    connObj = dbu.getConn()

    # --------------------------------------------------------
    # Insert data to location table and get location id
    # --------------------------------------------------------
    start_date = datetime.datetime.strptime(project_start_date,'%m%d%Y').date().strftime('%Y%m%d')
    end_date = datetime.datetime.strptime(project_end_date,'%m%d%Y').date().strftime('%Y%m%d')

    execSQL = ('insert_location_data')
    execData = (proj_loc_street, project_loc_city, project_loc_state, project_loc_country,None, None)
    project_loc_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
    print( "location id is")
    print (project_loc_id)

    execSQL = ('insert_project_data')
    execData = (project_name, start_date, end_date, json.dumps(project_workdays),int(project_budget),None, project_loc_id, None)
    project_id = dbu.fetchStoredFuncRes(connObj, execSQL,execData)[0]
    connObj.close()
    return project_id

# -------------- Function to get the contractor details -----------------------
def getContractorDetails():
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
        # Insert data to project and location table
        # --------------------------------------------------------
        execSQL = ('insert_contractor_data')
        execData = (contractor_name, contractor_email, contractor_phone, contractor_pcontact)
        contractor_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

    connObj.close()
    #return contractor_id

def writeActivitiesData_MultipleActivities(project_id):
    activityList = []
    connObj = dbu.getConn()

    node1 = "bundles"
    node2 = "activities"
    bundles_name = getItemsChildLevel(len(d), "bundles", "name")
    bundles_phases = getItemsChildLevel(len(d), "bundles", "phases")

    execSQL = ('insert_bundles_data')
    execData = (None, bundles_name, project_id, None)
    bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

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
        execData = (activities_unit_name)
        unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
        print ('units id is ')
        print (unit_id)

        activities_material = getItemsSubChildLevel_List(len(d), "bundles", "activities", "material",i)

        # --------------------------------------------------------
        # Insert data to project and location table
        # --------------------------------------------------------
        planned_start = datetime.datetime.strptime(activities_planned_start, '%m%d%Y').date().strftime('%Y%m%d')
        planned_end = datetime.datetime.strptime(activities_planned_end, '%m%d%Y').date().strftime('%Y%m%d')
        actual_start = datetime.datetime.strptime(activities_actual_start, '%m%d%Y').date().strftime('%Y%m%d')
        actual_end = datetime.datetime.strptime(activities_actual_end, '%m%d%Y').date().strftime('%Y%m%d')
        prj_name = getProjectName()

        execSQL = "INSERT INTO TEMP.ACTIVITIES(NAME,CONTRACTOR_NAME,TOTAL_PLANNED_HOURS,PROJECT_NAME,TOTAL_PLANNED_UNITS,PLANNED_START,PLANNED_END,UNIT_NAME,ACTUAL_START,ACTUAL_END) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        execData = (activities_name, activities_contractor, activities_total_planned_hours, prj_name,activities_total_planned_units,planned_start, planned_end, activities_unit_name, actual_start, actual_end)

        dbu.executeQueryWithData(connObj, execSQL, execData)

        print('#####################')
        print(execSQL)
        print(execData)
        print('writing values')
        print('Bundle Name : %s' %bundles_name)
        print('Bundle Phases : %s' %bundles_phases)
        print ('Activity Name : %s' %activities_name)
        print ('Activity Unit Name : %s' %activities_unit_name)
        print ('Activity Material: %s' %activities_material)
        print('#####################')

def getItems_MultiBundle_MultiActivity(node1,node2,node3,iterationVal_h,iterationVal_i):
    itemVar =""
    for i in range(0,len(d)):
        itemVar = d[i][node1][iterationVal_h][node2][iterationVal_i][node3]
        #print(itemVar)
    return itemVar

def writeActivitiesData_MultiBundles_MultipleActivities(bundle_item, project_id):
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
       execData = (str(activities_unit_name))
       unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, 'Rows')[0]
       print('units id is ')
       print(unit_id)

       activities_material = getItems_MultiBundle_MultiActivity(node1, node2, "material",bundle_item, i)

       print(activities_planned_start)

       # --------------------------------------------------------
       # Insert data to project and location table
       # --------------------------------------------------------
       planned_start = datetime.datetime.strptime(activities_planned_start, '%m%d%Y').date().strftime('%Y%m%d')
       planned_end = datetime.datetime.strptime(activities_planned_end, '%m%d%Y').date().strftime('%Y%m%d')
       actual_start = datetime.datetime.strptime(activities_actual_start, '%m%d%Y').date().strftime('%Y%m%d')
       actual_end = datetime.datetime.strptime(activities_actual_end, '%m%d%Y').date().strftime('%Y%m%d')
       prj_name = getProjectName()

       execSQL = "INSERT INTO TEMP.ACTIVITIES(NAME,CONTRACTOR_NAME,TOTAL_PLANNED_HOURS,PROJECT_NAME,TOTAL_PLANNED_UNITS,PLANNED_START,PLANNED_END,UNIT_NAME,ACTUAL_START,ACTUAL_END) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
       execData = (
       activities_name, activities_contractor, activities_total_planned_hours, prj_name, activities_total_planned_units,
       planned_start, planned_end, activities_unit_name, actual_start, actual_end)
       dbu.executeQueryWithData(connObj, execSQL, execData)

       print('#####################-- MultiBundle-MultiActivity----')
       print(execSQL)
       print(execData)
       print('writing values')
       print('Bundle Name : %s' % bundles_name)
       print('Bundle Phases : %s' % bundles_phases)
       print('Activity Name : %s' % activities_name)
       print('Activity Unit Name : %s' % activities_unit_name)
       print('Activity Material: %s' % activities_material)
       print('#####################')

    connObj.close()
# -----------------------------------------------------------#
# This function is called when  bundles is a list  and
# activities  is dictionary                                #
#-----------------------------------------------------------#

def getwriteBundleList_DictActivity(node1,node2,node3,iterationVal):
    itemVar = ""
    for i in range(0, len(d)):
        itemVar = d[i][node1][iterationVal][node2][node3]
    return itemVar

def writeBundleList_DictActivity(bundle_item, project_id):
    connObj = dbu.getConn()
    print('I am entering fn writeBundleList_DictActivity(i) ---')
    bundles_name = d[len(d) -1]["bundles"][bundle_item]["name"]
    bundles_phases = d[len(d) -1]["bundles"][bundle_item]["phases"]

    execSQL = ('insert_bundles_data')
    execData = (None, bundles_name, project_id, None)
    bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

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
    execData = (activities_unit_name)
    unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
    print('units id is ')
    print(unit_id)

    activities_material = getwriteBundleList_DictActivity("bundles","activities", "material",bundle_item)

    # --------------------------------------------------------
    # Insert data to project and location table
    # --------------------------------------------------------
    planned_start = datetime.datetime.strptime(activities_planned_start, '%m%d%Y').date().strftime('%Y%m%d')
    planned_end = datetime.datetime.strptime(activities_planned_end, '%m%d%Y').date().strftime('%Y%m%d')
    actual_start = datetime.datetime.strptime(activities_actual_start, '%m%d%Y').date().strftime('%Y%m%d')
    actual_end = datetime.datetime.strptime(activities_actual_end, '%m%d%Y').date().strftime('%Y%m%d')
    prj_name = getProjectName()

    execSQL = "INSERT INTO TEMP.ACTIVITIES(NAME,CONTRACTOR_NAME,TOTAL_PLANNED_HOURS,PROJECT_NAME,TOTAL_PLANNED_UNITS,PLANNED_START,PLANNED_END,UNIT_NAME,ACTUAL_START,ACTUAL_END) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    execData = (activities_name, activities_contractor, activities_total_planned_hours, prj_name,activities_total_planned_units,planned_start, planned_end, activities_unit_name, actual_start, actual_end)
    dbu.executeQueryWithData(connObj, execSQL, execData)

    print('###############-- writeBundleList_DictActivity() --######')
    print('writing values')
    print('Bundle Name : %s' % bundles_name)
    print('Bundle Phases : %s' % bundles_phases)
    print('Activity Name : %s' % activities_name)
    print('Activity Unit Name : %s' % activities_unit_name)
    print('Activity Material: %s' % activities_material)
    print('#####################')

    connObj.close()


# -----------------------------------------------------------#
# This function is called when both bundles and activities   #
# are dictionaries                                           #
# There is going to be only one entry in the list            #
# So directly read the values i.e: one bundle, one activity  #
#------------------------------------------------------------#
def writeBundle_Activity(project_id):
    ## Update the details to the database temp
    connObj = dbu.getConn()

    bundles_name = getItemsChildLevel(len(d),"bundles","name")
    bundles_phases = getItemsChildLevel(len(d), "bundles", "phases")

    execSQL = ('insert_bundles_data')
    execData = (None, bundles_name, project_id, None)
    bundle_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]

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
    execData = (activities_unit_name)
    unit_id = dbu.fetchStoredFuncRes(connObj, execSQL, execData)[0]
    print('units id is ')
    print(unit_id)

    activities_material = getItemsSubChildLevel("bundles", "activities", "material")

    # --------------------------------------------------------
    # Insert data to activities
    # --------------------------------------------------------
    planned_start = datetime.datetime.strptime(activities_planned_start, '%m%d%Y').date().strftime('%Y%m%d')
    planned_end = datetime.datetime.strptime(activities_planned_end, '%m%d%Y').date().strftime('%Y%m%d')
    actual_start = datetime.datetime.strptime(activities_actual_start, '%m%d%Y').date().strftime('%Y%m%d')
    actual_end = datetime.datetime.strptime(activities_actual_end, '%m%d%Y').date().strftime('%Y%m%d')
    prj_name = getProjectName()

    execSQL = "INSERT INTO TEMP.ACTIVITIES(NAME,CONTRACTOR_NAME,TOTAL_PLANNED_HOURS,PROJECT_NAME,TOTAL_PLANNED_UNITS,PLANNED_START,PLANNED_END,UNIT_NAME,ACTUAL_START,ACTUAL_END) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    execData = (activities_name,activities_contractor,activities_total_planned_hours,prj_name,activities_total_planned_units,planned_start,planned_end,activities_unit_name,actual_start,actual_end)
    print(execSQL)
    print(execData)
    dbu.executeQueryWithData(connObj, execSQL, execData)
    connObj.close()

    print('#####################')
    print('writing values')
    print('Bundle Name : %s' % bundles_name)
    print('Bundle Phases : %s' % bundles_phases)
    print('Activity Name : %s' % activities_name)
    print('Activity Unit Name : %s' % activities_unit_name)
    print('Activity Material: %s' % activities_material)
    print('#####################')

## First clean up the tables
def cleanUpTempTables():
## Update the details to the database temp
    connObj = dbu.getConn()

    # --------------------------------------------------------
    # First truncate the data from project
    # --------------------------------------------------------
    LsqlQuery = "TRUNCATE TABLE TEMP.PROJECTS"
    dbu.executeQuery(connObj, LsqlQuery)

    # --------------------------------------------------------
    # Contractors
    # --------------------------------------------------------
    LsqlQuery = "TRUNCATE TABLE TEMP.CONTRACTORS"
    dbu.executeQuery(connObj, LsqlQuery)

    # --------------------------------------------------------
    # Activities
    # --------------------------------------------------------
    LsqlQuery = "TRUNCATE TABLE TEMP.ACTIVITIES"
    dbu.executeQuery(connObj, LsqlQuery)


# -------------Main Program Starts --------#
#
cleanUpTempTables()
with open("./structural_data.json") as f:
    # bundle all the duplicate keys into one
    d = json.load(f, object_pairs_hook=join_duplicate_keys)

print(d)
#print(type(d))

# Now read each value inside the bundle and the iteration value
# first get the length of the bundle
#length_of_bundles = len(d[0]["bundles"])
#length_of_items_inside_bundles = len(d[0]["bundles"])

# first get each item from the list
item_project = getItemsParentLevel(len(d),"project")
item_bundles = getItemsParentLevel(len(d),"bundles")
print('Bundle Type is :- %s' %type(item_bundles))

if type(item_bundles)== list:
    lengthList = len(d)
    for i in range(0,len(item_bundles)):
        item_activities = d[lengthList - 1]["bundles"][i]["activities"]
        #print(item_activities)
        #print(type(item_activities))

# --- get all the project details ---
project_id = getProjectDetails()
print ( "Project_id %d", project_id)
getContractorDetails()
# --------------------------------

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
'''
def main(args):
    hello(args[1])
if __name__ == '__main__':
    main(sys.argv)
'''

## End of Program ###--------------
