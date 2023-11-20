import math
import numpy as np
from datetime import datetime

from classes import Orbit
from rkk4 import runge_kutta_4
from grafics import start_plot
from text_result import write_result

import time
# Засекаем время перед выполнением кода
start_time = time.time()

a = 8059 * 1000    # Большая полуось
e = 0.15  # Эксцентриситет
i = 1.2  # Наклонение
omega = 0.7  # Долгота восходящего узла
w = 1.37  # Аргумент перицентра
nu = 0.0  # Истиная аномалия
mu = 3.986004418 * 10 ** 14  # Гравитационный параметр
start_datetime = datetime(2023, 11, 14, 19, 00)  # Заданные дата и время начала моделирования
orbit = Orbit(a=a, e=e, i=i, omega=omega, w=w, nu=nu, mu=mu, start_datetime=start_datetime)

# Вызов метода Рунге-Кутта 4-го порядка
T = 2 * np.pi * a ** 1.5 / mu ** 0.5  # Период обращения
end_datetime = datetime(2023, 11, 28, 22, 00)  # Заданные дата и время конца моделирования
h = 0.2  # Шаг интегрирования по времени
n = math.ceil((end_datetime - start_datetime).total_seconds() / h)  # Количество шагов

runge_kutta_4(f=orbit.vector_function_right_parts, t0=orbit.t0, y0=orbit.y0, h=h, n=n, orbit=orbit)

# строим графики
start_plot(orbit=orbit)

# покажим различия с теорет моделью
write_result(orbit=orbit)

# Вычисляем время выполнения
execution_time = time.time() - start_time
print(f"Execution time: {execution_time} seconds")
# 910 секунд для 2 недели
