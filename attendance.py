'''
Author:Sabin Poudel
Date:2023/03/21
Title:Attendance Management System using Python's GUI Library (tkinter)
Last Modified/Edited:2023/03/21
'''
import tkinter as tk
from tkinter import ttk
import pdb
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import time
import tkcalendar

class Attendance:
    def __init__(self):   
         #---------------Initial Window-------#
        self.root=tk.Tk()
        #-----------variables for all the interface-------------#
        self.username_for_login_var=tk.StringVar() #for login only
        self.password_for_login_var=tk.StringVar() #for login only
        self.password_for_signup_var=tk.StringVar() #for signup only
        #----title-----#
        self.root.title("Attendance Management System")
        #----geometry----#
        self.root.geometry('300x300')
        #-----resizeable----#
        self.root.resizable(False,False)
        #----title of this program----#
        title_of_this_program=tk.Label(self.root,text="Attendance Management System",font=('sans serif',10),fg='blue')
        title_of_this_program.place(x=60,y=10)
        #--------labels and titles for login------#
        username_login_label=tk.Label(self.root,text="Username")
        username_login_label.place(x=120,y=40)
        username_login_entry=ttk.Entry(self.root,textvariable=self.username_for_login_var)
        username_login_entry.place(x=90,y=60)
        username_login_entry.focus()
        #------labels and entry for passwords-----#
        password_login_label=tk.Label(self.root,text="Password")
        password_login_label.place(x=120,y=90)
        password_login_entry=ttk.Entry(self.root,textvariable=self.password_for_login_var)
        password_login_entry.place(x=90,y=110)
        #----------callback functions------#
        def login():
            self.loggedin(self.username_for_login_var.get(),self.password_for_login_var.get())
        def signup():
            self.signup()
        #------loginbutton----------#
        login_button=ttk.Button(self.root,text="Login",command=login)
        login_button.place(x=115,y=140)
        #-----signupbutton---------#
        signup_button=ttk.Button(self.root,text="Signup",command=signup)
        signup_button.place(x=115,y=170)
        #----------database connection-----------#
        try:
            self.connection = mysql.connector.connect(host="localhost",password="",username="root",database="pythonproject")
        except:
            messagebox.showerror("Database not found","Couldnot connect to database")
            self.root.destroy()
        self.root.mainloop()
    def loggedin(self,username,password):
       cursor = self.connection.cursor()
       query=f"SELECT * FROM admins where username='{username}' and password='{password}'"
       try:
           cursor.execute(query)
           data = cursor.fetchone()
           if data[0]==username and data[1]==password:
               messagebox.showinfo("Sucess","Login Sucess")
               self.login_sucess(data[0])
           else:
               messagebox.showerror("Login Failed","Please Check your Details Again")
       except:
           messagebox.showerror("Login Failed","Your Account Doesnot exists")
    def signup(self):
        #-----signup interface--------#
        signup_interface=tk.Tk()
        #-----variables for signup----#
        self.username_for_signup_var=tk.StringVar() #for signup only
        #-------title-----------#
        signup_interface.title("Create Account")
        #----geometry-----#
        signup_interface.geometry('300x300')
        signup_interface.resizable(False,False)
        #-------lables for username and entry------#
        username_for_signup_label=tk.Label(signup_interface,text="Define Username")
        username_for_signup_label.place(x=105,y=40)
        username_entry_for_signup=ttk.Entry(signup_interface,textvariable=self.username_for_signup_var)
        username_entry_for_signup.place(x=90,y=60)
        #-------------lables for password and entry-----#
        password_for_signup_label=tk.Label(signup_interface,text="Define Password")
        password_for_signup_label.place(x=105,y=90)
        password_entry_for_signup=ttk.Entry(signup_interface,textvariable=self.password_for_signup_var)
        password_entry_for_signup.place(x=90,y=110)
        #----callback function----#
        def createaccount():
            self.createaccountwithus(username_entry_for_signup.get(),password_entry_for_signup.get())
        #-----create account button------#
        create_account_button=ttk.Button(signup_interface,text="Create Account",command=createaccount)
        create_account_button.place(x=105,y=140)
        signup_interface.mainloop()
    def createaccountwithus(self,username,password):
        query=f"INSERT INTO admins values('{username}','{password}')"
        cursor=self.connection.cursor()
        try:
            cursor.execute(query)
            messagebox.showinfo("Account Created","Account Created Sucess,Proceed towards login")
            self.connection.commit()
        except:
            messagebox.showerror("Username already in use","This username is already in use choose another username")
    def login_sucess(self,username):
        self.root.destroy()
        login_sucess_interface=tk.Tk()
        #-------title--------#
        login_sucess_interface.title(f"Welcome {username}")
        #----geometry-------#
        login_sucess_interface.geometry('450x450')
        login_sucess_interface.resizable(False,False)
        #-------date display----#
        t = time.ctime()
        date=t.split(' ')
        todays_date=date[0]+" "+date[1]+" "+date[2]+" "+date[-1]
        date_label=tk.Label(login_sucess_interface,text="{}".format(todays_date),font=("sans serif",10))
        date_label.place(x=340,y=0)
        #-----you are now logged in as ----#
        logged_in_as_label=tk.Label(login_sucess_interface,text=f"You are now logged in as {username}",font=("sans serif",11))
        logged_in_as_label.place(x=135,y=20)
        #------select divisions-----#
        select_division=tk.Label(login_sucess_interface,text="Select Division")
        select_division.place(x=200,y=50)
        #------divisions combobox-------#
        divisions_combobox=ttk.Combobox(login_sucess_interface,state="readonly",width=30)
        divisions_combobox['values']=("CEA","CEB","CEC","CED","CEE")
        divisions_combobox.current(0)
        divisions_combobox.place(x=140,y=80)
        #--------callback functions----#
        def getdetails():
            cursor = self.connection.cursor()
            division_name = divisions_combobox.get()
            division_name = division_name.lower()
            query = f"SELECT enrollment, name FROM {division_name};"
            cursor.execute(query)
            self.data = cursor.fetchall()
            start = 150
            self.checkboxes = []  # create a list to store the checkboxes
            for enrollment, name in self.data:
                records_label = ttk.Label(login_sucess_interface, text=f"{enrollment} {name}")
                records_label.place(x=145, y=start)
                checkbox = ttk.Checkbutton(login_sucess_interface)
                checkbox.place(x=350, y=start)
                self.checkboxes.append(checkbox)  # add the checkbox to the list
                start += 20
        def update():
            final_check=[]
            selected_date = date_entry.get_date()
            for checkbox in self.checkboxes:
                value = checkbox.instate(['selected'])
                final_check.append(value)
            details_with_status=list(zip(self.data,final_check))
            # print(details_with_status)
            for details in details_with_status:
                if False in details:
                    division=divisions_combobox.get()
                    try:
                        enrollment=details[0][0]
                        query = f"UPDATE {division} SET status='Absent',date_day='{selected_date}' where enrollment='{enrollment}'"
                        cursor=self.connection.cursor()
                        cursor.execute(query)
                        self.connection.commit()
                    except:
                        messagebox.showerror("Failed","Failed to Update Attendance")
                else:
                    division=divisions_combobox.get()
                    try:
                        enrollment=details[0][0]
                        query = f"UPDATE {division} SET status='Present',date_day='{selected_date}' where enrollment='{enrollment}'"
                        cursor=self.connection.cursor()
                        cursor.execute(query)
                        self.connection.commit()
                    except:
                        messagebox.showerror("Failed","Failed to Update Attendance")
            else:
                messagebox.showinfo("Sucess","Attendance Updated Sucessfully")
        def cleardata():
            # Clear the labels and checkboxes
            for widget in login_sucess_interface.winfo_children():
                if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Checkbutton):
                    widget.destroy()
        #------date entry------#
        date_entry = tkcalendar.DateEntry(login_sucess_interface, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.place(x=190,y=110)
        #-----student details-----#
        student_details_button=ttk.Button(login_sucess_interface,text="Get Students Details",command=getdetails)
        student_details_button.place(x=10,y=110)
        #-----clear data-------#
        clear_data_button=ttk.Button(login_sucess_interface,text="Clear Data",command=cleardata)
        clear_data_button.place(x=360,y=110)
        #----update attendance button-----#
        update_attendance=ttk.Button(login_sucess_interface,text="Update Attendance",command=update)
        update_attendance.place(x=180,y=400)
        login_sucess_interface.mainloop()
        
if __name__=="__main__":
    a= Attendance()
