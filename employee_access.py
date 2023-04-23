# Importing required libraries
import tkinter as tk
import mysql.connector

# SQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="infocom"
)

# Function to display 'se_data' table from MySQL


def se_data(parent):

    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM se_data")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # Creating a new window for displaying SE data
    table_window = tk.Toplevel(parent)
    table_window.title("SE Data")

    # Creating labels for column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Creating labels for each row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)
    # Adding button to view emp_se table
    emp_se_button = tk.Button(table_window, text="View SE Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_se(parent))
    emp_se_button.grid(row=i+2, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW)

    table_window.mainloop()


# Function to display 'hr_data' table from MySQL
def hr_data(parent):
    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM hr_data")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # Creating a new window for displaying HR data
    table_window = tk.Toplevel(parent)
    table_window.title("HR Data")

    # Creating labels for column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Creating labels for each row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)

    # Adding buttons to view HR, SE and PR employees
    emp_hr_button = tk.Button(table_window, text="View HR Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_hr(parent))
    emp_hr_button.grid(row=i+2, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))

    emp_se_button = tk.Button(table_window, text="View SE Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_se(parent))
    emp_se_button.grid(row=i+3, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

    emp_pr_button = tk.Button(table_window, text="View PR Employees",
                              bg='dark slate gray', fg='white', command=lambda: emp_pr(parent))
    emp_pr_button.grid(row=i+4, column=0,
                       columnspan=len(column_names), stick=tk.NSEW, pady=(0, 5))

    table_window.mainloop()

# Function to display 'pr_data' table from MySQL


def pr_data(parent):
    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_data")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # New window creation
    table_window = tk.Toplevel(parent)
    table_window.title("PR Data")

    # Creating labels for column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Creating labels for row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)

    # Buttons for emp_pr, emp_hr, emp_se tables
    emp_pr_button = tk.Button(table_window, text="View PR Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_pr(parent))
    emp_pr_button.grid(row=i+2, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 0))

    emp_hr_button = tk.Button(table_window, text="View HR Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_hr(parent))
    emp_hr_button.grid(row=i+3, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))

    emp_se_button = tk.Button(table_window, text="View SE Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_se(parent))
    emp_se_button.grid(row=i+4, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

    table_window.mainloop()

# Function to display 'emp_se' table from MySQL


def emp_se(parent):
    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM emp_se")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # Create new window
    table_window = tk.Toplevel(parent)
    table_window.title("SE Employees")

    # Fill column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Fill row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)

    table_window.mainloop()

# Function displaying 'emp_hr' table from MySQL


def emp_hr(parent):
    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM emp_hr")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # New window creation
    table_window = tk.Toplevel(parent)
    table_window.title("HR Employees")

    # Fill all column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Fill all row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)

    table_window.mainloop()


# Function to display 'emp_pr' table from MySQL
def emp_pr(parent):
    # Select all rows and store column names
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM emp_pr")
    rows = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]

    # New window creation
    table_window = tk.Toplevel(parent)
    table_window.title("PR Employees")

    # Fill column names
    for j, column_name in enumerate(column_names):
        label = tk.Label(table_window, text=column_name, relief=tk.RIDGE)
        label.grid(row=0, column=j, sticky=tk.NSEW)

    # Fill row data
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i+1, column=j, sticky=tk.NSEW)

    table_window.mainloop()

# Function for general role log in display


def general(parent):
    # Create a new top-level window as a child of the parent window
    table_window = tk.Toplevel(parent)
    table_window.title("General Portal")
    table_window.geometry('200x150')

    # Label for the title of the window
    title_label = tk.Label(
        table_window, text="General Portal", font=("Arial", 14))
    title_label.pack(pady=(10, 10))

    # Frame to store buttons
    button_frame = tk.Frame(table_window)
    button_frame.pack(expand=True)

    # Buttons create to view 'emp_hr', 'emp_pr', 'emp_se' tables from MySQL
    emp_hr_button = tk.Button(button_frame, text="View HR Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_hr(parent))
    emp_hr_button.pack(side='top', fill='x', pady=(5, 0))

    emp_pr_button = tk.Button(button_frame, text="View PR Employees",
                              bg='dark slate gray', fg='white', command=lambda: emp_pr(parent))
    emp_pr_button.pack(side='top', fill='x', pady=(5, 0))

    emp_se_button = tk.Button(button_frame, text="View SE Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_se(parent))
    emp_se_button.pack(side='top', fill='x', pady=(5, 0))

    table_window.mainloop()
