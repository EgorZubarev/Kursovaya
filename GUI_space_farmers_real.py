import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
import json
from peremain import calc_function
from plot_sh_vs_days_gui import graph_SH_vs_days

with open('real_task.txt', 'r') as f:
    points = eval(f.read())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Космические фермеры")
        self.setGeometry(100, 100, 800, 600)

        # Создаем виджеты для ввода номера миссии и отображения результатов
        self.label = QLabel("Выберите номер миссии:")
        self.label.setFont(QFont("Arial", 14))

        self.mission_input = QLineEdit()
        self.mission_input.setFont(QFont("Arial", 12))

        self.start_button = QPushButton("Начать миссию")
        self.start_button.setFont(QFont("Arial", 12))
        self.start_button.clicked.connect(self.start_mission)

        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Courier New", 10))

        # Создаем layout и добавляем виджеты
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.mission_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.output_text)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_mission(self, points):
        days_graph = []
        results, point_results = calc_function(points)

        # Формируем строку с результатами миссии
        result_output = "Результаты миссии:\n\n"
        for day_result in results:
            result_output += f"День {day_result['day']}:\n"
            result_output += f"Популяция SH: {day_result['current_sh_population']:.2f}\n"
            result_output += f"Использованная мощность: {day_result['total_used_power']}\n"
            result_output += f"Использованный кислород: {day_result['total_used_oxygen']}\n"
            result_output += f"Распределение мощности (двигатель/автоклав): {day_result['engine_power']}/{day_result['autoclave_power']}\n\n"
            days_graph.append([day_result['day'], day_result['current_sh_population']])
        result_output += "Расход ресурсов по точкам:\n\n"

        for point_result in point_results:
            result_output += f"Точка {point_result['point_index']}: День {point_result['day']}, Мощность {point_result['total_used_power']}, Кислород {point_result['total_used_oxygen']}\n"

        # Отображаем результаты в текстовом поле
        self.output_text.setText(result_output)
        graph_SH_vs_days(days_graph)
        return days_graph


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start_mission(points)
    sys.exit(app.exec_())


# Сделать графики количества/расхода в бд