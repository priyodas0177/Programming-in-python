import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
                break

    def mark_task_complete(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                break

    def change_password(self, new_password):
        self.password = new_password


class ToDoApp:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_users()

    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
                for user_data in users_data:
                    user = User(user_data['username'], user_data['password'])
                    user.tasks = user_data['tasks']
                    self.users[user.username] = user
        except FileNotFoundError:
            pass

    def save_users(self):
        users_data = []
        for user in self.users.values():
            user_data = {
                'username': user.username,
                'password': user.password,
                'tasks': user.tasks
            }
            users_data.append(user_data)

        with open('users.json', 'w') as file:
            json.dump(users_data, file)

    def register(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose another one.")
            return False
        self.users[username] = User(username, password)
        self.save_users()
        print("Registration successful.")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print(f"Welcome, {username}!")
            return True
        print("Invalid username or password.")
        return False

    def add_task(self, title, description, priority=0, due_date=None):
        if self.current_user:
            task = {
                'title': title,
                'description': description,
                'priority': priority,
                'due_date': due_date,
                'completed': False
            }
            self.current_user.add_task(task)
            self.save_users()
            print("Task added successfully.")
        else:
            print("Please log in first.")

    def remove_task(self, task_id):
        if self.current_user:
            task_list = self.current_user.tasks
            if 0 < task_id <= len(task_list):
                task_list.pop(task_id - 1)
                self.current_user.tasks = task_list 
                self.save_users()
                print("Task removed successfully.")
            else:
                print('Enter a valid id (0 to', len(task_list), ')')
        else:
            print("Please log in first.")

    def mark_task_complete(self, task_id):
        if self.current_user:
            task_list = self.current_user.tasks
            if 0 < task_id <= len(task_list):
                task_list[task_id - 1]['completed'] = True
                self.current_user.tasks = task_list 
                self.save_users()
                print("Task marked as complete.")
            else:
                print('Enter a valid id (0 to', len(task_list), ')')
        else:
            print("Please log in first.")

    def view_tasks(self):
        if self.current_user:
            print("Your tasks:")
            for i, task in enumerate(self.current_user.tasks):
                print(f'Task {i + 1}:')
                for key, value in task.items():
                    print(f'  {key}: {value}')
        else:
            print("Please log in first.")
    
    def edit_task(self, task_id):
        if self.current_user:
            task_list = self.current_user.tasks
            if 0 < task_id <= len(task_list):
                print("Editing task #", task_id)
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                priority = int(input("Enter task priority (0 for lowest): "))
                due_date = input("Enter due date (YYYY-MM-DD): ")

                task_list[task_id - 1]['title'] = title
                task_list[task_id - 1]['description'] = description 
                task_list[task_id - 1]['priority'] = priority
                task_list[task_id - 1]['due_date'] = due_date

                self.current_user.tasks = task_list 
                self.save_users()
                print("Task Edited")
            else:
                print('Enter a valid id (0 to', len(task_list), ')')
        else:
            print("Please log in first.")

    def filter_tasks(self, completed=1):
        if self.current_user:
            print("Filtered tasks:")
            if completed == 1: 
                filtered_tasks = [task for task in self.current_user.tasks if task['completed'] == True]
                print("Your tasks:")
                for i, task in enumerate(filtered_tasks):
                    print(f'Task {i + 1}:')
                    for key, value in task.items():
                        print(f'  {key}: {value}')
            elif completed == 2:
                filtered_tasks = [task for task in self.current_user.tasks if task['completed'] == False]
                print("Your tasks:")
                for i, task in enumerate(filtered_tasks):
                    print(f'Task {i + 1}:')
                    for key, value in task.items():
                        print(f'  {key}: {value}')
            else:
                print('Invalid input')
        else:
            print("Please log in first.")

    def sort_by_priority(self):
        if self.current_user:
            task_list = self.current_user.tasks
            sorted_tasks = sorted(task_list, key=lambda task: task['priority'], reverse=True)

            print("Your completed tasks (sorted by priority - descending):")
            for i, task in enumerate(sorted_tasks):
                print(f'Task {i + 1}:')
                for key, value in task.items():
                    print(f' {key}: {value}')


    def change_password(self, new_password):
        if self.current_user:
            self.current_user.change_password(new_password)
            self.save_users()
            print("Password changed successfully.")
        else:
            print("Please log in first.")


if __name__ == "__main__":
    todo_app = ToDoApp()
    loggedIn = False
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            todo_app.register(username, password)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            loggedIn = todo_app.login(username, password)
            if loggedIn: break
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

    if loggedIn:
        while True:
            print("\n1. Add Task\n2. Edit Task\n3. Remove Task\n4. Mark Task Complete")
            print("5. View Tasks\n6. Filter Tasks\n7. Sort Task By Priority\n8. Change Password\n9. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                priority = int(input("Enter task priority (0 for lowest): "))
                due_date = input("Enter due date (YYYY-MM-DD): ")
                todo_app.add_task(title, description, priority, due_date)

            elif choice == "2":
                todo_app.view_tasks()
                task_id = int(input("Enter task ID to Edit: "))
                todo_app.edit_task(task_id)

            elif choice == "3":
                todo_app.view_tasks()
                task_id = int(input("Enter task ID to remove: "))
                todo_app.remove_task(task_id)

            elif choice == "4":
                todo_app.view_tasks()
                task_id = int(input("Enter task ID to mark as complete: "))
                todo_app.mark_task_complete(task_id)

            elif choice == "5":
                todo_app.view_tasks()

            elif choice == "6":
                completed = int(input("Filter tasks by completion status\n1. Completed Tasks\n2. incomplete task\nYour choice: "))
                todo_app.filter_tasks(completed)

            elif choice == "7":
                todo_app.sort_by_priority()

            elif choice == "8":
                new_password = input('Enter new password: ')
                new_password_2 = input("ReEnter new password: ")
                if new_password == new_password_2:
                    todo_app.change_password(new_password)
                else:
                    print('Password doesn\'t match')

            elif choice == "9":
                todo_app.save_users()
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")
