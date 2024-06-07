import sys
import sqlite3
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox,
                             QLineEdit, QLabel, QSpinBox, QFormLayout, QDialog, QDialogButtonBox,
                             QHBoxLayout, QListWidget)


# Основное окно приложения
class SpaceFarmersApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  # Инициализация пользовательского интерфейса

    # Метод для инициализации пользовательского интерфейса
    def initUI(self):
        self.setWindowTitle("Space Farmers")  # Установка заголовка окна

        # Создание основного макета
        self.main_layout = QVBoxLayout()

        # Кнопка для тестирования приложения
        self.test_btn = QPushButton('Тестировать работу приложения', self)
        self.test_btn.clicked.connect(self.show_test_options)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(self.test_btn)

        # Кнопка для расчета реального полета
        self.custom_btn = QPushButton('Рассчитать реальный полет', self)
        self.custom_btn.clicked.connect(self.show_custom_options)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(self.custom_btn)

        # Установка основного виджета и макета
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

    # Метод для показа опций тестирования
    def show_test_options(self):
        self.clear_layout(self.main_layout)  # Очистка текущего макета

        # Кнопка для очистки БД и генерации данных
        clear_db_btn = QPushButton('Очистка БД и генерация', self)
        clear_db_btn.clicked.connect(self.clear_and_generate)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(clear_db_btn)

        # Кнопка для старта тестирования
        start_test_btn = QPushButton('Старт тестирования', self)
        start_test_btn.clicked.connect(self.start_gui)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(start_test_btn)

    # Метод для показа опций реального полета
    def show_custom_options(self):
        self.clear_layout(self.main_layout)  # Очистка текущего макета

        # Кнопка для добавления полетного задания
        add_task_btn = QPushButton('Добавить полетное задание', self)
        add_task_btn.clicked.connect(self.add_flight_task_dialog)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(add_task_btn)

        # Кнопка для показа списка заданий
        show_tasks_btn = QPushButton('Показать список заданий', self)
        show_tasks_btn.clicked.connect(self.show_flight_tasks)  # Подключение события нажатия кнопки к методу
        self.main_layout.addWidget(show_tasks_btn)

    # Метод для очистки макета
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # Метод для очистки базы данных и генерации новых данных
    def clear_and_generate(self):
        self.clear_database()  # Очистка базы данных
        self.generate_flight_tasks()  # Генерация новых данных
        QMessageBox.information(self, "Очистка и генерация", "База данных очищена и новые задания сгенерированы")

    # Метод для очистки базы данных
    def clear_database(self):
        db_name = 'flight_tasks.db'
        try:
            conn = sqlite3.connect(db_name)  # Подключение к базе данных
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS flight_tasks")  # Удаление таблицы, если она существует
            cursor.execute("DROP TABLE IF EXISTS points")  # Удаление таблицы, если она существует
            cursor.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                points TEXT NOT NULL
            )
            """)  # Создание новой таблицы
            conn.commit()

            # Проверка наличия таблицы
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
            table_exists = cursor.fetchone()
            if not table_exists:
                raise sqlite3.Error("Таблица 'tasks' не была создана")

            conn.close()

            # Удаление файла JSON, если он существует
            if os.path.exists('all_flight_tasks.json'):
                os.remove('all_flight_tasks.json')
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка: {e}")

    # Метод для генерации новых полетных заданий
    def generate_flight_tasks(self):
        try:
            os.system('python CreateBD.py')  # Запуск скрипта для создания базы данных
            os.system('python FillInBD.py')  # Запуск скрипта для заполнения базы данных
            os.system('python ExtractionBD.py')  # Запуск скрипта для извлечения данных из базы данных
        except Exception as e:
            QMessageBox.critical(self, "Ошибка генерации", f"Ошибка: {e}")

    # Метод для показа диалога добавления нового полетного задания
    def add_flight_task_dialog(self):
        dialog = AddTaskDialog(self)  # Создание диалога добавления задания
        if dialog.exec_() == QDialog.Accepted:
            task_name, points = dialog.get_task_data()  # Получение данных задания из диалога
            self.add_flight_task(task_name, points)  # Добавление нового задания в базу данных

    # Метод для добавления нового полетного задания в базу данных
    def add_flight_task(self, task_name, points):
        db_name = 'custom_flight_tasks.db'
        formatted_points = str([{"SH": point['sh'], "distance": point['distance']} for point in points])
        print(formatted_points)
        try:
            conn = sqlite3.connect(db_name)  # Подключение к базе данных
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_name, points) VALUES (?, ?)",
                           (task_name, formatted_points))  # Вставка данных задания
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавление задания", "Полетное задание успешно добавлено")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка: {e}")

    # Метод для показа списка полетных заданий
    def show_flight_tasks(self):
        self.clear_layout(self.main_layout)  # Очистка текущего макета

        self.task_list = QListWidget(self)  # Создание виджета списка заданий
        self.load_flight_tasks()  # Загрузка заданий из базы данных
        self.main_layout.addWidget(self.task_list)

        self.task_list.itemClicked.connect(self.run_selected_task)  # Подключение события нажатия на задание к методу

    # Метод для загрузки полетных заданий из базы данных
    def load_flight_tasks(self):
        db_name = 'custom_flight_tasks.db'
        try:
            conn = sqlite3.connect(db_name)  # Подключение к базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT id, task_name FROM tasks")  # Запрос всех заданий
            tasks = cursor.fetchall()
            conn.close()
            for task in tasks:
                self.task_list.addItem(f"{task[0]}: {task[1]}")  # Добавление задания в список
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка: {e}")

    # Метод для запуска выбранного задания
    def run_selected_task(self, item):
        task_id = item.text().split(":")[0]  # Получение ID задания из текста элемента списка
        db_name = 'custom_flight_tasks.db'
        try:
            conn = sqlite3.connect(db_name)  # Подключение к базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))  # Запрос задания по ID
            task = cursor.fetchone()
            print(task)
            conn.close()
            QMessageBox.information(self, "Запуск задания",
                                    f"Запуск задания: {task[1]}\nДанные: {task[2]}")  # Информация о запуске задания
            self.start_real_gui(task[2])  # Запуск реального GUI с данными задания
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка: {e}")

    # Метод для запуска реального графического интерфейса
    def start_real_gui(self, points):
        print(points)
        with open('real_task.txt', 'w') as f:
            f.write(str(points))
        try:
            os.system('python GUI_space_farmers_real.py')  # Запуск скрипта реального GUI
        except Exception as e:
            QMessageBox.critical(self, "Ошибка запуска", f"Ошибка: {e}")

    # Метод для запуска тестового графического интерфейса
    def start_gui(self):
        try:
            os.system('python GUI_space_farmers.py')  # Запуск скрипта тестового GUI
        except Exception as e:
            QMessageBox.critical(self, "Ошибка запуска", f"Ошибка: {e}")


# Диалоговое окно для добавления нового полетного задания
class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Добавить полетное задание')  # Установка заголовка окна

        layout = QFormLayout(self)  # Основной макет

        self.task_name_input = QLineEdit(self)  # Поле ввода для названия задания
        layout.addRow('Название задания:', self.task_name_input)

        self.num_points_input = QSpinBox(self)  # Поле ввода для количества точек
        self.num_points_input.setMinimum(1)
        layout.addRow('Количество точек:', self.num_points_input)

        self.points_layout = QVBoxLayout()  # Макет для точек
        layout.addRow(self.points_layout)

        self.num_points_input.valueChanged.connect(
            self.update_points_inputs)  # Подключение события изменения значения количества точек

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)  # Кнопки ОК и Отмена
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.update_points_inputs()  # Обновление макета точек

    # Метод для обновления полей ввода точек в зависимости от их количества
    def update_points_inputs(self):
        while self.points_layout.count():
            item = self.points_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.sh_inputs = []
        self.distance_inputs = []

        for i in range(self.num_points_input.value()):
            sh_input = QLineEdit(self)
            self.sh_inputs.append(sh_input)

            distance_input = QLineEdit(self)
            self.distance_inputs.append(distance_input)

            point_layout = QHBoxLayout()  # Макет для отдельной точки
            point_layout.addWidget(QLabel(f'Точка {i + 1} - SH:'))
            point_layout.addWidget(sh_input)
            point_layout.addWidget(QLabel('Расстояние:'))
            point_layout.addWidget(distance_input)

            self.points_layout.addLayout(point_layout)

    # Метод для получения данных задания из полей ввода
    def get_task_data(self):
        task_name = self.task_name_input.text()
        points = [{'sh': int(sh.text()), 'distance': int(distance.text())} for sh, distance in
                  zip(self.sh_inputs, self.distance_inputs)]
        return task_name, points


# Основной блок кода для запуска приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpaceFarmersApp()
    ex.show()
    sys.exit(app.exec_())  # Запуск основного цикла приложения
