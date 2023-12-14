import sqlite3 as sq

db = sq.connect('tg_shop.db')
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS accounts 
(id INTEGER PRIMARY KEY AUTOINCREMENT, 
tg_id INTEGER,
cart_id TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS items
(i_id INTEGER PRIMARY KEY AUTOINCREMENT,
photo TEXT,
name TEXT,
desc TEXT,
price TEXT,
type TEXT)""")

db.commit()

db = sq.connect('tg_shop.db')
cur = db.cursor()

users = cur.execute("SELECT tg_id FROM accounts").fetchall()
print(users)

for user in users:
    print(list(user))
    print(user[0])