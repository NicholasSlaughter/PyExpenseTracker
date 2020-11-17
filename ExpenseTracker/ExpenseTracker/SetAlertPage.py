from tkinter import *
from tkinter import messagebox 
from DatabaseConnection import DbConnection

class SetAlertPageForm(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("Set Alerts Page")

        cursor = DbConnection.conxn.cursor()
        
        #Get categories to that will appear in option window
        categories = cursor.execute('SELECT * FROM Category').fetchall()
        cat = []
        try:
            for c in categories:
                cat.append(c[1])
            category = StringVar(self)
            category.set(cat[0])
        except:
            messagebox.showerror(title="No Categories",message="There is no categories in the database!")

        #Get periods to that will appear in option window
        periods = cursor.execute('SELECT * FROM Period').fetchall()
        per = []

        try:
            for p in periods:
                per.append(p[1])
            period = StringVar(self)
            period.set(per[0])
        except:
            messagebox.showerror(title="No Periods",message="There is no periods in the database!")

        entry_value = StringVar()

        def Submit_Clicked(max_amount,cat,per):
            max_amount_to_insert = max_amount
            cat_to_insert = cat
            per_to_insert = per

            #Loop through categories to find matching category Id
            categories = cursor.execute('SELECT * FROM Category').fetchall()
            for c in categories:
                if cat_to_insert == c[1]:
                    cat_to_insert = c[0]
                    break
            #Loop through periods to find matching category Id
            periods = cursor.execute('SELECT * FROM Period').fetchall()
            for p in periods:
                if per_to_insert == p[1]:
                    per_to_insert = p[0]
                    break

            insert_query = '''INSERT INTO Alert (MaxAmount,CurrentAmount,CategoryId,PeriodId)
                          VALUES (?,?,?,?)'''
            
            try:
                cursor.execute(insert_query,max_amount_to_insert,0,cat_to_insert,per_to_insert)
                DbConnection.conxn.commit()
                messagebox.showinfo("Alert Created","You Have Created An Alert")
            except:
                messagebox.showerror("Unable To Insert Alert","Alert Can Not Be Inserted Into The Database!")


        max_amount_label = Label(self,text="Max Amount:",font=20,padx=10,pady=5).grid(row=0,column=0,sticky='NSEW')
        max_amount_entry = Entry(self,font=10,justify=RIGHT,textvariable=entry_value).grid(row=0,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        category_label = Label(self,text="Category:",font=20,padx=10,pady=5).grid(row=1,column=0,sticky='NSEW')
        category_option_menu = OptionMenu(self,category,*cat).grid(row=1,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        period_label = Label(self,text="Period:",font=20,padx=10,pady=5).grid(row=2,column=0,sticky='NSEW')
        period_option_menu = OptionMenu(self,period,*per).grid(row=2,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        submit_button = Button(self,text="Submit",command=lambda:Submit_Clicked(entry_value.get(),category.get(),period.get()),font=20,width=7).grid(row=3,column=1,padx=10,pady=5,sticky='NSEW')

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)