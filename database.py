import sqlite3


def create_connection():
    conn = sqlite3.connect('carseason.db')
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    # Создание таблицы для автомобилей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        price REAL NOT NULL,
        condition TEXT NOT NULL,
        body_style TEXT NOT NULL,
        image TEXT
    )
    ''')

    # Создание таблицы для клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        testimonial TEXT NOT NULL
    )
    ''')

    conn.commit()


def insert_car(conn, make, model, year, price, condition, body_style, image):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO cars (make, model, year, price, condition, body_style, image)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (make, model, year, price, condition, body_style, image))
    conn.commit()


def insert_client(conn, name, location, testimonial):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO clients (name, location, testimonial)
    VALUES (?, ?, ?)
    ''', (name, location, testimonial))
    conn.commit()


def main():
    conn = create_connection()
    create_tables(conn)

    # Пример вставки данных
    insert_car(conn, 'Toyota', 'Camry', 2020, 24000, 'New', 'Sedan', 'path/to/image.png')
    insert_client(conn, 'John Doe', 'New York', 'Great service!')

    conn.close()


if __name__ == '__main__':
    main()
