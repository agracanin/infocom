import tkinter as tk
import tkinter.messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mustang5",
    database="infocom"
)


class Form(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_interface()

    def initialize_interface(self):
        self.parent.title("Login")
        self.parent.config(background="lavender")
        self.parent.geometry("300x100")
        self.parent.resizable(False, False)

        global username
        global password
        global role

        username = tk.StringVar()
        password = tk.StringVar()
        role = tk.StringVar()

        self.labelUser = tk.Label(self.parent, text="Username: ", background="dark slate gray", foreground="White",
                                  font="Arial 8 bold")
        self.labelUser.place(x=25, y=25)

        self.entryUser = tk.Entry(self.parent, textvariable=username)
        self.entryUser.place(x=100, y=25)

        self.labelPass = tk.Label(self.parent, text="Password: ", background="dark slate gray", foreground="White",
                                  font="Arial 8 bold")
        self.labelPass.place(x=25, y=50)

        self.entryPass = tk.Entry(self.parent, textvariable=password)
        self.entryPass.place(x=100, y=50)

        self.labelRole = tk.Label(self.parent, text="Role: ", background="dark slate gray", foreground="White",
                                  font="Arial 8 bold")

        self.buttonLogin = tk.Button(self.parent, text="LOGIN", font="Arial 8 bold", command=logs)
        self.buttonLogin.place(height=45, width=60, x=230, y=25)


def logs():
    mycursor = mydb.cursor()
    sql = "SELECT role FROM login_credential WHERE BINARY username = '%s' AND BINARY password = '%s'" % (
        username.get(), password.get())
    mycursor.execute(sql)
    row = mycursor.fetchone()

    if row:
        role = row[0]
        print(f"Successfully logged in as {username.get()} with role {role}")
        welcome_message = f"Welcome {role}!"
        tk.messagebox.showinfo("Login Successful", welcome_message)
    else:
        tk.messagebox.showinfo("Error", "Invalid credentials.")


def main():
    root = tk.Tk()
    b = Form(root)
    b.mainloop()


if __name__ == "__main__":
    main()
