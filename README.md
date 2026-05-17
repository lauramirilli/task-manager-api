# Task Manager API

Final project for Harvard's CS50x — a RESTful API for personal task management, built with Python and Flask.

## About the Project

This API allows users to create accounts, log in securely, and manage their personal tasks. Each user can only access their own tasks. Authentication is handled with JWT tokens, and passwords are never stored in plain text.

The project was built as part of CS50x to practice backend development concepts in a real-world context.

## Skills Developed

- Designing and building a REST API from scratch
- JWT authentication and route protection
- Password hashing with Werkzeug
- SQLite database modeling with foreign keys
- HTTP methods and status codes
- Input validation and error handling
- Environment variables and project structure best practices

## Tech Stack

- Python
- Flask
- SQLite
- PyJWT
- Werkzeug

## Endpoints

| Method | Route | Auth Required | Description |
|--------|-------|---------------|-------------|
| POST | `/register` | No | Create a new account |
| POST | `/login` | No | Login and receive a JWT token |
| GET | `/tasks` | Yes | List all tasks for the logged-in user |
| POST | `/tasks` | Yes | Create a new task |
| PATCH | `/tasks/<id>` | Yes | Update a task (title, description, or done status) |
| DELETE | `/tasks/<id>` | Yes | Delete a task |

## How to Use

### 1. Clone the repository

```bash
git clone https://github.com/lauramirilli/task-manager-api.git
cd task-manager-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of the project:

```
SECRET_KEY=your_secret_key_here
```

### 5. Initialize the database

```bash
python database.py
```

### 6. Run the server

```bash
flask --app app.py run
```

### 7. Test with Postman

- Register a user with `POST /register` sending `{"username": "...", "password": "..."}`
- Login with `POST /login` to receive your token
- Add the token to the `Authorization` header for all protected routes

## Authentication

Protected routes require a JWT token in the request header:

```
Authorization: <your_token>
```

The token is returned after a successful login.

## Project Structure

```
task-manager-api/
├── app.py           # Main application and routes
├── database.py      # Database initialization
├── requirements.txt # Project dependencies
├── .env             # Environment variables (not committed)
└── .gitignore
```