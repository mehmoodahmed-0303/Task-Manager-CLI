import json
import os

USERS_FILE = 'users.json'
TASKS_FILE = 'tasks.json'

def initialize_files():
	if not os.path.exists(USERS_FILE):
		with open(USERS_FILE, 'w') as file:
			json.dump({}, file)
	if not os.path.exists(TASKS_FILE):
		with open(TASKS_FILE, 'w') as file:
			json.dump([], file)














def main():
	initialize_files()
	print("Task Manager Started.")

if __name__ == '__main__':
	main()