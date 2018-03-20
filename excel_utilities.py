'''
File Name      : excel_utilities.py
Author Name    : Lakshmi Damodara
Date           : 01/30/2018
Version        : 1.0
Description    : This program does the following

1) Accepts workbook and list as argument
2) Reads the workbook and worksheet
3) Goes to each and every activity sheet and gets the data values for public.activities and activity_data
4) Removes unwanted data and returns back list with actual valid data from the sheets.

Functions:
getSheetResult(), remove_item_list(), ConvertDate()


'''


import datetime
import excel_config_reader as efcr
import string

print('##---Program: excel_utilities..........................')
print(datetime.datetime.today())
print('##---------------------------------------------........')

def getLowerAlphabetDictionary():
    letter_count = dict(zip(string.ascii_lowercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
    return letter_count

def getUpperAlphabetDictionary():
    letter_count = dict(zip(string.ascii_uppercase, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] * 26))
    return letter_count

def getRowColumn(strVal):
    rowCol = []
    Tcol = strVal[0] #get the first character from the string: eg: if strVal = A5 -> 'A' is selected
    T1col = getUpperAlphabetDictionary() # get the corresponding key value from the function
    col = T1col[Tcol] # assign the key to the col index value: eg) A5 -> 0
    Trow = int(strVal[1:]) # getting the rest of the string value after the first
    row = Trow -1
    rowCol.append(row)
    rowCol.append(col)
    return rowCol

def remove_items_list(listVar,removeListVar):
    # remove the unnecessary values from the result data
    for i in sorted(removeListVar, reverse=True):
        del listVar[i]
    return listVar

def convertDate(dtt):
    return datetime.datetime.date(dtt) # returns just the date in mm-dd-yyyy format

#---------------------------------------------------------------------------
# This function contains the business logic to read the daily activity sheet
#----------------------------------------------------------------------------
def getSheetResult(wbe,active_sheet_value):
    sName = efcr.shName(active_sheet_value)  # get the sheet name
    Asheet = wbe[sName]

   # get the max count of rows and cols
    m_row = Asheet.max_row
    #m_col = Asheet.max_column
    m_row = m_row + 1

    # -- This section is to store the data of the active sheet in to List of Lists
    # -- result_data is the list of list containing : rows and columns of the active sheet
    # -- The reading of row starts at Row# 7 and 6 columns are read starting from column # 2
    # -- As it is being read, the dates are converted to MMDDYYYY format and
    # -- the result is stored in result_data as list of lists

    # initialize list
    result_data = []
    for curr_row in range(7, m_row, 1):
        if not Asheet.row_dimensions[curr_row].hidden == True:  # dont read if the row is hidden
            row_data = []
            row_data.append(sName) # inserting the activity name
            for curr_col in range(2, 8, 1): # read each col. from the sheet starting from col number 2 upto col 8
                data = Asheet.cell(row=curr_row, column=curr_col)
                if isinstance(data.value, datetime.datetime): # getting the date value and converting to mmddyyyy format value
                    row_data.append(convertDate(data.value).strftime('%m%d%Y')) # inserting the value to row_data
                else:
                    row_data.append(data.value) # inserting the rest of the values

        result_data.append(row_data) # inserting the row_data into result_data list

    # -- This section is to create a list - popping_Var which contains the row index of result_data
    # -- that needed to be removed as it contains non-date values
    # -- We are reading the col.#2 and checking if the string value is greater than 10
    # -- If yes, then the index value is stored in popping_Var

    popping_Var = []
    ## Now accessing the list of list result_data : result_data = [][]
    for i in range(0, len(result_data), 1):
        for j in range(1, 7, 1):  # access the list from index of 1 in result_data as the index[0] is the project name
            if type(result_data[i][j]) == str and len(result_data[i][j]) > 10:
                popping_Var.append(i)
                break

    # Call the function to remove the list of values in result_data which are referenced in popping_Var
    result_data = remove_items_list(result_data, popping_Var)

### -------------------------------------
### Remove the list of result Data which has None or null values
### If the planned to date column has null values, those rows in the result_data list are removed.
### --------------------------------------
    popping_Var_None = []
    ## Now accessing the list of list result_data with None Value
    for i in range(0, len(result_data), 1):
        if result_data[i][5] == None: # checking if the list index[5] in result_data is None
            popping_Var_None.append(i) # store the index value in popping_Var_None list

    # Call the function to remove the list containing None or null values as referenced in popping_Var_None
    result_data=remove_items_list(result_data,popping_Var_None)

    # return the final list to the calling function
    print(result_data)
    del popping_Var
    del popping_Var_None
    return result_data


### ---------End of Functions -----
