import sqlite3

conn = sqlite3.connect("06.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

names = ["Гэндальф", "Гимли", "Леголас", "Саурон", "Саруман"]

for name in names:
    cursor.execute(
        "INSERT INTO users (name) VALUES (?)",
        (name,)
    )

conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()