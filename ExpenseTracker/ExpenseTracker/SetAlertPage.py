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
            ONE_BILLION = 1000000000
            #Check to see if the last character for amount is a decimal point. If true then output an error else input the amount to the database
            if max_amount[-1] == ".":
                messagebox.showerror("Invalid Amount","The Max Amount Field Can Not End With A Decimal Point!")
                return
            elif float(max_amount) > ONE_BILLION:
                messagebox.showerror("Invalid Amount","The Amount Field Can Not Be Equal To Or Larger Than 1 Billion")
                return

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
                #Max length allowed is 12 (Up To 999,999,999.99)
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

        vcmd = (self.register(callback))
                
        max_amount_label = Label(self,text="Max Amount:",font=20,padx=10,pady=5).grid(row=0,column=0,sticky='NSEW')
        max_amount_entry = Entry(self,validate='all', validatecommand=(vcmd,'%d','%S'),font=10,justify=RIGHT,textvariable=entry_value).grid(row=0,column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

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