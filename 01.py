import sqlite3

conn = sqlite3.connect("01.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("INSERT INTO users (name) VALUES ('Гэндальф')")
cursor.execute("INSERT INTO users (name) VALUES ('Гимли')")
cursor.execute("INSERT INTO users (name) VALUES ('Леголас')")

conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()