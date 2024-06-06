import sqlite3
import random


# Функция для генерации значения SH
def generate_sh():
    n = random.randint(0, 10)
    if random.random() < 0.5:
        return random.randint(1, 7)  # Значения в интервале [1, 8)
    else:
        return 8 * (2 ** n) - 8  # Значения по формуле 8 * 2^n - 8


# Подключение к базе данных
conn = sqlite3.connect('flight_tasks.db')
cursor = conn.cursor()

# Вставляем примерные данные для полетных заданий
for i in range(1, 11):
    cursor.execute('INSERT INTO flight_tasks (task_name) VALUES (?)', (f'Flight Task {i}',))
    task_id = cursor.lastrowid

    # Вставляем до 1001 точки для каждого полетного задания
    for j in range(1001):
        distance = random.randint(10, 50)
        sh = generate_sh()
        cursor.execute('INSERT INTO points (task_id, distance, SH) VALUES (?, ?, ?)', (task_id, distance, sh))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
