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

def getConn():
    try :
        ## creating a connection instance
        myConnection = psycopg2.connect(host=os.environ.get('DATABASE_HOSTNAME'),port=os.environ.get('DATABASE_PORT'),
                                        user=os.environ.get('DATABASE_USER'),password=os.environ.get('DATABASE_PWD'),
                                        database=os.environ.get('DATABASE_NAME'))
        print (myConnection)
        return myConnection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def executeQueryWithData(conn, exSQL, exData):
   try:
       cur = conn.cursor()
       print(exSQL)
       print(exData)
       cur.execute(exSQL, exData)
       conn.commit()
   except (Exception, psycopg2.DatabaseError) as error:
    print(error)

def executeQuery(conn, exSQL):
   try:
       cur = conn.cursor()
       print(exSQL)
       cur.execute(exSQL)
       conn.commit()
   except (Exception, psycopg2.DatabaseError) as error:
    print(error)

#-- End of Program --