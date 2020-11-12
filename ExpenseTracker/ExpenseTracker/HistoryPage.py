from tkinter import *
from tkinter import ttk
from DatabaseConnection import DbConnection

class HistoryPageForm(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("History Page")

        cursor = DbConnection.conxn.cursor()

        #Define Tree View
        history_tree = ttk.Treeview(self)

        #Establish Column Names
        history_tree['columns'] = ('Category','Price','Date')

        #Format Columns
        history_tree.column('#0',width=0) #Phantom column (if parent and child then have width greater than 0)
        history_tree.column('Category', anchor=W, width=120)
        history_tree.column('Price', anchor=CENTER, width=80)
        history_tree.column('Date', anchor=W, width=120)

        #Create Headings
        history_tree.heading('#0',text='',anchor=W)
        history_tree.heading('Category',text='Category', anchor=W)
        history_tree.heading('Price',text='Price', anchor=CENTER)
        history_tree.heading('Date',text='Date', anchor=W)

        ### Add Data ###
        #Query to get data from the expense and category tables
        expenses = cursor.execute('SELECT Category.Name, Expense.Amount, Expense.Date FROM Expense INNER JOIN Category ON Expense.CategoryId=Category.Id').fetchall()

        #Loop through the expenses and append them in a list
        var = []
        for e in expenses:
            var.append((e[0],e[1],e[2]))

        #Put Data Into Tree
        for i in range(len(var)):
            history_tree.insert(parent='',index='end',iid=i,values=(var[i][0],var[i][1],var[i][2]))

        #Grid To Screen
        history_tree.grid(row=0,column=0,padx=5,pady=20,sticky='NSEW')

        #Add functionality for the widgets to resize with the window
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
