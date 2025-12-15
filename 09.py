import sqlite3
import csv

conn = sqlite3.connect("01.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

conn.close()

with open("09.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    
    writer.writerow(["id", "name"])
    
    for row in rows:
        writer.writerow(row)

print("Экспорт завершён. Файл 09.csv создан.")
