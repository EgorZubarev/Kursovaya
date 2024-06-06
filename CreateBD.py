import sqlite3

# Создаем или подключаемся к базе данных
conn = sqlite3.connect('flight_tasks.db')
cursor = conn.cursor()

# Создаем таблицу для полетных заданий
cursor.execute('''
CREATE TABLE IF NOT EXISTS flight_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL
)
''')

# Создаем таблицу для точек
cursor.execute('''
CREATE TABLE IF NOT EXISTS points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    distance INTEGER,
    SH INTEGER,
    FOREIGN KEY (task_id) REFERENCES flight_tasks(id)
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
