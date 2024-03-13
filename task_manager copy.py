# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist.
def load_tasks():
    '''Load tasks from 'tasks.txt' file and return a list of tasks.
        It returns a list of dictionaries representing tasks.
        Contains username, title, description, due_date, assigned_date and
        completion status.
    '''
    if not os.path.exists("tasks.txt"):
        # Create tasks.txt if it doesn't exist.
        with open("tasks.txt", "w") as default_file:
            pass
    # Read the task data from tasks.txt.        
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    # Converts the data into dictionary format.
    for t_str in task_data:
        curr_t = {}

    # Split by semicolon and manually add each component.
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account.
def load_users():
    '''Loads users from 'user.txt' file and return a dictionary mapping
        usernames to passwords.
        It returns the dictionary mpping usernames to passwords.
    '''
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

# Read user data from user.txt and converts it to a dictionary.
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

# Converts user_data to a dictionary.
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Function to write the data to file.
def write_data_to_file(data, filename):
    '''Writes the data to a file.
    '''
    with open(filename, "w") as out_file:
        out_file.writelines('\n'.join(data))

# Function to register a new user by asking for a username and password.
def reg_user(username_password):
    '''Registers a new user by prompting for a username and password. Adds to
        the 'user.txt' file.
    '''
    while True:
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Username already exists. Please enter a different username.")
        else:
            break
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm New Password: ")
    
    # If passwords match, the new user will be added to user.txt.
    if new_password == confirm_password:
        print("New user has been added.")
        username_password[new_username] = new_password
        write_data_to_file([f"{k};{v}" for k, v in username_password.items()], "user.txt")
    else:
        print("Passwords do not match.")

# Function will add a new task which will be updated in the 'tasks.txt' file.
def add_task(task_list, username_password):
    '''Adds a new task to the task list and updates 'tasks.txt'.
        task_list is a list of dictionaries representing the tasks.
        username_password is a dictionary mapping usernames to passwords.
    '''
    task_username = input("Name of the person assigned to the task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid userame.")
        return
    
    task_title = input("Title of the Task: ")
    task_description = input("Description of the Task: ")
    
    while True:
        try:
            task_due_date = input("Enter the task due date (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            # Ensures that the due date is in the future.
            if due_date_time.date() < date.today():
                print("The due date must be in the future. Please enter a \
valid date.")
                continue
            break
        except ValueError:
            print("Invalid datetime format. Please user the correct format.")
            
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    
    task_list.append(new_task) 
    # Write updated task list to tasks.txt.
    task_data = [f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime\
(DATETIME_STRING_FORMAT)};{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};\
{'Yes' if t['completed'] else 'No'}" for t in task_list]
    write_data_to_file(task_data, "tasks.txt")

    print("Task successfully added.")

# Function to view all the tasks which are displayed in the task list.   
def view_all(task_list):
    '''Displays all the tasks in the task list.
        task_list is a list of dictionaries representing the tasks.
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)    

# Function to view the tasks assigned to the current user and can allow the
# user to select a specific task they would like to view.
def view_mine(task_list, curr_user):
    '''Displays the tasks assigned to the current user and allows the user to
        select tasks for their actions.
        task_list is a list of dictionaries representing the tasks.
        curr_user is the username of the current user.
    '''
    task_number = 1
    task_map = {}
    for t in task_list:
        if t['username'] == curr_user:
            task_map[task_number] = t
            disp_str = f"Task Number: {task_number}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            task_number += 1
            
    task_number -= 1
    
    if task_number == 0:
        print("You have no tasks assigned.")
    
    # Prompt the user to select a certain task to continue with the program.    
    while True:
        choice = input("Enter the task number to select a task or enter -1 to \
return to the main menu: ")
        
        if choice == '-1':
            return
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= task_number:
                selected_task = task_map[choice]
                if selected_task['completed']:
                    print("This task has already been completed.")
                else:
                    action = input("Select an action for this task:\n1. Mark \
as complete\n2. Edit task\nEnter choice: ")
                    if action == '1':
                        selected_task['completed'] = True
                        print("Task marked as complete.")
                    elif action == '2':
                        if not selected_task['completed']:
                            new_username = input("Enter a new username or \
leave blank to keep current username: ")
                            new_due_date = input("Enter a new due date \
(YYYY-MM-DD) or leave blank to keep current due date: ")
                            
                            if new_username:
                                selected_task['username'] = new_username
                            if new_due_date:
                                selected_task['due_date'] = datetime.strptime\
(new_due_date, DATETIME_STRING_FORMAT)
                                
                            print("Task edited successfully.")
                        else:
                            print("This task cannot be edited as it is completed.")
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid task number.")
        else:
            print("Invalid input. Please enter a number or -1.")

# Function to display the statistics.
def display_statistics(username_password, task_list):
    '''Displays the statistics including number of users, tasks and generate
        reports.
        username_password is a dictionary mapping usernames to passwords.
        task_list is a list of dictionaries representing tasks.
    '''
    print("Display statistics function has been called.")
    
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        # If required files don't exist, they will be generated.
        load_tasks()
        load_users()
        print("Files have now been generated.")
        return
    
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")
    
    # Generating reports. Function below with generate these reports.
    generate_reports(num_users, num_tasks, task_list, username_password)
    
    # Displays the contents of the user overview text file.
    print("\nUser Overview Report:")
    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())
    
    # Displays the contents of the task overview text file.
    print("\nTask Overview Report:")
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())
 
# Function to generate the reports.       
def generate_reports(num_users, num_tasks, task_list, username_password):
    '''Generate tasks and user overview reports and writes them to files.
        num_users is the number of users.
        num_tasks is the number of tasks.
        task_list is a list of dictionaries representing tasks.
        username_password is a dictionary mapping usernames to passwords.
    '''
    print("Generating reports.")
    # Displays the task overview report.
    total_completed_tasks = sum(1 for task in task_list if task["completed"])
    total_incompleted_tasks = num_tasks - total_completed_tasks
    total_overdue_tasks = sum(1 for task in task_list if not task["completed"]\
and task["due_date"] < datetime.today())
    percentage_incomplete_tasks = (total_incompleted_tasks / num_tasks) * 100 \
if num_tasks > 0 else 0
    percentage_overdue_tasks = (total_overdue_tasks / num_tasks) * 100 if \
num_tasks > 0 else 0
    
    # Generates user overview report.
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview Report\n")
        task_overview_file.write("\n")
        task_overview_file.write(f"Total number of tasks: {num_tasks}\n")
        task_overview_file.write(f"Total number of completed tasks: \
{total_completed_tasks}\n")
        task_overview_file.write(f"Total number of incomplete tasks: \
{total_incompleted_tasks}\n")
        task_overview_file.write(f"Total nymber of overdue tasks: \
{total_overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: \
{percentage_incomplete_tasks:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: \
{percentage_overdue_tasks:.2f}%\n")
        
    # Displays the user overview report.
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview Report\n")
        user_overview_file.write("\n")
        user_overview_file.write(f"Total number of users: {num_users}\n")
        user_overview_file.write(f"Total number of tasks: {num_tasks}\n\n")
        
        for username in username_password.keys():
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for task in user_tasks if task['completed'])
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if not task\
                ['completed'] and task['due_date'] < datetime.today())
            percentage_user_completed_tasks = (completed_user_tasks / total_user_tasks)\
 * 100 if total_user_tasks > 0 else 0
            percentage_user_incomplete_tasks = (incomplete_user_tasks / total_user_tasks)\
 * 100 if total_user_tasks > 0 else 0
            percentage_user_overdue_tasks = (overdue_user_tasks / total_user_tasks)\
 * 100 if total_user_tasks > 0 else 0

            user_overview_file.write(f"User: {username}\n")
            user_overview_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of completed tasks: \
{percentage_user_completed_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of incomplete tasks: \
{percentage_user_incomplete_tasks:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: \
{percentage_user_overdue_tasks:.2f}%\n\n") 

# Function to display the menu and handle the users choices.
def display_menu(username_password, task_list):
    '''Displays the menu options and handles user choices.
        username_password is a dictionary mapping usernames to passwords.
        task_list is a list of dictionaries representing tasks.
    '''
    logged_in = False
    while not logged_in:
        print("Login")
        curr_user = input("Username: ") 
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist.")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Incorrect password.")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    while True:
        # Presenting the menu to the user and making sure that the user 
        # input is converted to lower case.
        print()
        menu = input('''Please select one of the following options:
r - registering user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit
: ''').lower()

        if menu == 'r':
            # Call the functuion to register a new user.
            reg_user(username_password)
        
        elif menu == 'a':
            # Add a new task.
            add_task(task_list, username_password)
        
        elif menu == 'va':
            # View all the tasks.
            view_all(task_list)
        
        elif menu == 'vm':
            # View the tasks assigned to the current user.
            view_mine(task_list, curr_user)
        
        elif menu == 'gr':
            if curr_user == 'admin':
                # Generating the reports for the admin only.
                generate_reports(len(username_password), len(task_list),\
task_list, username_password)
                # Call function to generate reports
                print("Reports have now been generated.")
            else:
                print("Only an admin can generate the reports.")
        
        elif menu == 'ds':
            if curr_user == 'admin':
                # Displays the statistics for the admin only.
                display_statistics(username_password, task_list)
            else:
                print("Only the admin can display the statistics.")
        
        elif menu == 'e':
            print("Goodbye!!!")
            exit()
        
        else:
            print("You have made a wrong choice, Please Try again")
            
username_password = load_users()
task_list = load_tasks()
display_menu(username_password, task_list)