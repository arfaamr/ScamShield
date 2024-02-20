import sqlite3

connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO scams (title, content) VALUES (?, ?)",
    ("scams@scams.com", ""),
)

cur.execute(
    "INSERT INTO scams (title, content) VALUES (?, ?)",
    ("phishing@fraud.com", ""),
)

cur.execute(
    "INSERT INTO scams (title, content) VALUES (?, ?)",
    ("phish@yahoo.com", ""),
)

cur.execute(
    "INSERT INTO scams (title, content) VALUES (?, ?)",
    ("spam@gmail.com", ""),
)

connection.commit()
connection.close()
