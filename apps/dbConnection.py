import psycopg2 as ps
import sys 
import os 
import pandas as pd


ENDPOINT="ds4a-demo-instance.ccl8oxs9s8af.us-east-1.rds.amazonaws.com"
PORT="5432" 
USR="postgres" 
REGION="us-east-1" 
DBNAME="bucaramanga"
PWD= "ZAHcsHqjKNf5owsDx7hl"
                
def startConn():                
    try:
        conn = ps.connect(host=ENDPOINT,database=DBNAME,user=USR,password=PWD,port=PORT)
        print('Connected!')
    except ps.OperationalError as e:
        raise e
    
    return conn
