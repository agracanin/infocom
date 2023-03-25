# Python MySQL Authentication

This project demonstrates authentication in a Python application using MySQL as the backend database. The project uses tkinter for the graphical user interface (GUI) and mysql.connector to connect to the MySQL database. Users can log in using their username, password, and role.

## Features
- MySQL database connection
- Tkinter-based GUI for user input
- Authentication based on user credentials and role
- Customizable interface
- Simple and efficient code

## Skills Demonstrated 

- Python Programming: Proficiency in Python programming, including working with libraries, modules, and best practices.

- GUI Development with Tkinter: Designing and implementing a user-friendly graphical user interface using the Tkinter library for Python.

- MySQL Database Management: Creating and managing MySQL databases, including designing table structures, writing SQL queries, and managing data.

- Database Connectivity: Connecting to a MySQL database using the mysql.connector library and executing SQL queries from within a Python application.

- Authentication and Authorization: Implementing basic authentication and role-based access control for a secure application experience.
Error Handling and Validation: Handling user input errors, providing feedback to users, and ensuring proper data validation before processing.

- Software Design Patterns: Applying design patterns, such as Object-Oriented Programming (OOP), to create a modular and maintainable codebase.

## Roadmap

Planned features and improvements currently being worked on:

- Role-based access control: Enhancing the application to display pages and data based on the user's role after successful login. Each role will have specific access rights and be limited to certain information.

- Registration functionality: Allowing new users to register with a username, password, and role, which will be stored in the MySQL database.

- Data management: Creating role-specific pages where users can view, add, update, and delete data depending on their access rights.

- Improved security: Authenticating roles based on MySQL users rather than checking with Python. Connecting with root currently poses security flaws.

## Current Screenshots

![Main Page](/Demo%20Screenshots/loginMain.png)

![Working Login](/Demo%20Screenshots/workingLogin.png)

![Failed Login](/Demo%20Screenshots/failedLogin.png)