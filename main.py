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

		with open(TASKS_FILE, 'r') as file:
			tasks = json.load(file)

		task = {
		'id': str(uuid.uuid4()),
		'title': title,
		'description': description,
		'owner': CURRENT_USER[0],
		'creation date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		'status': 'pending'
		}
		tasks.append(task)

		with open(TASKS_FILE, 'w') as file:
			json.dump(tasks, file, indent=4)
		print(f"Task '{title}'' creation successful.")
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
			print("2. Log out")
			print("3. Exit")
			choice = input("Enter choice 1-3: ").strip()
			if choice == '1':
				create_task()
			elif choice == '2':
				CURRENT_USER[0] = None
				print("Logging out..")
			elif choice == '3':
				print("Exiting..")
				break
			else:
				print("Invalid choice. please enter 1-3")

if __name__ == '__main__':
	main()