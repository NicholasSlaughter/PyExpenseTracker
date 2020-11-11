import pyodbc
from tkinter import *
from DatabaseConnection import DbConnection

def main():
    cursor = DbConnection.conxn.cursor()
    root = Tk()
    root.title('Expense Tracker')

    root.mainloop()
    DbConnection.conxn.close()

if __name__ == "__main__":
    main()
