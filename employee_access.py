import tkinter as tk
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="infocom"
)


def se_data(parent):

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM se_data")
    rows = mycursor.fetchall()

    table_window = tk.Toplevel(parent)
    table_window.title("SE Data")

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i, column=j, sticky=tk.NSEW)

    table_window.mainloop()


def hr_data(parent):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM hr_data")
    rows = mycursor.fetchall()

    table_window = tk.Toplevel(parent)
    table_window.title("HR Data")

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i, column=j, sticky=tk.NSEW)

    table_window.mainloop()


def pr_data(parent):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pr_data")
    rows = mycursor.fetchall()

    table_window = tk.Toplevel(parent)
    table_window.title("PR Data")

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_window, text=cell, relief=tk.RIDGE)
            label.grid(row=i, column=j, sticky=tk.NSEW)

    table_window.mainloop()
