# Importing the necessary libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import datetime
import os

# Importing functions from different modules
from employee_access import se_data, pr_data, hr_data, emp_se
from registration import register_user

# Function to write logs to audit_trail.txt


def log_action(username, action):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format for writing to audit trail
    log_entry = f"{timestamp} - {username} {action}\n"

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
    def delete_user(user_id, username):
        # Confirming the users decision to delete the user
        confirmed = tk.messagebox.askyesno(
            "Confirm Deletion", "Are you sure you want to delete this user?")

        # If the user confirms the deletion, deleting the user from the table
        if confirmed:
            mycursor = mydb.cursor()
            mycursor.execute(
                "DELETE FROM login_credential WHERE id = %s", (user_id,))
            log_action(username, "has been deleted from login_credentials")
            mydb.commit()
            mycursor.close()
            mydb.close()
            refresh()

    # Change role function
    def change_role(user_id, username):
        def submit():
            selected_role = role_var.get()
            old_role = current_role.get()
            if selected_role != old_role:  # If current role and selected role do not match
                confirm = messagebox.askyesno(
                    "Confirm", "Are you sure you want to change this role?")
                # If the user confirms, update the database with the new role
                if confirm:
                    try:
                        mycursor = mydb.cursor()
                        mycursor.execute(
                            "UPDATE login_credential SET role = %s WHERE id = %s", (selected_role, user_id))
                        mydb.commit()
                        messagebox.showinfo(
                            "Success", f"Role changed successfully for user {user_id}")
                        log_action(
                            username, f"role change from {old_role} to {selected_role}")
                        change_role_window.destroy()
                        refresh()
                    # If there is a error, display to user
                    except Exception as e:
                        messagebox.showinfo(
                            "Error", f"An error occurred while changing the role: {str(e)}")

        # Creating the new window and populating a drop down menu with the roles available. Current role is preselected
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT role FROM login_credential WHERE id = %s", (user_id,))
        current_role = tk.StringVar()
        current_role.set(mycursor.fetchone()[0])

        change_role_window = tk.Toplevel()
        change_role_window.title("Change Role")

        tk.Label(change_role_window, text="Select a new role:").grid(
            row=0, column=0, pady=10, padx=10)

        # Storing our roles in an array for the dropdown menu
        roles = ["SE", "HR", "PR", "General", "Admin"]
        role_var = tk.StringVar(change_role_window)
        role_var.set(current_role.get())
        role_menu = ttk.Combobox(
            change_role_window, textvariable=role_var, values=roles, state="readonly")
        role_menu.grid(row=0, column=1, pady=10, padx=10)

        submit_button = tk.Button(
            change_role_window, text="Submit", command=submit)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Function to open the audit_trail.txt
    def display_audit_trail():
        audit_file_path = "audit_trail.txt"
        try:
            if os.path.exists(audit_file_path):
                os.startfile(audit_file_path)
            else:
                # Error handling if the file does not exist
                tk.messagebox.showinfo("Error", "Audit trail file not found.")
        except Exception as e:
            # Error handling for any other errors
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
                table_frame, text="Delete", command=lambda row=row: delete_user(row[0], row[1]), bg='red3', fg='white')
            delete_button.grid(row=i, column=num_cols, padx=5)
            change_role_button = tk.Button(
                table_frame, text="Change Role", command=lambda row=row: change_role(row[0], row[1]), bg='dark slate gray', fg='white')
            change_role_button.grid(row=i, column=num_cols + 1, padx=5)

    # Create a frame for the button
    button_frame = tk.Frame(table_window)
    button_frame.pack(side="bottom", fill="x")

    # Add the button to the frame
    button_se_data = tk.Button(
        button_frame, text="View SE Data", font="Arial 8 bold", command=lambda: se_data(table_window), bg='dark slate gray', fg='white')
    button_se_data.pack(pady=(5, 5))

    # Creating buttons to view different data and register a new user, a button to refresh the table and a button to display audit trail
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
