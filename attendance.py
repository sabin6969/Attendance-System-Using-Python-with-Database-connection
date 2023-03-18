'''
This is a simple attendance management system in python with GUI and Database connection
Author:Sabin Poudel
Date:2023/03/17
'''

import tkinter as tk
from tkinter import ttk
import time
import mysql.connector
from tkinter import messagebox
import smtplib
import pdb

class AttendanceSystem:
    def __init__(self):
        
        self.root=tk.Tk()
        self.root.geometry('300x300')
        self.root.title("Attendance System")
        try:
            self.connection = mysql.connector.connect(host="localhost",user="root",password="",database="pythonproject")
        except:
            messagebox.showerror("Error","Couldnot Connect to Database")
            self.root.destroy()

        #------title------#
        title_label=tk.Label(self.root,text="Welcome to Attendance System",font=("sans serif",10,"bold"),fg="orange")
        title_label.pack()
        #----icon-----#
        self.root.iconbitmap('')
        def login():

            user_name=self.username_var.get()
            password=self.user_password_var.get()

             #-----checking for empty fields------#
            if len(user_name)==0 or len(password)==0:
                messagebox.showerror("Required","All Fields are required")
            cursor=self.connection.cursor()
            query=f"SELECT * FROM admins where username='{user_name}' and password='{password}'"
            cursor.execute(query)
            data=cursor.fetchone()

            #-----checking for username and password's case sensitivity------#
            try:
                if data[0]==user_name and data[1]==password:
                    messagebox.showinfo("Sucess","Login Sucess")
                    self.__name=data[0]
                    self.logged_in()
                else:
                    messagebox.showerror("Failed","Login Failed Contact Admin")
                    self.username_entry.delete(0,tk.END)
                    self.user_password_entry.delete(0,tk.END)
            except:
                messagebox.showerror("Login Failed","Contact Admin or check your details")
                self.username_entry.delete(0,tk.END)
                self.user_password_entry.delete(0,tk.END)

        #-------Username and password------#
        self.username_var=tk.StringVar()
        self.username_lable=ttk.Label(self.root,text="Username")
        self.username_entry=ttk.Entry(self.root,textvariable=self.username_var)
        self.username_lable.place(x=130,y=50)
        self.username_entry.place(x=100,y=70)
        self.username_entry.focus()

        #------password---------#
        self.user_password_var=tk.StringVar()
        self.user_password_label=ttk.Label(self.root,text="Password")
        self.user_password_label.place(x=130,y=110)
        self.user_password_entry=ttk.Entry(self.root,textvariable=self.user_password_var)
        self.user_password_entry.place(x=100,y=130)

        #-----------login button-----#
        login_button=ttk.Button(self.root,text="Login",command=login)
        login_button.place(x=120,y=160)
        self.root.mainloop()
    def logged_in(self):

        self.log_in_interface=tk.Tk()
        self.value_var=tk.StringVar()

        #--------destroying previous window------#
        self.root.destroy()

        #-------title----------#
        self.log_in_interface.title("Welcome {}".format(self.__name))

        #-------functions or commands------#
        def manual():
            self.manual_attendance()
        def face():
            self.face_attendance()

        #-----you are now logged in as -----#
        self.you_are_logged_in_as=tk.Label(self.log_in_interface,text="You are now logged in as {}".format(self.__name),font=("sans serif",10))
        self.you_are_logged_in_as.place(x=100,y=30)

        #------select class-------#
        select_division=tk.Label(self.log_in_interface,text="Select Division")
        select_division.place(x=160,y=60)

        #------dimensions-------#
        self.log_in_interface.geometry('400x400')
        self.log_in_interface.resizable(False,False)

        #--------displaying today's date------#
        t = time.ctime()
        date=t.split(' ')
        todays_date=date[0]+" "+date[1]+" "+date[2]+" "+date[-1]
        date_label=tk.Label(self.log_in_interface,text="{}".format(todays_date),font=("sans serif",10))
        date_label.place(x=290,y=0)

        #--------mark attendance------#
        mark_attendance = ttk.Button(self.log_in_interface,text="Manual Attendance",command=manual)
        mark_attendance.place(x=30,y=110)
        mark_attendance_2=ttk.Button(self.log_in_interface,text="Face Recognition",command=face)
        mark_attendance_2.place(x=270,y=110)
        #---------select division----#
        self.combobox=ttk.Combobox(self.log_in_interface,state="readonly")
        self.combobox['values']=("CEA","CEB","CEC","CED","CEE")
        self.combobox.place(x=130,y=80)
        self.combobox.current(0)
        #--------main loop------#
        self.log_in_interface.mainloop()
    def manual_attendance(self):
        #---------------call functions and methods-----------------#
        def update():
            pass
            print("inside update")
        def clear():
            # Clear the labels and checkboxes
            for widget in self.log_in_interface.winfo_children():
                if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Checkbutton):
                    widget.destroy()

        #--------------fetching data from database-----#
        cursor = self.connection.cursor()
        database_name=self.combobox.get()
        database_name=database_name.lower()
        query=f"select enrollment,name from {database_name};"
        cursor.execute(query)
        records = cursor.fetchall()
        start=140
        update_button=ttk.Button(self.log_in_interface,text="Update Attendance",command=update)
        update_button.place(x=150,y=370)
        clear_button=ttk.Button(self.log_in_interface,text="Clear Data",command=clear)
        clear_button.place(x=167,y=340)
        self.present_absent=[]

        for data in records:
            record_label=ttk.Label(self.log_in_interface,text="{} {}".format(data[0],data[1]))
            check_box_attendance=ttk.Checkbutton(self.log_in_interface)
            record_label.place(x=80,y=start)
            check_box_attendance.place(x=300,y=start)
            start+=20
    def face_attendance(self):
       pass

if __name__=="__main__":
    a = AttendanceSystem()