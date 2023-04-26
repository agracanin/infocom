# Importing required libraries
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from user_data import get_role, get_username

# SQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="infocom"
)

# Function to create the insert data form


def insert_data_form(parent, table_name):
    mycursor = mydb.cursor()
    mycursor.execute(f"DESCRIBE {table_name}")
    columns = mycursor.fetchall()

    # Creating a new window for the form
    form_window = tk.Toplevel(parent)
    form_window.title(f"Insert Data into {table_name}")

    # Creating labels and input fields for each column
    input_vars = []
    for i, column in enumerate(columns):
        label = tk.Label(form_window, text=column[0])
        label.grid(row=i, column=0, padx=(10, 5), pady=5)

        input_var = tk.StringVar()
        input_entry = tk.Entry(form_window, textvariable=input_var)
        input_entry.grid(row=i, column=1, padx=(5, 10), pady=5)

        input_vars.append(input_var)

    # Function to handle form submission
    def submit_form():
        input_values = [input_var.get() for input_var in input_vars]

        # Check if all fields are filled
        if all(input_values):
            # Insert the data into the table
            query = f"INSERT INTO {table_name} ({', '.join(column[0] for column in columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            mycursor.execute(query, input_values)
            mydb.commit()
            # Success message
            messagebox.showinfo("Success", "Data inserted successfully")
            # Setting our username and calling log_action to write to audit_trail
            username = get_username()
            from user_access import log_action  # To avoid circular import
            log_action(username, f"has inserted data into {table_name}")
            form_window.destroy()
        else:
            # Error handling
            messagebox.showerror("Error", "Please fill all fields")

    # Adding the submit button
    submit_button = tk.Button(form_window, text="Submit", command=submit_form)
    submit_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    form_window.mainloop()


def custom_select_query(parent):
    # Store the role in role variable
    role = get_role()
    # Create a list of tables that can be accessed based on the user's role
    allowed_tables = []
    if role == "Admin":
        allowed_tables = ["login_credential", "se_data",
                          "emp_se", "hr_data", "emp_hr", "emp_pr", "pr_data"]
    elif role == "SE":
        allowed_tables = ["se_data", "emp_se"]
    elif role == "HR":
        allowed_tables = ["hr_data", "emp_hr", "emp_se", "emp_pr"]
    elif role == "PR":
        allowed_tables = ["emp_pr", "pr_data", "emp_se", "emp_hr"]
    elif role == "General":
        allowed_tables = ["emp_se", "emp_hr", "emp_pr"]
    else:
        # If the role is not recognized, display an error message and return
        messagebox.showerror("Error", "Role not recognized")
        return
    # Create a new window for the query form
    query_window = tk.Toplevel(parent)
    query_window.title("Custom SELECT Query")

    # Label for the query entry field
    query_label = tk.Label(query_window, text="Enter your SELECT query:")
    query_label.pack(padx=(10, 10), pady=(10, 0))

    # Entry field for the query
    query_entry = tk.Entry(query_window, width=60)
    query_entry.pack(padx=(10, 10), pady=(5, 10))

    # Function to execute the entered query and display results
    def execute_query():
        query = query_entry.get()
        try:
            # Parse the query to get the table name
            table_name = query.split()[3]

            # Check if the table is allowed based on the user's role
            if table_name in allowed_tables:
                mycursor = mydb.cursor()
                mycursor.execute(query)
                rows = mycursor.fetchall()
                column_names = [desc[0] for desc in mycursor.description]

                # Create a new window to display the results
                results_window = tk.Toplevel(query_window)
                results_window.title("Results")

                # Display the column names and row data
                for j, column_name in enumerate(column_names):
                    label = tk.Label(
                        results_window, text=column_name, relief=tk.RIDGE)
                    label.grid(row=0, column=j, sticky=tk.NSEW)

                for i, row in enumerate(rows):
                    for j, cell in enumerate(row):
                        label = tk.Label(
                            results_window, text=cell, relief=tk.RIDGE)
                        label.grid(row=i+1, column=j, sticky=tk.NSEW)
            else:
                # If the table is not allowed, display an error message
                messagebox.showerror(
                    "Error", f"You are not authorized to access the {table_name} table.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Add a submit button to execute the query
    submit_button = tk.Button(
        query_window, text="Submit", command=execute_query)
    submit_button.pack(pady=(5, 10))

    query_window.mainloop()

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
    # Adding all the wonderful buttons!
    emp_se_button = tk.Button(table_window, text="View SE Employees", bg='dark slate gray', fg='white',
                              command=lambda: emp_se(parent))
    emp_se_button.grid(row=i+2, column=0,
                       columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "se_data"))
    insert_data_button.grid(row=i+3, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), se_data(parent)])
    refresh_button.grid(row=i+4, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    custom_query_button = tk.Button(table_window, text="Custom SELECT Query", bg='navy', fg='white',
                                    command=lambda: custom_select_query(parent))
    custom_query_button.grid(row=i+5, column=0,
                             columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

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

    # Adding all the wonderful buttons!
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
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "hr_data"))
    insert_data_button.grid(row=i+5, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), hr_data(parent)])
    refresh_button.grid(row=i+6, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    custom_query_button = tk.Button(table_window, text="Custom SELECT Query", bg='navy', fg='white',
                                    command=lambda: custom_select_query(parent))
    custom_query_button.grid(row=i+7, column=0,
                             columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

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

    # Adding all the wonderful buttons!
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
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "pr_data"))
    insert_data_button.grid(row=i+5, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), pr_data(parent)])
    refresh_button.grid(row=i+6, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))
    custom_query_button = tk.Button(table_window, text="Custom SELECT Query", bg='navy', fg='white',
                                    command=lambda: custom_select_query(parent))
    custom_query_button.grid(row=i+7, column=0,
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

    # Insert and refresh buttons
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "emp_se"))
    insert_data_button.grid(row=i+2, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), emp_se(parent)])
    refresh_button.grid(row=i+3, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

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

    # Insert and refresh buttons
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "emp_hr"))
    insert_data_button.grid(row=i+2, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), emp_hr(parent)])
    refresh_button.grid(row=i+3, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

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

    # Insert and refresh buttons
    insert_data_button = tk.Button(table_window, text="Insert Data", bg='green4', fg='white',
                                   command=lambda: insert_data_form(parent, "emp_pr"))
    insert_data_button.grid(row=i+2, column=0,
                            columnspan=len(column_names), sticky=tk.NSEW, pady=(5, 5))
    refresh_button = tk.Button(table_window, text="Refresh", bg='dark slate gray', fg='white',
                               command=lambda: [
                                   table_window.destroy(), emp_pr(parent)])
    refresh_button.grid(row=i+3, column=0,
                        columnspan=len(column_names), sticky=tk.NSEW, pady=(0, 5))

    table_window.mainloop()

# Function for general role log in display


def general(parent):
    # Create a new top-level window as a child of the parent window
    table_window = tk.Toplevel(parent)
    table_window.title("General Portal")
    table_window.geometry('450x300')

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
    # Select query button
    custom_query_button = tk.Button(button_frame, text="Custom SELECT Query", bg='navy', fg='white',
                                    command=lambda: custom_select_query(parent))
    custom_query_button.pack(side='top', fill='x', pady=(5, 5))

    table_window.mainloop()
