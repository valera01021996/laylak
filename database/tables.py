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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()