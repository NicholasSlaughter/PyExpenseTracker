from tkinter import *
from tkinter import ttk
from SetAlertPage import SetAlertPageForm
from DatabaseConnection import DbConnection

class ViewAlertsPageForm(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("View Alerts Page")

        #Define cursor to manipulate database
        cursor = DbConnection.conxn.cursor()

        #Define Tree View
        history_tree = ttk.Treeview(self)

        #Establish Column Names
        history_tree['columns'] = ('Category','Currently Spent','Max Alloted','Period')

        #Format Columns
        history_tree.column('#0',width=0) #Phantom column (if parent and child then have width greater than 0)
        history_tree.column('Category', anchor=W, width=120)
        history_tree.column('Currently Spent', anchor=CENTER, width=120)
        history_tree.column('Max Alloted', anchor=CENTER, width=120)
        history_tree.column('Period',anchor=W,width=120)

        #Create Headings
        history_tree.heading('#0',text='',anchor=W)
        history_tree.heading('Category',text='Category', anchor=W)
        history_tree.heading('Currently Spent',text='Currently Spent', anchor=CENTER)
        history_tree.heading('Max Alloted',text='Max Alloted', anchor=CENTER)
        history_tree.heading('Period',text='Period',anchor=W)

        ### Add Data ###
        #Query to get data from the expense and category tables
        alerts = cursor.execute('SELECT Category.Name, Alert.CurrentAmount, Alert.MaxAmount, Period.Name FROM Alert INNER JOIN Category ON Alert.CategoryId=Category.Id INNER JOIN Period ON Alert.PeriodId=Period.Id').fetchall()

        #Loop through the expenses and append them in a list
        var = []
        for a in alerts:
            var.append((a[0],a[1],a[2],a[3]))

        #Put Data Into Tree
        for i in range(len(var)):
            history_tree.insert(parent='',index='end',iid=i,values=(var[i][0],var[i][1],var[i][2],var[i][3]))

        #Pack To Screen
        history_tree.grid(row=0,column=0,padx=5,pady=20,sticky='NSEW')

        #Add Set Alert button that takes you to the Set Alert page
        set_alert_button = Button(self,text="Set An Alert", command= lambda:SetAlertPageForm(self),font=20,width=7).grid(row=1,column=0,padx=5,pady=5,sticky='NSEW')
        
        #Add functionality for the widgets to resize with the window
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)