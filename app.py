from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from functools import wraps
import jwt
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

secret_key = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.json.sort_keys = False

def get_db():
    conn = sqlite3.connect("tasks.db")
    return conn


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401

        token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        return f(payload, *args, **kwargs)
    return decorated

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Must inform username and password"}), 400
    
    try:
        username = data["username"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Key must contain username and password"}),400

    hash = generate_password_hash(password)

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hash))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}),409

    return jsonify("User registered sucessfullly!")


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Must inform username and password"}), 400
    
    try:
        username = data["username"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Key must contain username and password"}), 400
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    # result[0] -> user_id
    # result[1] -> password hash 
    conn.close()

    if result is None:
        return jsonify({"error": "Invalid username or password"}), 401
    else:
        password_hash = result[1]
        hash_check = check_password_hash(password_hash, password)
        if hash_check:
            user_id = result[0]
            payload = {
                "user_id": user_id
            }
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            return jsonify({"token": token})
        else:
            return jsonify({"error": "Invalid username or password"}), 401
        
@app.route("/tasks", methods=['GET'])
@token_required
def tasks_get(payload):

    user_id = payload["user_id"]

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT title, description, done, created_at, id FROM tasks WHERE user_id = ?", (user_id,))
    tasks = c.fetchall()
    conn.close()

    result = []
    for task in tasks:
        result.append({
            "title": task[0],
            "description": task[1],
            "done": bool(task[2]),
            "created_at": task[3],
            "id": task[4]
        })

    return jsonify(result)

@app.route("/tasks", methods=['POST'])
@token_required
def tasks_post(payload):

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Must inform at least title"}), 400

    title = data.get("title")
    description = data.get("description", None)

    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    user_id = payload["user_id"]
    created_at = datetime.now().isoformat()

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, title, description, done, created_at) VALUES (?, ?, ?, ?, ?)", (user_id, title, description, 0, created_at))
    conn.commit()
    conn.close()

    return jsonify("Task succesfully created!")

@app.route("/tasks/<id>", methods=['DELETE'])
@token_required
def tasks_delete(payload, id):
    
    user_id = payload["user_id"]

    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (id, user_id))
    conn.commit()
    conn.close()
    if c.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify("Task succesfully deleted!")

@app.route("/tasks/<id>", methods=['PATCH'])
@token_required
def tasks_update(payload, id):

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Must inform an update"}), 400
    
    update_title = data.get("update_title")
    update_description = data.get("update_description")
    update_done = data.get("update_done")

    user_id = payload["user_id"]

    fields = []
    values = []

    if update_title is not None:
        fields.append("title = ?")
        values.append(update_title)

    if update_description is not None:
        fields.append("description = ?")
        values.append(update_description)

    if update_done is not None:
        fields.append("done = ?")
        values.append(update_done)

    if len(fields) == 0:
        return jsonify("Nothing to update")
    
    conn = get_db()
    c = conn.cursor()
    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ? AND user_id = ?"
    c.execute(sql, (*values, id, user_id))
    conn.commit()
    conn.close()

    return jsonify("Task updated succesfully!")