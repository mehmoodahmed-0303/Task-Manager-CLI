# 🗂️ CLI Task Manager

A command-line based task management application written in Python. It supports user registration, login, and full task lifecycle management (create, read, update, delete) — all stored locally using JSON files.

---

## 🚀 Features

- ✅ User registration & login with secure password hashing (`bcrypt`)
- ✅ Password strength and email format validation
- ✅ Task creation with:
  - Title
  - Description
  - Deadline
  - Priority (low, medium, high)
  - Optional assignee
- ✅ Edit and delete tasks
- ✅ User-specific task access and session handling
- ✅ JSON-based file storage (no database needed)

---

## 🛠️ Built With

- Python 3
- `bcrypt` for password hashing
- `json` for file storage
- `uuid` for unique task IDs
- `datetime` for timestamping
- `re` for input validation (emails, passwords)

---

## 📂 Project Structure

```
task_manager.py         # Main CLI logic and functions
users.json              # Stores registered user accounts
tasks.json              # Stores all created tasks
session.json (optional) # Used for session tracking (if implemented)
```

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/cli-task-manager.git
   cd cli-task-manager
   ```

2. Install dependencies (only `bcrypt` is external):
   ```bash
   pip install bcrypt
   ```

3. Run the app:
   ```bash
   python task_manager.py
   ```

---

## 📸 Screenshots

| Register/Login | Task Menu | Task Listing |
|----------------|-----------|---------------|
| ![Login](assets/login.png) | ![Menu](assets/menu.png) | ![List](assets/list.png) |

> *(Optional: You can add screenshots later in the `/assets` folder for better visuals)*

---

## 📌 Future Improvements

- Add task filtering/sorting by status, deadline, priority
- Add color-coded terminal output
- Implement session.json for persistent login
- Convert to GUI (Tkinter or Flask-based)

---

## 👤 Author

**Mehmood Ahmed**  
📧 [mehmood3980350@gmail.com](mailto:mehmood3980350@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/mehmoodahmed-ds)  
🔗 GitHub: [@your-username](https://github.com/your-username)

---

## 📝 License

This project is open-source and free to use.
