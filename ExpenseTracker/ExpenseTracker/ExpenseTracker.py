import pyodbc
from DatabaseConnection import DbConnection

cursor = DbConnection.conxn.cursor()

#grabs data to output using a query
cursor.execute('SELECT * FROM Category')

#print data grabbed from query
for row in cursor:
    print(row)

DbConnection.conxn.close()
