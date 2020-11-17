from datetime import datetime
from tkinter import *
from tkinter import messagebox 
from DatabaseConnection import DbConnection
from HistoryPage import HistoryPageForm
from ViewAlertsPage import ViewAlertsPageForm

def main():
    cursor = DbConnection.conxn.cursor()
    root = Tk()
    root.title('Expense Tracker')
    
    categories = cursor.execute('SELECT * FROM Category').fetchall()
    var = []



    for c in categories:
        var.append(c[1])
    category = StringVar(root)
    category.set(var[0])

    entry_value = StringVar()

    def Submit_Clicked(amount,cat):
        amount_to_insert = amount
        cat_to_insert = cat
        date = datetime.now()

        #Loop through categories to find matching category Id
        categories = cursor.execute('SELECT * FROM Category').fetchall()
        for c in categories:
            if cat_to_insert == c[1]:
                cat_to_insert = c[0]
                break

        insert_query = '''INSERT INTO Expense (Amount,Date,CategoryId)
                          VALUES (?,?,?)'''

        cursor.execute(insert_query,amount_to_insert,date,cat_to_insert)
        DbConnection.conxn.commit()
        messagebox.showinfo("Expense Entered","You Have Entered An Expense")

        #Loop through each alert, see if there are matching categories with what was previously entered and then update the current amount that the user has spent
        alerts = cursor.execute('SELECT * FROM Alert').fetchall()
        for a in alerts:
            #If there is an alert with a matching category then increase the current amount for that alert by the amount entered
            if cat_to_insert == a[3]:
                a[2] += float(amount_to_insert)
                #Update the new current amount into the database
                update_query = '''UPDATE Alert
                                  SET CurrentAmount = (?)
                                  WHERE Alert.Id = (?)'''
                cursor.execute(update_query,a[2],a[0])
                DbConnection.conxn.commit()

                #If the current amount is larger than the max amount for an alert then alert the user that they have over spent
                if a[1] < a[2]:
                    alert_period = cursor.execute('SELECT Period.Name FROM Alert INNER JOIN Period ON Alert.PeriodId = Period.Id').fetchall()
                    messagebox.showinfo(title="Over Spending!",message="You are currently over your " + alert_period[0][0] + " limit for " + cat + "\nAmount Over Spent: " + str((a[2]-a[1])))


    amount_label = Label(root,text="Amount:",font=20,padx=10,pady=5).grid(row=0,column=0,sticky='NSEW')
    amount_entry = Entry(root,font=10,justify=RIGHT,textvariable=entry_value).grid(row=0,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

    category_label = Label(root,text="Category:",font=20,padx=10,pady=5).grid(row=1,column=0,sticky='NSEW')
    category_option_menu = OptionMenu(root,category,*var).grid(row=1,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

    history_button = Button(root,text="History",command=lambda:HistoryPageForm(root),font=20,width=7).grid(row=3,column=0,padx=10,pady=5,sticky='NSEW')
    submit_button = Button(root,text="Submit",command=lambda:Submit_Clicked(entry_value.get(),category.get()),font=20,width=7).grid(row=3,column=1,padx=10,pady=5,sticky='NSEW') #Include Submit Functionality
    alert_button = Button(root,text="Alert", command= lambda:ViewAlertsPageForm(root),font=20,width=7).grid(row=3,column=2,padx=10,pady=5,sticky='NSEW')

    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.grid_rowconfigure(2,weight=1)
    root.grid_rowconfigure(3,weight=1)

    root.mainloop()
    DbConnection.conxn.close()

if __name__ == "__main__":
    main()
