import sqlite3

conn = sqlite3.connect("tasks.db")
c = conn.cursor()

# c.execute("""CREATE TABLE users (
#           user_id integer PRIMARY KEY AUTOINCREMENT,
#           username text UNIQUE,
#           password text
#           )""")

# c.execute("""CREATE TABLE tasks (
#           id integer PRIMARY KEY AUTOINCREMENT,
#           user_id integer,
#           title text,
#           description text,
#           done integer,
#           created_at text,
#           FOREIGN KEY (user_id)
#             REFERENCES users (user_id)
#           )""")

conn.commit()
conn.close()