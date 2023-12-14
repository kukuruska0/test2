import sqlite3 as sq


async def db_start():
    db = sq.connect('tg_shop.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS accounts 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
     tg_id INTEGER,
     cart_id TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS items
    (photo TEXT,
    name TEXT,
    desc TEXT,
    price TEXT,
    type TEXT)""")

    db.commit()

    db.close()


async def cmd_start_db(user_id):
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key} ".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))

        db.commit()

    db.close()


async def add_item(state):
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (photo, name, desc, price, type) VALUES (?, ?, ?, ?, ?)",
                    (data['photo'], data['name'], data['desc'], data['price'], data['type']))
        db.commit()

    db.close()


async def db_delete(data):
    db = sq.connect('tg_shop.db')
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE name == ?", (data,))
    db.commit()
    db.close()

