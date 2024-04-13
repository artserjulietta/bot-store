import sqlite3

DATABASE = 'store.db'

class StoreManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            # Создание таблицы "товары"
            conn.execute('''CREATE TABLE IF NOT EXISTS items (
                                item_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                price INTEGER NOT NULL,
                                color TEXT,
                                img TEXT
                            )''')

            # Создание таблицы "корзина"
            conn.execute('''CREATE TABLE IF NOT EXISTS cart (
                                user_id INTEGER,
                                item_id INTEGER,
                                count INTEGER,
                                FOREIGN KEY(item_id) REFERENCES items(item_id)
                            )''')
            conn.commit()

    def add_items(self, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany("INSERT INTO items (name, price, color, img ) VALUES (?, ?, ?, ?)", data)
            conn.commit()

    def show_items(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM items ")
            res = cur.fetchall()
            return res 
        
    def add_item_to_cart(self, user_id, item_id): # метод для добавления товара в корзину
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM cart WHERE user_id = ? AND item_id = ?", (user_id, item_id))
            res = cur.fetchall()
            if res:
                cur.execute("UPDATE cart SET count = count + 1  WHERE user_id = ? AND item_id = ? ", (user_id, item_id))
            else:
                cur.execute("INSERT INTO cart VALUES (?, ?, ?)", (user_id, item_id, 1))
            conn.commit()

    def show_cart(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT item_id, count FROM cart WHERE user_id = ? ", (user_id,))
            res = cur.fetchall()
            return res
        
    def get_name_of_item(self, item_id): # метод для получения названия одежды по id из таблицы "одежда"
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM items WHERE item_id = ? ", (item_id,))
            res = cur.fetchall()
            return res
        
    def delete(self,user_id):

        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany("DELETE FROM cart WHERE user_id = ?", (user_id,))
            conn.commit()

      