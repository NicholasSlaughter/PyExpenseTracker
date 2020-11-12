from tkinter import *;
from DatabaseConnection import DbConnection

class SetAlertPageForm(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("Set Alerts Page")