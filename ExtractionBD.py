import sqlite3
import json

# Подключение к базе данных
conn = sqlite3.connect('flight_tasks.db')
cursor = conn.cursor()

# Извлечение всех полетных заданий
cursor.execute('SELECT id, task_name FROM flight_tasks')
flight_tasks = cursor.fetchall()

# Создаем словарь для хранения всех полетных заданий
all_tasks_data = {}

# Извлечение точек для каждого полетного задания
for task in flight_tasks:
    task_id, task_name = task
    cursor.execute('''
    SELECT distance, SH FROM points WHERE task_id = ?
    ''', (task_id,))
    points_data = cursor.fetchall()

    # Формирование структуры данных для текущего полетного задания
    task_data = {
        "points": [{"distance": point[0], "SH": point[1]} for point in points_data]
    }

    # Добавляем текущее полетное задание в общий словарь
    all_tasks_data[task_id] = task_data


# Закрытие соединения с базой данных
conn.close()

# Преобразование структуры данных в строку JSON
json_data = json.dumps(all_tasks_data, ensure_ascii=False, indent=4)

# Сохранение JSON данных в файл
with open('all_flight_tasks.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

# Вывод JSON данных
print(json_data)
