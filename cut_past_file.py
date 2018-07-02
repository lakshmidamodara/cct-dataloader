# put the below line in the begining along with list initialization
parentChildDict = {}

## copy this code and paste it over the getParentChildActivities
def maintainParentChildActivityName(ActivityName, dictKey):
    LActName = ActivityName
    LDictKey = dictKey
   # creating a dictionary with objects
    global parentChildDict
    parentChildDict[dictKey] = ActivityName
    #print(parentChildDict)


# This method takes the result_data list
# removes all the empty record list.
# opens up the final_data list, inserts the first node, which is the project or parent node.
# then using previous, current and final cursor (level) parses through the record list and finds out the lowest node
# in the list and creates the final_list
def getParentChildActivities():
    try:
        previous_level = 0
        current_level = 0
        next_level = 0
        parent_activity_name = ""

        # first remove empty list from result_data i.e, if there are empty rows in the excel
        result_data1 = [x for x in result_data if x != []]
        print("\n", file=f)
        print("############## Result Data List in getParentChildActivities after Null ",file=f)
        print(result_data1,file=f)
        totalRec = len(result_data1)

        for i in range(0,totalRec):
            local_node_result = []
            previous_level = int(result_data1[i-1][3])
            current_level = int(result_data1[i][3])
            maintainParentChildActivityName(result_data1[i][0], current_level)
            # if it is not the last record
            if (i+1) != totalRec:
                next_level = int(result_data1[i+1][3])
                # if the current activity is greater than the previous one
                # then the parent activity name is stored in the variable to
                # be concatenated with the current levels
                if int(current_level) >= int(previous_level):
                    if int(current_level) >= int(next_level):
                        local_Level = int(result_data1[i][3])
                        parent_activity_name = parentChildDict[local_Level - 1]
                        local_activity_name = parent_activity_name + "-" + result_data1[i][0]
                        local_node_result.append(local_activity_name)
                        local_node_result.append(result_data1[i][1])
                        local_node_result.append(result_data1[i][2])
                        local_node_result.append(result_data1[i][3])
                        final_list.append(local_node_result)

            # this logic is executed for the last record in the list
            elif (i + 1) == totalRec:
                # get the dictionary
                if current_level != previous_level:
                    local_Level = int(result_data1[i][3])
                    ActivityName = parentChildDict[local_Level - 1]
                    local_node_result.append(ActivityName + "-" + result_data1[i][0])
                    local_node_result.append(result_data1[i][1])
                    local_node_result.append(result_data1[i][2])
                    local_node_result.append(local_Level)
                    final_list.append(local_node_result)

                elif current_level == previous_level:
                    local_Level = int(result_data1[i][3])
                    ActivityName = parentChildDict[local_Level - 1]
                    local_node_result.append(ActivityName + "-" + result_data1[i][0])
                    local_node_result.append(result_data1[i][1])
                    local_node_result.append(result_data1[i][2])
                    local_node_result.append(local_Level)
                    # get the parent of the last node
                    final_list.append(local_node_result)

        print("\n",file=f)
        print("########## Printing Final dataset to be inserted.- getParentChildActivities()... ##########", file=f)
        print(final_list,file=f)
        print("final list in getParentChild", len(final_list))
    except (Exception) as error:
        print(error)
