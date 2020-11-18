import unittest
import pyodbc
from datetime import datetime
from DatabaseConnection import DbConnection

class Test_DbTest(unittest.TestCase):
    #Return True If Passes
    def test_Db_Connection(self):
        try:
            server = 'NICK-PC\\NICKS_MSSQLSERVR'
            database = 'ExpenseTracker'

            conxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                SERVER=' + server + '; \
                                DATABASE=' + database +'; \
                                Trusted_Connection=yes;')
            self.assertTrue(True)
        except:
            self.fail("Could Not Connect To Database")

    #Return True If Passes
    def test_Db_Insert_Expense(self):
        try:
            cursor = DbConnection.conxn.cursor()
            amount = float(5.99)
            date = datetime.now()
            catId = 5

            insert_query = '''INSERT INTO Expense (Amount,Date,CategoryId)
                        VALUES (?,?,?)'''
            cursor.execute(insert_query,float(amount),date,int(catId))
            self.assertTrue(True)
        except:
            self.fail("Could Not Insert An Expense")

    #Return True If Fails
    def test_Db_Bad_Insert_Expense(self):
        try:
            cursor = DbConnection.conxn.cursor()
            amount = 'a'
            date = datetime.now()
            catId = 5

            insert_query = '''INSERT INTO Expense (Amount,Date,CategoryId)
                        VALUES (?,?,?)'''
            cursor.execute(insert_query,amount,date,int(catId))
            self.fail("Should Not Insert Bad Data")
        except:
            self.assertTrue(True)

    #Return True If Passes
    def test_Db_Delete_Expense(self):
        try:
            cursor = DbConnection.conxn.cursor()
            expense_to_delete = cursor.execute('SELECT TOP 1 * FROM Expense ORDER BY Id DESC').fetchall()
            expense_to_delete = expense_to_delete[0][0]

            delete_query = '''DELETE FROM Expense WHERE Id = (?)'''

            cursor.execute(delete_query,expense_to_delete)
            self.assertTrue(True)
        except:
            self.fail("Could Not Insert An Expense")

    #Return True If Fails
    def test_Db_Bad_Delete_Expense(self):
        try:
            cursor = DbConnection.conxn.cursor()
            expense_to_delete = cursor.execute('SELECT TOP 1 * FROM Expense ORDER BY Id DESC').fetchall()
            #Out Of Range
            expense_to_delete = expense_to_delete[0][0] + 1

            delete_query = '''DELETE FROM Expense WHERE Id = (?)'''

            cursor.execute(delete_query,expense_to_delete)
            self.fail("Should Not Delete")
        except:
            self.assertTrue(True)

    #Return True If Passes
    def test_Db_Insert_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            max_amount = float(20)
            current_amount = 0
            catId = 5
            periodId = 1

            insert_query = '''INSERT INTO Alert (MaxAmount,CurrentAmount,CategoryId,PeriodId)
                          VALUES (?,?,?,?)'''
            cursor.execute(insert_query,max_amount,current_amount,catId,periodId)
            self.assertTrue(True)
        except:
            self.fail("Could Not Insert An Alert")

    #Return True If Fails
    def test_Db_Bad_Insert_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            max_amount = float(20)
            current_amount = a
            catId = 5
            periodId = 1

            insert_query = '''INSERT INTO Alert (MaxAmount,CurrentAmount,CategoryId,PeriodId)
                          VALUES (?,?,?,?)'''
            cursor.execute(insert_query,max_amount,current_amount,catId,periodId)
            self.fail("Should Not Insert An Alert")
        except:
            self.assertTrue(True)

    #Return True If Passes
    def test_Db_Delete_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            alert_to_delete = cursor.execute('SELECT TOP 1 * FROM Alert ORDER BY Id DESC').fetchall()
            alert_to_delete = alert_to_delete[0][0]

            delete_query = '''DELETE FROM Alert WHERE Id = (?)'''

            cursor.execute(delete_query,alert_to_delete)
            self.assertTrue(True)
        except:
            self.fail("Could Not Delete An Alert")

    #Return True If Fails
    def test_Db_Bad_Delete_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            alert_to_delete = cursor.execute('SELECT TOP 1 * FROM Alert ORDER BY Id DESC').fetchall()
            #Out Of Range
            alert_to_delete = alert_to_delete[0][0] + 1

            delete_query = '''DELETE FROM Alert WHERE Id = (?)'''

            cursor.execute(delete_query,alert_to_delete)
            self.fail("Should Not Delete An Alert")
        except:
            self.assertTrue(True)

    #Return True If Passes
    def test_Db_Update_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            current_amount = 30
            alert_to_update = cursor.execute('SELECT TOP 1 * FROM Alert ORDER BY Id DESC').fetchall()
            alert_to_update = alert_to_update[0][0]

            update_query = '''UPDATE Alert
                              SET CurrentAmount = (?)
                              WHERE Alert.Id = (?)'''

            cursor.execute(update_query,current_amount,alert_to_update)
            self.assertTrue(True)
        except:
            self.fail("Could Not Update An Alert")

    #Return True If Fails
    def test_Db_Bad_Update_Alert(self):
        try:
            cursor = DbConnection.conxn.cursor()
            current_amount = a
            alert_to_update = cursor.execute('SELECT TOP 1 * FROM Alert ORDER BY Id DESC').fetchall()
            alert_to_update = alert_to_update[0][0]

            update_query = '''UPDATE Alert
                              SET CurrentAmount = (?)
                              WHERE Alert.Id = (?)'''

            cursor.execute(update_query,current_amount,alert_to_update)
            self.fail("Should Not Update An Alert")
        except:
            self.assertTrue(True)
    
    #Return True If Passes
    def test_Db_Insert_Category(self):
        try:
            cursor = DbConnection.conxn.cursor()
            cat_to_insert = 'Temp Category'

            insert_query = '''INSERT INTO Category (Name)
                          VALUES (?)'''
            cursor.execute(insert_query,cat_to_insert)
            self.assertTrue(True)
        except:
            self.fail("Could Not Insert A Category")

    #Return True If Fails
    def test_Db_Bad_Insert_Category(self):
        try:
            cursor = DbConnection.conxn.cursor()
            cat_to_insert = 1

            insert_query = '''INSERT INTO Category (Name)
                          VALUES (?)'''
            cursor.execute(insert_query,int(cat_to_insert))
            self.fail("Could Not Insert A Category")
        except:
            self.assertTrue(True)

    #Not Allowed Due To Foreign Key Relationship So Output Call Exception To Return True
    def test_Db_Delete_Category(self):
        try:
            cursor = DbConnection.conxn.cursor()
            category_to_delete = cursor.execute('SELECT TOP 1 * FROM Category ORDER BY Id DESC').fetchall()
            category_to_delete = category_to_delete[0][0]

            delete_query = '''DELETE FROM Category WHERE Id = (?)'''

            cursor.execute(delete_query,category_to_delete)
            self.fail("Not Supposed To Delete Due To Foreign Key")
        except:            
            self.assertTrue(True)

    #Return True If Passes
    def test_Db_Insert_Period(self):
        try:
            cursor = DbConnection.conxn.cursor()
            per_to_insert = 'Temp Period'

            insert_query = '''INSERT INTO Period (Name)
                          VALUES (?)'''
            cursor.execute(insert_query,per_to_insert)
            self.assertTrue(True)
        except:
            self.fail("Could Not Insert A Period")

    #Return True If Fails
    def test_Db_Bad_Insert_Period(self):
        try:
            cursor = DbConnection.conxn.cursor()
            per_to_insert = 1

            insert_query = '''INSERT INTO Period (Name)
                          VALUES (?)'''
            cursor.execute(insert_query,int(per_to_insert))
            self.fail("Could Not Insert A Period")
        except:
            self.assertTrue(True)

    #Not Allowed Due To Foreign Key Relationship So Output Call Exception To Return True
    def test_Db_Delete_Period(self):
        try:
            cursor = DbConnection.conxn.cursor()
            period_to_delete = cursor.execute('SELECT TOP 1 * FROM Period ORDER BY Id DESC').fetchall()
            period_to_delete = period_to_delete[0][0]

            delete_query = '''DELETE FROM Period WHERE Id = (?)'''

            cursor.execute(delete_query,period_to_delete)
            self.fail("Not Supposed To Delete Due To Foreign Key")
        except:            
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
