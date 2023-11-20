import math
import numpy as np

from classes import Pendulum, Control


def runge_kutta_4(f, t0: float, y0: np.ndarray, h, n: int, control: Control, pendulum: Pendulum):
    """
    Метод Рунге-Кутта 4-го порядка для решения системы дифференциальных уравнений

    Аргументы:
    f: функция, описывающая систему дифференциальных уравнений
       Принимает аргументы t и y и возвращает массив значений производных dy/dx
    t0: начальное значение t
    y0: начальное значение y (массив значений)
    h: шаг интегрирования
    n: количество шагов
    control: класс управления
    pendulum: класс маятника
    """

    # Создаем массивы для хранения результатов
    t = np.zeros(n + 1)
    y = np.zeros((n + 1, len(y0)))

    # Записываем начальные значения
    t[0] = t0
    y[0] = y0

    # учитваем дискретность управления
    period_U = math.ceil(control.time_work / h)
    U = 0

    # Итерационный процесс метода Рунге-Кутта 4-го порядка
    for i in range(n):
        if i % period_U == 0:
            U = control.get_control(alfa=y[i][0], alfa_dot=y[i][1], time_now=t[i])

        k1 = f(t[i], y[i], U=U)
        k2 = f(t[i] + h / 2, y[i] + h / 2 * k1, U=U)
        k3 = f(t[i] + h / 2, y[i] + h / 2 * k2, U=U)
        k4 = f(t[i] + h, y[i] + h * k3, U=U)

        t[i + 1] = t[i] + h
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) * h / 6

    pendulum.add_results(result_t=t, result_alfa=y[:, 0], result_alfa_dot=y[:, 1])

