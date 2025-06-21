# TaskManagerCLI

A secure, user-friendly command-line task manager built with Python.\
Supports user registration with password hashing, login authentication, and full CRUD operations on personal tasks — all stored in JSON files.

---

## 📌 Features

- 🔐 User registration with **password strength checks** and **bcrypt hashing**
- 🔑 Secure login system
- ✅ Create, view, edit, delete tasks
- 📝 Each task supports:
  - Title, description, deadline, priority, status
  - Optional assignee from registered users
- 📓 Tasks and users stored in JSON files (`tasks.json`, `users.json`)
- 📂 Local persistence (no database required)
- 🗓️ Timestamp tracking for registration and task creation

---

## 📁 Project Structure

```
TaskManagerCLI/
│
├── app.py             # Main application logic
├── users.json         # Auto-generated user database
├── tasks.json         # Auto-generated task records
├── requirements.txt   # Required Python packages
└── README.md          # This file
```

---

## ⚙️ Requirements

Include the following in `requirements.txt`:

```
bcrypt
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/TaskManagerCLI.git
cd TaskManagerCLI
```

2. **Create and activate virtual environment**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```

---

## 🧑‍💻 Usage

- Run the app.
- Register a new user.
- Login with your credentials.
- Manage tasks (Add, List, Edit, Delete).
- Logout or exit anytime.

---

## 🔒 Password Policy

- At least 8 characters
- One uppercase letter
- One lowercase letter
- One digit
- One special character (e.g., `!@#$%`)

# Task Manager

A Python-based command-line application for managing tasks with user accounts and collaboration features.

## Status
Under development.