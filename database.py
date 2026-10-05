import sqlite3


def create_database():
    connection = sqlite3.connect("tickets.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            problem TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            sentiment TEXT,
            status TEXT DEFAULT 'Open',
            suggested_response TEXT
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")