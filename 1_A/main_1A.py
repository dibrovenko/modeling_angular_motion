import numpy as np
from matplotlib import pyplot as plt

from grafics import plot_subplot
from rkk4 import runge_kutta_4


class Pendulum:
    E = None  # calculate_energy
    result_t = None  # add_results
    result_alfa = None  # add_results
    result_alfa_dot = None  # add_results
    t0 = None  # add_initial_data
    y0 = None  # add_initial_data

    def __init__(self, g, l, m):
        """
        Инициализирует объект класса Pendulum.

        :param g: Ускорение свободного падения (м/с^2).
        :param l: Длина маятника (метры).
        :param m: Масса маятника (килограммы).
        """
        self.g = g
        self.l = l
        self.m = m

    def add_initial_data(self, t0: float, y0: np.ndarray):
        """
        Добавляет начальные данные для математического маятника.

        :param t0: Время начальных данных (секунды).
        :param y0: Начальные значения угла и угловой скорости в виде NumPy массива.
        """
        self.y0 = y0
        self.t0 = t0

    def add_results(self, result_t: np.ndarray, result_alfa: np.ndarray, result_alfa_dot: np.ndarray):
        """
        Добавляет результаты расчетов.

        :param result_t: Временной массив результатов (секунды).
        :param result_alfa: Угловые значения результатов в радианах в виде NumPy массива.
        :param result_alfa_dot: Угловые скорости в радианах/секунду в виде NumPy массива.
        """
        self.result_t = result_t
        self.result_alfa = result_alfa
        self.result_alfa_dot = result_alfa_dot

    def calculate_energy(self):
        """
        Рассчитывает полную энергию математического маятника.
        """
        self.E = 0.5 * self.m * self.l ** 2 * self.result_alfa_dot ** 2 + \
            self.m * self.g * self.l * (1 - np.cos(self.result_alfa))
        print(self.E[0])

        self.E = self.E - self.E[0]

def vector_function_right_parts(t: float, y: np.ndarray, params: Pendulum):
    """
    Рассчитывает правые части векторной функции для дифференциальных уравнений математического маятника.

    :param t: Время (секунды).
    :param y: NumPy массив, содержащий текущие значения угла (y[0]) и угловой скорости (y[1]) маятника.
    :param params: Объект класса Pendulum, содержащий параметры маятника.

    :return: NumPy массив, содержащий правые части дифференциальных уравнений: [y[1], -g/l * sin(y[0])],
    """
    alfa = y[0]
    alfa_dot = y[1]
    g = params.g
    l = params.l

    # Вычисление правых частей
    right_parts = np.array([alfa_dot, -g / l * np.sin(alfa)])

    return right_parts


# Начальные данные
t0 = 0.0
alfa0 = 0.2  # начальный угол
alfa_dot0 = 2  # начальная угловая скорость
pendulum = Pendulum(g=9.8, l=1.0, m=1.0)
pendulum.add_initial_data(t0=t0, y0=np.array([alfa0, alfa_dot0]))

h = 0.0001  # Шаг интегрирования
n = 100000  # Количество шагов

# Вызов метода Рунге-Кутта 4-го порядка
result_runge_kutta_4 = runge_kutta_4(
    f=vector_function_right_parts, t0=pendulum.t0, y0=pendulum.y0, h=h, n=n, params=pendulum)

pendulum.add_results(result_t=result_runge_kutta_4[0],
                     result_alfa=result_runge_kutta_4[1][:, 0],
                     result_alfa_dot=result_runge_kutta_4[1][:, 1])

#Считаем первый интеграл
pendulum.calculate_energy()
print(f"Разница между max и min значением первого интеграла: {max(pendulum.E) - min(pendulum.E)}")

# Создаем графики
plt.figure(figsize=(10.5, 7))
plot_subplot(221, pendulum.result_t, pendulum.result_alfa, 'Угол от времени', 't, c', 'alfa, рад')
plot_subplot(222, pendulum.result_t, pendulum.result_alfa_dot, 'Угловая скорость от времени', 't, c', 'alfa_dot рад/с')
plot_subplot(223, pendulum.result_alfa, pendulum.result_alfa_dot, 'Фазовая картина движения', 'alfa, рад', 'alfa_dot рад/с')
plot_subplot(224, pendulum.result_t, pendulum.E, 'Первый интреграл от времени', 'E, Дж', 't, c')

plt.tight_layout()
plt.show()
