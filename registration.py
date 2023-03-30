import tkinter as tk
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="infocom"
)


def register_user():
    # Create a new toplevel window for user registration
    reg_window = tk.Toplevel()
    reg_window.title("Register New User")

    # Create label and entry fields for username
    username_label = tk.Label(reg_window, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    username_entry = tk.Entry(reg_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create label and entry fields for role
    role_label = tk.Label(reg_window, text="Role:")
    role_label.grid(row=1, column=0, padx=5, pady=5)

    role_entry = tk.Entry(reg_window)
    role_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create label and entry fields for password
    password_label = tk.Label(reg_window, text="Password:")
    password_label.grid(row=2, column=0, padx=5, pady=5)

    password_entry = tk.Entry(reg_window)
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    # Create the "add user" button and define its command
    def add_user():
        username = username_entry.get()
        role = role_entry.get()
        password = password_entry.get()

        if username and role and password:
            # If all fields are filled, insert the new user into the database
            mycursor = mydb.cursor()
            sql = "INSERT INTO login_credential (username, role, password) VALUES (%s, %s, %s)"
            val = (username, role, password)
            mycursor.execute(sql, val)
            mydb.commit()

            # Show a success message and close the registration window
            success_message = tk.Toplevel()
            success_message.title("Success")
            success_message_label = tk.Label(
                success_message, text="User added successfully")
            success_message_label.pack(padx=20, pady=10)
            reg_window.destroy()

        else:
            # If any field is empty, show an error message
            error_message = tk.Toplevel()
            error_message.title("Error")
            error_message_label = tk.Label(
                error_message, text="Please fill out all fields")
            error_message_label.pack(padx=20, pady=10)

    add_user_button = tk.Button(reg_window, text="Add User", command=add_user)
    add_user_button.grid(row=3, column=1, padx=5, pady=5)
