import tkinter as tk
import mysql.connector
from employee_access import se_data, pr_data, hr_data
from registration import register_user


def display_table(self):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password123",
        database="infocom"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM login_credential")
    rows = mycursor.fetchall()

    table_window = tk.Toplevel(self)
    table_window.title("Login Credentials")

    # Change the geometry manager of the table_window from grid() to pack()
    table_window.pack_propagate(False)

    # Create a frame for the table
    table_frame = tk.Frame(table_window)
    num_rows = len(rows)
    num_cols = len(rows[0])
    table_frame.pack(fill="both", expand=True)
    table_window.update_idletasks()
    table_window.geometry('{}x{}'.format(num_cols*100, (num_rows+1)*50))

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_frame, text=cell, relief=tk.RIDGE)
            label.grid(row=i, column=j, sticky=tk.NSEW)

    # Create a frame for the button
    button_frame = tk.Frame(table_window)
    button_frame.pack(side="bottom", fill="x")

    # Add the button to the frame
    button_se_data = tk.Button(
        button_frame, text="View SE Data", font="Arial 8 bold", command=lambda: se_data(table_window))
    button_se_data.pack(pady=(5, 5))

    button_hr_data = tk.Button(
        button_frame, text="View HR Data", font="Arial 8 bold", command=lambda: hr_data(table_window))
    button_hr_data.pack(pady=(0, 5))

    button_pr_data = tk.Button(
        button_frame, text="View PR Data", font="Arial 8 bold", command=lambda: pr_data(table_window))
    button_pr_data.pack(pady=(0, 5))

    button_register = tk.Button(
        button_frame, text="Register New User", font="Arial 8 bold", command=lambda: register_user())
    button_register.pack(pady=(0, 5))

    table_window.mainloop()
