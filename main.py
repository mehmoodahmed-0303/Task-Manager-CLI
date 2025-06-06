import json
import os
import bcrypt
import re
from datetime import datetime

USERS_FILE = 'users.json'
TASKS_FILE = 'tasks.json'

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









def main():
	initialize_files()
	while True:
		print("\nTask Manager Menu")
		print("1. Register")
		print("2. Exit")
		choice = input("Enter choice (1-2): ").strip()
		if choice == '1':
			register_user()
		elif choice == '2':
			print("Exiting...")
			break
		else:
			print("Invalid choice. please choose 1-2")
if __name__ == '__main__':
	main()