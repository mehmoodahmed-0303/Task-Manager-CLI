import tkinter as tk
from tkinter import messagebox, ttk
import json
from main import USERS_FILE, TASKS_FILE, CURRENT_USER, create_task, list_tasks

class TaskManagerGUI:
	"""docstring for TaskManagerGUI"""

	def __init__(self, root):
		self.root = root
		self.root.title("Task Manager GUI")
		self.root.geometry("600x400")

		if not CURRENT_USER[0]:
			self.show_login()
		else:
			self.show_task_manager()

	def show_login(self):
		self.clear_window()
		tk.Label(self.root, text="Please login via Command line first.").pack(pady=20)
		tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

	def show_task_manager(self):
		self.clear_window()
		tk.Label(self.root, text=f"Logged in as {CURRENT_USER[0]}", font=('Arial',12)).pack(pady=10)

		self.tree = ttk.Treeview(self.root, columns=("ID","Title","Status","Priority","Assignee","Deadline"), show="headings")
		self.tree.heading("ID", text="ID")
		self.tree.heading("Title", text="Title")
		self.tree.heading("Status", text="Status")
		self.tree.heading("Priority", text="Priority")
		self.tree.heading("Assignee", text="Assignee")
		self.tree.heading("Deadline", text="Deadline")
		self.tree.column("ID", width=50)
		self.tree.column("Title", width=100)
		self.tree.column("Status", width=80)
		self.tree.column("Priority", width=80)
		self.tree.column("Assignee", width=80)
		self.tree.column("Deadline", width=80)
		self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
		self.refresh_tasks()

		frame = tk.Frame(self.root)
		frame.pack(pady=10)

		tk.Label(frame, text="Title:").grid(row=0, column=0)
		self.title_entry = tk.Entry(frame)
		self.title_entry.grid(row=0, column=1)

		tk.Label(frame, text="Description:").grid(row=1, column=0)
		self.desc_entry = tk.Entry(frame)
		self.desc_entry.grid(row=1, column=1)

		tk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0)
		self.deadline_entry = tk.Entry(frame)
		self.deadline_entry.grid(row=2, column=1)

		tk.Label(frame, text="Priority (low/medium/high):").grid(row=3, column=0)
		self.priority_entry = tk.Entry(frame)
		self.priority_entry.grid(row=3, column=1)

		tk.Label(frame, text="Assignee:").grid(row=4, column=0)
		self.assignee_entry = tk.Entry(frame)
		self.assignee_entry.grid(row=4, column=1)
		tk.Button(frame, text="Create Task", command=self.create_task_gui).grid(row=5, column=0)

		tk.Button(self.root, text="Refresh Task", command=self.refresh_tasks).pack(pady=5)
		tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

	def clear_window(self):
		for widget in self.root.winfo_children():
			widget.destroy()

	def refresh_tasks(self):
		for item in self.tree.get_children():
			self.tree.delete(item)
		try:
			with open(TASKS_FILE, 'r') as file:
				tasks = json.load(TASKS_FILE)
			user_tasks = [task for task in tasks if task.get('owner') == CURRENT_USER[0]]
			for task in user_tasks:
				self.tree.insert("", tk.END, values=(
				task.get('id', 'N/A')[:8],
				task.get('title', ''),
				task.get('status', 'N/A'),
				task.get('priority', ''),
				task.get('assignee', ''),
				task.get('deadline', '')
				))
		except Exception as e:
			messagebox.showerror(f"error, faild to load tasks: {e}")

	def create_task_gui(self):
		title = self.title_entry.get().strip()
		description = self.desc_entry().strip()
		deadline = self.deadline_entry().strip()
		priority = self.priority_entry().strip().lower()
		assignee = self.assignee_entry().strip().lower()

		if not title:
			messagebox.showerror("Error", "Title can not be empty.")
			return

		import sys
		from io import StringIO
		old_stdin = sys.stdin
		sys.stdin = StringIO(f"{'title'}\n{'description'}\n{'deadline'}\n{'priority'}\n{'assignee'}")
		create_task()
		sis.stdin = old_stdin

		self.refresh_tasks()
		self.title_entry.delete(0, tk.END)
		self.desc_entry.delete(0, tk.END)
		self.desc_entry.delete(0, tk.END)
		self.priority_entry.delete(0, tk.END)
		self.assignee_entry.delete(0, tk.END)
		messagebox.showinfo("Success", "Task created Successfully.")

	def logout(self):
		CURRENT_USER[0] = None
		self.show_login()


if __name__ == '__main__':
	root = tk.Tk()
	app = TaskManagerGUI(root)
	root.mainloop()
