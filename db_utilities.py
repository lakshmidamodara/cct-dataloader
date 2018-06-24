''''
File Name      : db_utilities.py
Author Name    : Lakshmi Damodara
Creation Date  : 01/30/2018
Updated Date   : 02/02/2018
Version        : 1.0
Description    :
1. This program is used for various database operations
2. Functions:
    getConn()
    executeQueryWithData()
    executeQuery()
'''

# Loading the library for postgres sql
import psycopg2
import os
import utilities as utl
from openpyxl.writer.excel import save_virtual_workbook

def getConn():
    try :
        ## creating a connection instance
        myConnection = psycopg2.connect(host=os.environ.get('DATABASE_HOSTNAME'),port=os.environ.get('DATABASE_PORT'),
                                        user=os.environ.get('DATABASE_USER'),password=os.environ.get('DATABASE_PWD'),
                                        database=os.environ.get('DATABASE_NAME'))
        print (myConnection)
        return myConnection
    except (Exception, psycopg2.DatabaseError) as error:
        print ( "Database Error %s " %error)
        raise

def executeQueryWithData(conn, exSQL, exData):
   try:
       cur = conn.cursor()
       print(exSQL)
       print(exData)
       cur.execute(exSQL, exData)
       conn.commit()
   except (Exception, psycopg2.DatabaseError) as error:
       print("Database Error %s " % error)
       raise

def executeQuery(conn, exSQL):
   try:
       cur = conn.cursor()
       print(exSQL)
       cur.execute(exSQL)
       conn.commit()
   except (Exception, psycopg2.DatabaseError) as error:
       print("Database Error %s " % error)
       raise

def executeQueryRes(conn, exSQL):
   try:
       cur = conn.cursor()
       print(exSQL)
       cur.execute(exSQL)
       rows = cur.fetchall()
       conn.commit()
       cur.close()
       return(rows)
   except (Exception, psycopg2.DatabaseError) as error:
       print("Database Error %s " % error)
       raise

def fetchStoredFuncRes(conn, exSQL, exData):
    ## This function is useful to call stored procs for single row returns
   try:
       cur = conn.cursor()
       cur.callproc(exSQL, tuple(exData))
       # process the result set
       row = cur.fetchone()
       conn.commit()
       cur.close()
       return(row)
       print(exSQL)
       print(exData)
   except (Exception, psycopg2.DatabaseError) as error:
       print("Database Error %s " % error)
       raise

# update the file object into db
def updateFileObjectIntoDB( conn, wb, L_FileName,load_type):
    try:
        conn = getConn()
        execSQL = """update FILE_STORAGE  
                      set filename = '{fileName}',
                          filedata = {data},
                          updated = current_timestamp(2) 
                    where load_type = '{type}'; """
        execSQL = execSQL.format(fileName = L_FileName, data = psycopg2.Binary(wb), type = load_type)
        executeQuery(conn, execSQL)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database Error %s " % error)
        raise
    finally:
        if conn is not None:
            conn.close()

#-- End of Program --