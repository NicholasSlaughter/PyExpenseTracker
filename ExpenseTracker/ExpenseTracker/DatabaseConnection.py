import pyodbc

class DbConnection():
    server = 'NICK-PC\\NICKS_MSSQLSERVR'
    database = 'ExpenseTracker'

    #Establishes Connection String
    conxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                            SERVER=' + server + '; \
                            DATABASE=' + database +'; \
                            Trusted_Connection=yes;')

    #Create Connection Cursor
    #cursor = conxn.cursor()

    #Create Data To Insert
    #data_to_insert = [['Shoes'],
    #                  ['Apples']]

    #query used to call an insert on a table
    #triple quotes means a multi line string
    #? symbol is used to have data placed into it
    #insert_query = '''INSERT INTO Category (Name)
    #                  VALUES (?)'''

    #Loop Through And Insert Data
    #for row in data_to_insert:
    #    values = (row[0])
    #    cursor.execute(insert_query,values)

    #Commit Changes
    #conxn.commit()

    #grabs data to output using a query
    #cursor.execute('SELECT * FROM Category')

    #print data grabbed from query
    #for row in cursor:
    #    print(row)