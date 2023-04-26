# user_data.py
# Used to access username and role across files
username = None
role = None

# Function to get the username


def set_username(user):
    global username
    username = user

# Function to get the role


def set_role(r):
    global role
    role = r

# Function to return username


def get_username():
    return username

# Function to return role


def get_role():
    return role
