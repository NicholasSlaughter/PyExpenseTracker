import pyodbc
from tkinter import *
from DatabaseConnection import DbConnection

def main():
    cursor = DbConnection.conxn.cursor()
    root = Tk()
    root.title('Expense Tracker')

    
    categories = cursor.execute('SELECT * FROM Category').fetchall()
    var = []
    for cat in categories:
        var.append(cat[1])
    variable = StringVar(root)
    variable.set(var[0])

    amount_label = Label(root,text="Amount:",font=20,padx=10,pady=5).grid(row=0,column=0,sticky='NSEW')
    amount_entry = Entry(root,font=10,justify=RIGHT).grid(row=0,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

    category_label = Label(root,text="Category:",font=20,padx=10,pady=5).grid(row=1,column=0,sticky='NSEW')
    category_option_menu = OptionMenu(root,variable,*var).grid(row=1,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

    history_button = Button(root,text="History",font=20,width=7).grid(row=3,column=0,padx=10,pady=5,sticky='NSEW')
    submit_button = Button(root,text="Submit",font=20,width=7).grid(row=3,column=1,padx=10,pady=5,sticky='NSEW')
    alert_button = Button(root,text="Alert",font=20,width=7).grid(row=3,column=2,padx=10,pady=5,sticky='NSEW')

    root.mainloop()
    DbConnection.conxn.close()

if __name__ == "__main__":
    main()
