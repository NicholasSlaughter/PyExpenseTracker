from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from DatabaseConnection import DbConnection

class HistoryPageForm(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("History Page")

        cursor = DbConnection.conxn.cursor()

        #Define Tree View
        history_tree = ttk.Treeview(self)

        #Establish Column Names
        history_tree['columns'] = ('Id','Category','Price','Date')

        #Format Columns
        history_tree.column('#0',width=0,minwidth=0) #Phantom column (if parent and child then have width greater than 0)
        history_tree.column('Id',width=0,minwidth=0)
        history_tree.column('Category', anchor=W, width=120)
        history_tree.column('Price', anchor=CENTER, width=80)
        history_tree.column('Date', anchor=W, width=120)

        #Create Headings
        history_tree.heading('#0')
        history_tree.heading('Id')
        history_tree.heading('Category',text='Category', anchor=W)
        history_tree.heading('Price',text='Price', anchor=CENTER)
        history_tree.heading('Date',text='Date', anchor=W)

        ### Add Data ###
        #Query to get data from the expense and category tables
        expenses = cursor.execute('''SELECT Expense.Id, Category.Name, Expense.Amount, Expense.Date 
                                     FROM Expense 
                                     INNER JOIN Category 
                                     ON Expense.CategoryId=Category.Id'''
                                     ).fetchall()

        #Loop through the expenses and append them in a list
        var = []
        for e in expenses:
            formatted_time = str(e[3].month) + '/' + str(e[3].day) + '/' + str(e[3].year) + ' at ' + str(e[3].hour) + ':' + str(e[3].minute)
            var.append((e[0],e[1],e[2],formatted_time))

        #Put Data Into Tree
        for i in range(len(var)):
            try:
                history_tree.insert(parent='',index='end',iid=i,values=(var[i][0],var[i][1],var[i][2],var[i][3]))
            except:
                messagebox.showerror(title="Unable To Show All Expenses",message="Unable To Show An Expense In The Tree")
                print("Part in tree not shown: " + i)

        #Grid To Screen
        history_tree.grid(row=0,column=0,padx=5,pady=20,sticky='NSEW')

        #Delete Selected Expenses
        def Remove_Expenses():
            nonlocal history_tree
            expenses_to_remove = history_tree.selection()
            #Loop through the selected expenses and delete them from both the tree and the database
            for e in expenses_to_remove:
                #Get the the Id of the expense in the database
                expense_id = history_tree.item(e)['values']
                
                #Set up query used to delete an element from the expense table
                delete_query = '''DELETE FROM Expense WHERE Id = (?)'''

                #The Id is the 1st element in the array to scope to that and delete it from the db
                try:
                    cursor.execute(delete_query,expense_id[0])
                    DbConnection.conxn.commit()

                    #delete expense from tree to sync with database
                    history_tree.delete(e)
                except:
                    messagebox.showerror(title="Unable To Delete",message="Unable To Delete Expense From Database")
                    print("Expense That Is Not Deletable: " + str(expense_id[0]))

            #Tell The User That The Expense Has Been Deleted
            messagebox.showinfo("Expense(s) Deleted","Expense(s) Has Been Deleted")

        #button used to delete an element from the expense table
        delete_selected_button = Button(self,text="Delete Selected Expenses",command=lambda:Remove_Expenses(),font=20,width=7).grid(row=1,column=0,padx=10,pady=5,sticky='NSEW')

        #Add functionality for the widgets to resize with the window
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
