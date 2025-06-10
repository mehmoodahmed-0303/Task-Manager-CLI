import json
import os
import bcrypt
import re
from datetime import datetime
import uuid

USERS_FILE = 'users.json'
TASKS_FILE = 'tasks.json'
CURRENT_USER = [None]

def initialize_files():
	if not os.path.exists(USERS_FILE):
		with open(USERS_FILE, 'w') as file:
			json.dump({}, file)
	if not os.path.exists(TASKS_FILE):
		with open(TASKS_FILE, 'w') as file:
			json.dump([], file)

def is_strong_password(password):
	if len(password) < 8:
		return False, "Password must be atleast 8 characters"
	if not re.search(r"[A-Z]", password):
		return False, "Password must contain at least one uper case latter"
	if not re.search(r"[a-z]", password):
		return False, "Password must contain at least one lowercase latter"
	if not re.search(r"[0-9]", password):
		return False, "Password must contain at least one number."
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
		return False, "Password must contain at least one Special character"
	return True, ""
def is_valid_email(email):
	if not email:
		return True
	return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def register_user():
	try:
		with open(USERS_FILE, 'r') as file:
			users = json.load(file)
		while True:
			username = input("Enter user name (or cancel to exit): ").strip().lower()
			if username == 'cancel':
				print("Registration canceled.")
				return
			if not username:
				print("User name can not be empty")
				continue
			if username in users:
				print("User name already exists")
				continue
			break
		while True:
			password = input("Enter password: ").strip()
			is_strong, message = is_strong_password(password)
			if not is_strong:
				print(message)
				continue
			break
		email = input("Enter email(optional, press enter to skipp): ")
		if not is_valid_email(email):
			print("Invalid email format. Skipping email")
			email = ""

		hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		users[username] = {'password': hashed.decode(), 'email':email, 'registered_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

		with open(USERS_FILE, 'w') as file:
			json.dump(users, file, indent=4)
		print(f"User {username} registered successfuly.")
	except Exception as e:
		print(f"Error: {e}")




def login_user():
	try:
		with open(USERS_FILE, 'r') as file:
			users = json.load(file)

		while True:
			username = input("Enter user name(or cancel to exit): ").lower().strip()
			if username == 'cancel':
				print("Login canceled.")
				return
			if not username:
				print("username can not be empty.")
				continue
			if username not in users:
				print("User not found.")
				continue
			break
		
		password = input("Enter password: ").strip()
		if bcrypt.checkpw(password.encode(), users[username]['password'].encode()):
			CURRENT_USER[0] = username
			print(f"Logged in as {username}.")
			return True
		else:
			print(f"Incorrect password.")
			return False
	except Exception as e:
		print(f"Unexpected error: {e}")


def create_task():
	try:
		title = input("Enter Task title (or cancel to exit): ").strip()
		if title.lower() == 'cancel':
			print("Task creation canceled.")
			return
		if not title:
			print("Title can not be empty. exiting")
			return
		description = input("Enter task description (optional, press enter to skip)")
		deadline = input("Enter task deadline(YY-MM-DD, optional, press enter to skip): ")
		if deadline:
			try:
				datetime.strptime(deadline, '%Y-%m-%d')
			except ValueError:
				print("Invalid date format. Skipping deadline.")
				deadline = ""
		priority = input("Enter priority. (low/medium/high, default:medium): ").strip().lower()
		if priority not in ['low','medium','high']:
			priority = 'medium'

		with open(TASKS_FILE, 'r') as file:
			tasks = json.load(file)

		task = {
		'id': str(uuid.uuid4()),
		'title': title,
		'description': description,
		'owner': CURRENT_USER[0],
		'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'deadline': deadline,
		'priority': priority,
		'status': 'pending'
		}
		tasks.append(task)

		with open(TASKS_FILE, 'w') as file:
			json.dump(tasks, file, indent=4)
		print(f"Task '{title}'' creation successful.")
	except Exception as e:
		print(f"Unexpected error: {e}")


def list_tasks():
	try:
		with open(TASKS_FILE, 'r') as file:
			tasks = json.load(file)
        
        # Ensure tasks is a list
		if not isinstance(tasks, list):
			print("Error: tasks.json is corrupted. Resetting to empty list.")
			tasks = []
			with open(TASKS_FILE, 'w') as file:
				json.dump(tasks, file, indent=4)
        
		user_tasks = [task for task in tasks if task.get('owner') == CURRENT_USER[0]]
		if not user_tasks:
			print("No tasks found.")
			return
        
		print("\nYour Tasks:")
		print(f"{'ID':<36} {'Title':<20} {'Status':<10} {'Deadline':<12} {'Priority':<10} {'Created Date'}")
		for task in user_tasks:
			created_date = task.get('created_date', 'Unknown')
			print(f"{task.get('id', 'N/A'):<36} {task.get('title', '')[:19]:<20} {task.get('status', 'N/A'):<10} {task.get('deadline',''):<12} {task.get('priority', ''):<10} {created_date}")
	except json.JSONDecodeError:
		print("Error: Invalid JSON format in tasks.json.")
	except Exception as e:
		print(f"Error: {e}")


def edit_task():
	try:
		with open(TASKS_FILE, 'r') as file:
			tasks = json.load(file)

		user_tasks = [task for task in tasks if task.get('owner') == CURRENT_USER[0]]
		if not user_tasks:
			print("No tasks found to edit.")
			return
		print("\nChose task to edit.")
		print(f"{'index':<6} {'ID':<15} {'Title':<20} {'Status':<10} {'Created date'}")
		for i, task in enumerate(user_tasks, 1):
			print(f"{i:<6} {task.get('id', 'N/A')[:10]} {task.get('title', '')[:19]} {task.get('status', 'N/A')[:10]} {task.get('created_date', '')}")

		while True:
			index = input("Enter the index of task to edit. (or cancel to exit)").strip().lower()
			if index == 'cancel':
				print("Task editing canceled.")
				return
			try:
				index = int(index) - 1
				if 0 <= index <= len(task):
					break
			except ValueError:
				print("Invalid index. Enter number of canel")

		task = user_tasks[index]
		task_index = tasks.index(task)

		title = input(f"Enter new title. (current title {task.get('title', '')}), press enter to keep unchanged: ")
		if title:
			task['title'] = title

		description = input(f"Enter new description. current '{task.get('description','')}, press enter to keep unchanged': ")
		if description:
			task['description'] = description

		deadline = input(f"Enter new deadline (YYYY-MM-DD, current: {task.get('deadline', '')}, press Enter to keep): ").strip()
		if deadline:
			try:
				datetime.strptime(deadline, '%Y-%m-%d')
				task['deadline'] = deadline
			except ValueError:
				print("Invalid date format. Skipping deadline.")
		priority = input(f"Enter priority.(low/medium/high, default medium, current priority: {task.get('priority', '')})")
		if priority  in ['low', 'medium', 'high']:
			task['priority'] = priority

		status = input(f"Enter new status. (pending/complete, current {task.get('status', '')}). press enter to keep unchanged: ")
		if status:
			task['status'] = status

		tasks[task_index] = task
		with open(TASKS_FILE, 'w') as file:
			json.dump(tasks, file, indent=4)
		print("Task updated successfuly.")

	except Exception as e:
		print(f"Unexpected error: 	{e}")





def delete_task():
	try:
		with open(TASKS_FILE, 'r') as file:
			tasks = json.load(file)

		user_tasks = [task for task in tasks if task.get('owner') == CURRENT_USER[0]]
		if not user_tasks:
			print("No task found to delete.")
			return
		print("\nYour tasks")
		print(f"{'index':<6} {'ID':<10} {'Title':<20} {'Status':<20} {'Date Created'}")
		for i, task in enumerate(user_tasks, 1):
			print(f"{i:<6} {task.get('id', 'N/A')[:10]:<10} {task.get('title', '')[:19]:<20} {task.get('status', 'N/A')[:20]} {task.get('created_date', '')}")

		while True:
			index = input("Enter task index to delete (or cancel to exit): ").strip().lower()
			if index == 'cancel':
				print("Canceled.")
				return
			try:
				index = int(index) - 1
				if 0 <= index <= len(user_tasks):
					break
			except ValueError:
				print("Invalid index. Enter a number or cancel")

		task = user_tasks[index]
		tasks.remove(task)
		with open(TASKS_FILE, 'w') as file:
			json.dump(tasks, file, indent=4)
		print("Task deleted successfully.")

	except Exception as e:
		print(f"Unexpected error: {e}")

def main():
	initialize_files()
	while True:
		if not CURRENT_USER[0]:
			print("\nTask Manager Menu")
			# print(f"Current user: {CURRENT_USER[0] or 'Not logged in'}")
			print("1. Register")
			print("2. Login")
			print("3. Exit")
			choice = input("Enter choice (1-3): ").strip()
			if choice == '1':
				register_user()
			elif choice == '2':
				login_user()
			elif choice == '3':
				print("Exiting...")
				break
			else:
				print("Invalid choice. please choose 1-3")
		else:
			print(f"\nTask Manager - Logged in as {CURRENT_USER[0]}:")
			print("1. Add task")
			print("2. List Tasks")
			print("3. Edit Task")
			print("4. delete task")
			print("5. Log out")
			print("6. Exit")
			choice = input("Enter choice 1-6: ").strip()
			if choice == '1':
				create_task()
			elif choice == '2':
				list_tasks()
			elif choice == '3':
				edit_task()
			elif choice == '4':
				delete_task()
			elif choice == '5':
				print("Logging out..")
				CURRENT_USER[0] = None
			elif choice == '6':
				print("Exiting..")
				break
			else:
				print("Invalid choice. please enter 1-6")

if __name__ == '__main__':
	main()