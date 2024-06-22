import sqlite3


def setup_database():
    conn = sqlite3.connect('../database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_ru TEXT NOT NULL,
            name_uz TEXT NOT NULL
        )
        ''')

    # Создание таблицы продуктов с поддержкой нескольких языков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_ru TEXT NOT NULL,
            name_uz TEXT NOT NULL,
            category_id INTEGER,
            ingredients_en VARCHAR(100) NOT NULL,
            ingredients_ru VARCHAR(100) NOT NULL,
            ingredients_uz VARCHAR(100) NOT NULL,
            price INTEGER,
            image VARCHAR(100) NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(50) NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        total_price DECIMAL(9,2) DEFAULT 0,
        total_amount INTEGER DEFAULT 0,
        in_order BOOL DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(id),
        create_date VARCHAR(20) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(id),
        product_id INTEGER REFERENCES products(id),
        product_name VARCHAR(15) NOT NULL,
        quantity INTEGER NOT NULL,
        total_coast DECIMAL(9, 2) NOT NULL,   
        UNIQUE(cart_id, product_id)     
    )
    ''')

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        full_name VARCHAR(50) NOT NULL,
        phone_number VARCHAR(14) NOT NULL,
        review TEXT NOT NULL   
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
