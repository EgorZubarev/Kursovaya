import matplotlib.pyplot as plt


def graph_SH_vs_days(data):
    # Извлечение переменных из списка
    x_values = [item[0] for item in data]
    y_values = [item[1] for item in data]

    # Построение графика
    plt.plot(x_values, y_values, marker='o')

    # Добавление заголовка и меток осей
    plt.title('График зависимости количества SH от дня полета')
    plt.xlabel('День')
    plt.ylabel('SH')

    # Отображение графика
    plt.grid(True)
    plt.show()
