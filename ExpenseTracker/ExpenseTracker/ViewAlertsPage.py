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
        alert_tree = ttk.Treeview(self)

        #Establish Column Names
        alert_tree['columns'] = ('Id','Category','Currently Spent','Max Alloted','Period')

        #Format Columns
        alert_tree.column('#0',width=0,minwidth=0) #Phantom column (if parent and child then have width greater than 0)
        alert_tree.column('Id',width=0,minwidth=0)
        alert_tree.column('Category', anchor=W, width=120)
        alert_tree.column('Currently Spent', anchor=CENTER, width=120)
        alert_tree.column('Max Alloted', anchor=CENTER, width=120)
        alert_tree.column('Period',anchor=W,width=120)

        #Create Headings
        alert_tree.heading('#0')
        alert_tree.heading('Id')
        alert_tree.heading('Category',text='Category', anchor=W)
        alert_tree.heading('Currently Spent',text='Currently Spent', anchor=CENTER)
        alert_tree.heading('Max Alloted',text='Max Alloted', anchor=CENTER)
        alert_tree.heading('Period',text='Period',anchor=W)

        ### Add Data ###
        #Query to get data from the alert and category tables
        alerts = cursor.execute('SELECT Alert.Id, Category.Name, Alert.CurrentAmount, Alert.MaxAmount, Period.Name FROM Alert INNER JOIN Category ON Alert.CategoryId=Category.Id INNER JOIN Period ON Alert.PeriodId=Period.Id').fetchall()

        #Loop through the alerts and append them in a list
        var = []
        for a in alerts:
            var.append((a[0],a[1],a[2],a[3],a[4]))

        #Put Data Into Tree
        for i in range(len(var)):
            alert_tree.insert(parent='',index='end',iid=i,values=(var[i][0],var[i][1],var[i][2],var[i][3],var[i][4]))

        #Pack To Screen
        alert_tree.grid(row=0,column=0,padx=5,pady=20,sticky='NSEW')

        #Delete Selected Alerts
        def Remove_Alerts():
            nonlocal alert_tree
            alerts_to_remove = alert_tree.selection()
            #Loop through the selected alerts and delete them from both the tree and the database
            for a in alerts_to_remove:
                #Get the the Id of the alert in the database
                alert_id = alert_tree.item(a)['values']
                
                #Set up query used to delete an element from the alert table
                delete_query = '''DELETE FROM Alert WHERE Id = (?)'''

                #The Id is the 1st element in the array to scope to that and delete it from the db
                cursor.execute(delete_query,alert_id[0])
                DbConnection.conxn.commit()

                #delete alert from tree to sync with database
                alert_tree.delete(a)

        #button used to delete an element from the alert table
        delete_selected_button = Button(self,text="Delete Selected Alerts",command=lambda:Remove_Alerts(),font=20,width=7).grid(row=1,column=0,padx=10,pady=5,sticky='NSEW')

        #Add Set Alert button that takes you to the Set Alert page
        set_alert_button = Button(self,text="Set An Alert", command= lambda:SetAlertPageForm(self),font=20,width=7).grid(row=1,column=1,padx=5,pady=5,sticky='NSEW')
        
        #Add functionality for the widgets to resize with the window
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)