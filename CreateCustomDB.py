import sqlite3

def create_custom_db(db_name='custom_flight_tasks.db'):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Создание таблицы tasks
        cursor.execute("DROP TABLE IF EXISTS tasks")
        cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            points TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
        print(f"Database {db_name} created successfully with table 'tasks'.")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_custom_db()
