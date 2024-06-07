from math import sin, pi


def calc_function(points):
    day_result = []  # Список для хранения данных по каждому дню полета
    point_result = []  # Список для хранения данных по каждой точке назначения
    day = 1  # Текущий день
    starship_weight = 192  # Базовый вес звездолета
    used_oxygen = 0  # Использованный кислород
    used_power = 0  # Использованная мощность реактора в процентах
    point_index = 1  # Индекс текущей точки назначения

    for point in points:
        current_sh_population = 8  # Текущее количество SH
        distance_to_point = point["distance"]  # Расстояние до текущей точки
        required_sh = point["SH"]  # Требуемое количество SH для разгрузки
        suitable_power = True

        # Полет к текущей точке
        while suitable_power:
            for reactor_power in range(80, 0, -1):  # Итерация мощности реактора от 80 до 0
                speed = 2 * (reactor_power / 80) * (200 / (starship_weight + current_sh_population))  # Рассчет скорости
                if distance_to_point - speed > 0:  # Если после полета остается расстояние
                    distance_to_point -= speed  # Обновление оставшегося расстояния
                    used_oxygen += current_sh_population * 2  # Использование кислорода
                    used_power += reactor_power  # Увеличение использованной мощности реактора
                    day += 1  # Увеличение количества дней
                    used_power += 20  # Увеличение использованной мощности реактора на 20% (для обслуживания автоклава)
                    day_result.append({
                        'day': day,
                        'current_sh_population': int(current_sh_population),
                        'total_used_power': used_power,
                        'total_used_oxygen': int(used_oxygen + 1),
                        'reactor_power_usage': 20 + reactor_power,
                        'oxygen_usage': current_sh_population * 2,
                        'engine_power': reactor_power,
                        'autoclave_power': 20
                    })  # Добавление данных дня
                    if reactor_power != 80:
                        suitable_power = False  # Если мощность не 80%, выход из цикла
                    break
            else:
                suitable_power = False  # Если мощность 80% не подходит, выход из цикла

        # Увеличение популяции SH
        suitable_power = True
        while suitable_power:
            for oxygen_per_sh in range(20, 0, -1):  # Итерация кислорода на единицу SH от 20 до 0
                growth_factor = sin(
                    -pi / 2 + (pi * (30 + 0.5 * oxygen_per_sh) / 40))  # Рассчет коэффициента роста популяции SH
                if current_sh_population + current_sh_population * growth_factor <= required_sh + 8:  # Если новая популяция <= требуемой + 8
                    used_oxygen += current_sh_population * oxygen_per_sh  # Использование кислорода
                    current_sh_population += current_sh_population * growth_factor  # Обновление популяции SH
                    day += 1  # Увеличение количества дней
                    used_power += 43  # Увеличение использованной мощности реактора на 43% (для автоклава)
                    day_result.append({
                        'day': day,
                        'current_sh_population': int(current_sh_population),
                        'total_used_power': used_power,
                        'total_used_oxygen': int(used_oxygen + 1),
                        'reactor_power_usage': 43,
                        'oxygen_usage': current_sh_population * oxygen_per_sh,
                        'engine_power': 0,
                        'autoclave_power': 43
                    })  # Добавление данных дня
                    if oxygen_per_sh != 20:
                        suitable_power = False  # Если кислород на единицу SH не 20, выход из цикла
                    break
                else:
                    suitable_power = False  # Если новая популяция > требуемой + 8, выход из цикла


        # Полет к следующей точке
        suitable_power = True
        while suitable_power:
            for reactor_power in range(1, 81):  # Итерация мощности реактора от 1 до 80
                speed = 2 * (reactor_power / 80) * (200 / (starship_weight + current_sh_population))  # Рассчет скорости
                if distance_to_point - speed < 0:  # Если после полета остается расстояние
                    distance_to_point -= speed  # Обновление оставшегося расстояния
                    used_oxygen += current_sh_population * 2  # Использование кислорода
                    used_power += reactor_power  # Увеличение использованной мощности реактора
                    day += 1  # Увеличение количества дней
                    used_power += 20  # Увеличение использованной мощности реактора на 20% (для обслуживания автоклава)
                    day_result.append({
                        'day': day,
                        'current_sh_population': int(current_sh_population),
                        'total_used_power': used_power,
                        'total_used_oxygen': int(used_oxygen + 1),
                        'reactor_power_usage': reactor_power + 20,
                        'oxygen_usage': current_sh_population * 2,
                        'engine_power': reactor_power,
                        'autoclave_power': 20
                    })  # Добавление данных дня
                    suitable_power = False  # Выход из цикла
                    break
            else:
                reactor_power = 80  # Если мощность 80% не подходит, использовать её
                speed = 2 * (reactor_power / 80) * (200 / (starship_weight + current_sh_population))  # Рассчет скорости
                distance_to_point -= speed  # Обновление оставшегося расстояния
                used_oxygen += current_sh_population * 2  # Использование кислорода
                used_oxygen = int(used_oxygen + 1)
                used_power += reactor_power  # Увеличение использованной мощности реактора
                day += 1  # Увеличение количества дней
                used_power += 20  # Увеличение использованной мощности реактора на 20% (для обслуживания автоклава)

        # Добавление данных точки назначения
        point_result.append({
            'point_index': point_index,
            'day': day,
            'total_used_power': used_power,
            'total_used_oxygen': int(used_oxygen + 1)
        })
        point_index += 1  # Увеличение индекса точки назначения

    return day_result, point_result
