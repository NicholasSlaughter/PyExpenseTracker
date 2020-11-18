from datetime import datetime
from tkinter import *
from tkinter import messagebox 
import math
from DatabaseConnection import DbConnection
from HistoryPage import HistoryPageForm
from ViewAlertsPage import ViewAlertsPageForm

def main():
    cursor = DbConnection.conxn.cursor()
    root = Tk()
    root.title('Expense Tracker')
    
    categories = cursor.execute('SELECT * FROM Category').fetchall()
    var = []

    #Get The List Of Category Names To Appear In The Option Menu
    try:
        for c in categories:
            var.append(c[1])
        category = StringVar(root)
        category.set(var[0])

        entry_value = StringVar()
    except:
        messagebox.showerror(title="No Categories",message="There is no categories in the database!")

    def Submit_Clicked(amount,cat):
        ONE_BILLION = 1000000000
        #Check to see if the last character for amount is a decimal point. If true then output an error else input the amount to the database
        if amount[-1] == ".":
            messagebox.showerror("Invalid Amount","The Amount Field Can Not End With A Decimal Point!")
            return
        elif float(amount) > ONE_BILLION:
            messagebox.showerror("Invalid Amount","The Amount Field Can Not Be Equal To Or Larger Than 1 Billion")
            return

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
        try:
            cursor.execute(insert_query,amount_to_insert,date,cat_to_insert)
            DbConnection.conxn.commit()
            messagebox.showinfo("Expense Entered","You Have Entered An Expense")
        except:
            messagebox.showerror(title="Unable To Insert",message="Unable To Insert The Expense!")

        #Loop through each alert, see if there are matching categories with what was previously entered and then update the current amount that the user has spent
        alerts = cursor.execute('SELECT * FROM Alert').fetchall()
        for a in alerts:
            #If there is an alert with a matching category then increase the current amount for that alert by the amount entered
            if cat_to_insert == a[3]:
                a[2] += float(amount_to_insert)

                #If current amount is larger than 1 billion, through an error else input the current amount to the database
                if a[2] >= (1*math.pow(10,9)):
                    messagebox.showerror("Current Amount Too Big", "Current Amount Can Not Exceed 1 billion")
                else:
                    #Update the new current amount into the database
                    update_query = '''UPDATE Alert
                                      SET CurrentAmount = (?)
                                      WHERE Alert.Id = (?)'''
                    try:
                        cursor.execute(update_query,a[2],a[0])
                        DbConnection.conxn.commit()
                    except:
                        messagebox.showerror(title="Unable To Update",message="Unable to update the current amount of the alert!")

                    #If the current amount is larger than the max amount for an alert then alert the user that they have over spent
                    if a[1] < a[2]:
                        alert_period = cursor.execute('SELECT Period.Name FROM Alert INNER JOIN Period ON Alert.PeriodId = Period.Id').fetchall()
                        messagebox.showinfo(title="Over Spending!",message="You are currently over your " + alert_period[0][0] + " limit for " + cat + "\nAmount Over Spent: " + str((a[2]-a[1])))
                    
    
    #flag if a decimal point has been used
    decimal_point_used = 0
    #Places after the decimal point in the Entry box
    places_after_dec_point = 0

    #Checks To Validate What Was Input To The Into The Entry Box
    def callback(d,S):
        nonlocal decimal_point_used
        nonlocal places_after_dec_point

        #If the text entered is a digit, a decimal point, or nothing then return true and update the Entry box
        if str.isdigit(S) or S == "." or S == "":
            #Max length allowed is 12 (up to 999,999,999.999)
            if len(entry_value.get()) < 12:
                #If the text entered is a decimal point check to see if it is being inserted or deleted
                if S == ".":
                    #If inserted (d=1) then raise the decimal point flag if it has not been used already
                    if int(d) == 1:
                        if decimal_point_used != 1:
                            places_after_dec_point = 0
                            decimal_point_used = 1
                            return True
                        else:
                            #If a decimal point has already been used then do not update the entry box
                            return False
                    else:
                        #If the decimal point is being deleted then set the decimal point flag to 0
                        decimal_point_used = 0
                        return True
                elif decimal_point_used == 1 and int(d) == 1:
                    places_after_dec_point += 1
                    if places_after_dec_point <= 2:
                        return True
                    else:
                        return False
                else:
                    #If the text entered is does not have a decimal point then we do not need further validation and return true
                    return True
            elif int(d) == 0:
                return True
            else:
                return False
        else:
            return False

    vcmd = (root.register(callback))

    amount_label = Label(root,text="Amount:",font=20,padx=10,pady=5).grid(row=0,column=0,sticky='NSEW')
    amount_entry = Entry(root, validate='all', validatecommand=(vcmd,'%d','%S'),font=10,justify=RIGHT,textvariable=entry_value).grid(row=0,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

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
