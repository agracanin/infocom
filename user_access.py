# Importing the necessary libraries
import tkinter as tk
import mysql.connector
import datetime
import os

# Importing functions from different modules
from employee_access import se_data, pr_data, hr_data, emp_se
from registration import register_user


def log_user_login(username):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username} has logged in\n"

    # Write the log entry to the audit trail file
    with open("audit_trail.txt", "a") as file:
        file.write(log_entry)

# Function to display the login credentials table


def display_table(self):

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password123",
        database="infocom"
    )

    # Function to delete a user from the login credentials table
    def delete_user(user_id):
        # Confirming the user's decision to delete the user
        confirmed = tk.messagebox.askyesno(
            "Confirm Deletion", "Are you sure you want to delete this user?")

        # If the user confirms the deletion, deleting the user from the table
        if confirmed:
            mycursor = mydb.cursor()
            mycursor.execute(
                "DELETE FROM login_credential WHERE id = %s", (user_id,))
            mydb.commit()
            mycursor.close()
            mydb.close()
            refresh()

    def get_all_roles():
        mycursor.execute("SELECT DISTINCT role FROM login_credential")
        roles = mycursor.fetchall()
        return [role[0] for role in roles]

    def change_role(user_id, current_role):
        pass

    def display_audit_trail():
        audit_file_path = "audit_trail.txt"
        try:
            if os.path.exists(audit_file_path):
                os.startfile(audit_file_path)
            else:
                tk.messagebox.showinfo("Error", "Audit trail file not found.")
        except Exception as e:
            tk.messagebox.showinfo(
                "Error", f"An error occurred while opening the audit trail: {str(e)}")

    # Function to refresh the table

    def refresh():
        table_window.destroy()
        display_table(self)

    # Fetching the data from the login credentials table
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM login_credential")
    rows = mycursor.fetchall()

    # Creating a new window for the table
    table_window = tk.Toplevel(self)
    table_window.title("Login Credentials")

    # Preventing the window from resizing with its content
    table_window.pack_propagate(False)

    # Create a frame for the table
    table_frame = tk.Frame(table_window)
    num_rows = len(rows)
    num_cols = len(rows[0])
    table_frame.pack(fill="both", expand=True)
    table_window.update_idletasks()
    table_window.geometry('{}x{}'.format(num_cols*150, (num_rows+1)*75))

    # Creating labels for each cell in the table and a button to delete the corresponding row
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            label = tk.Label(table_frame, text=cell, relief=tk.RIDGE)
            label.grid(row=i, column=j, sticky=tk.NSEW)
            delete_button = tk.Button(
                table_frame, text="Delete", command=lambda row=row: delete_user(row[0]), bg='red')
            delete_button.grid(row=i, column=num_cols, padx=5)
            change_role_button = tk.Button(
                table_frame, text="Change Role", command=lambda row=row: change_role(row[0], row[-1]))
            change_role_button.grid(row=i, column=num_cols + 1, padx=5)

    # Create a frame for the button
    button_frame = tk.Frame(table_window)
    button_frame.pack(side="bottom", fill="x")

    # Add the button to the frame
    button_se_data = tk.Button(
        button_frame, text="View SE Data", font="Arial 8 bold", command=lambda: se_data(table_window), bg='dark slate gray', fg='white')
    button_se_data.pack(pady=(5, 5))

    # Creating buttons to view different data and register a new user, and a button to refresh the table
    button_hr_data = tk.Button(
        button_frame, text="View HR Data", font="Arial 8 bold", command=lambda: hr_data(table_window), bg='dark slate gray', fg='white')
    button_hr_data.pack(pady=(0, 5))

    button_pr_data = tk.Button(
        button_frame, text="View PR Data", font="Arial 8 bold", command=lambda: pr_data(table_window), bg='dark slate gray', fg='white')
    button_pr_data.pack(pady=(0, 5))

    button_register = tk.Button(
        button_frame, text="Register New User", font="Arial 8 bold", command=lambda: register_user(), bg='dark slate gray', fg='white')
    button_register.pack(pady=(0, 5))

    button_refresh = tk.Button(
        button_frame, text="Refresh", font="Arial 8 bold", command=refresh, bg='dark slate gray', fg='white')
    button_refresh.pack(pady=(0, 5))

    button_audit = tk.Button(
        button_frame, text="Audit Trail", font="Arial 8 bold", command=display_audit_trail, bg='dark slate gray', fg='white')
    button_audit.pack(pady=(0, 5))

    # Main loop
    table_window.mainloop()
