# Importing necessary libraries
import tkinter as tk
import tkinter.messagebox
import mysql.connector
# Function import
from user_data import set_username, set_role

# Creating a connection to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123",
    database="infocom"
)

# Creating a class to implement login form or well everything here..


class Form(tk.Frame):

    # Initializing form with constructor
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_interface()

    # Method intializing login interface
    def initialize_interface(self):

        # Setting properties of parent window
        self.parent.title("Login")
        self.parent.config(background="lavender")
        self.parent.geometry("300x100")
        self.parent.resizable(False, False)

        # Global variables for the form field
        global username
        global password
        global role

        # Initialization of variables
        username = tk.StringVar()
        password = tk.StringVar()
        role = tk.StringVar()

        # Creating the label for the username field
        self.labelUser = tk.Label(self.parent, text="Username: ", background="dark slate gray", foreground="White",
                                  font="Arial 8 bold")
        self.labelUser.place(x=25, y=25)

        # Creating the username entry field
        self.entryUser = tk.Entry(self.parent, textvariable=username)
        self.entryUser.place(x=100, y=25)

        # Creating the label for the password field
        self.labelPass = tk.Label(self.parent, text="Password: ", background="dark slate gray", foreground="White",
                                  font="Arial 8 bold")
        self.labelPass.place(x=25, y=50)

        # Creating the password entry field
        self.entryPass = tk.Entry(self.parent, textvariable=password, show='*')
        self.entryPass.place(x=100, y=50)

        # Creating the login button
        self.buttonLogin = tk.Button(
            self.parent, text="LOGIN", font="Arial 8 bold", command=self.logs, background="dark slate gray", foreground="White")
        self.buttonLogin.place(height=45, width=60, x=230, y=25)

    # Method to handle the login process

    def logs(self):
        mycursor = mydb.cursor()
        # SQL query to fetch the role based on the provided username and password
        sql = "SELECT role FROM login_credential WHERE BINARY username = '%s' AND BINARY password = '%s'" % (
            username.get(), password.get())
        # Executing and fetching the first row from the query result
        mycursor.execute(sql)
        row = mycursor.fetchone()

        # Checking if the row is not empty
        if row:
            # Importing functions here to avoid circular import
            from user_access import display_table
            from employee_access import se_data, hr_data, pr_data, general
            role.set(row[0])
            # Setting our user_data.py functions here to access in other files
            set_username(username.get())
            set_role(row[0])
            # Importing our log writing to audit trail and writing the log in
            from user_access import log_action
            log_action(username.get(), "has logged in")
            # Depending on the role, displaying different data
            if role.get() == 'Admin':
                display_table(self.parent)
            elif role.get() == 'SE':
                se_data(self.parent)
            elif role.get() == 'HR':
                hr_data(self.parent)
            elif role.get() == 'PR':
                pr_data(self.parent)
            elif role.get() == 'General':
                general(self.parent)
            else:
                # If the role is not recognized, displaying an error message
                tk.messagebox.showinfo(
                    'Error', 'Role has not been assigned. Contact admin.')
        else:
            # If the username and password combination is invalid, displaying an error message
            tk.messagebox.showinfo("Error", "Invalid credentials.")


# Main function to start application
def main():
    root = tk.Tk()
    b = Form(root)
    b.mainloop()


# Checking if run directly
if __name__ == "__main__":
    main()
