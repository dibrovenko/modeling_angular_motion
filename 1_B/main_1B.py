import numpy as np
from matplotlib import pyplot as plt

from classes import Pendulum, Control
from rkk4 import runge_kutta_4
from grafics import plot_subplot

# Начальные данные
t0 = 0.0
alfa0 = np.pi/3  # начальный угол
alfa_dot0 = -2  # начальная угловая скорость

pendulum = Pendulum(g=9.8, l=1.0, m=1.0)
pendulum.add_initial_data(t0=t0, y0=np.array([alfa0, alfa_dot0]))

# Данные об управлении
required_angle = np.pi/4
kf_alfa = -2  # кф управления альфа
kf_beta = 3  # кф управления бета
time_work_of_control = 0.1  # min время работы управления
std_angle = 0.01  # шум угла
std_angle_dot = 0.03  # шум угловой скорости

control = Control(params=pendulum, required_angle=required_angle)
control.add_control_characteristics(time_work=time_work_of_control, kf_alfa=kf_alfa, kf_beta=kf_beta,
                                    std_angle=std_angle, std_angle_dot=std_angle_dot)

# Вызов метода Рунге-Кутта 4-го порядка
h = 0.01  # Шаг интегрирования
n = 800  # Количество шагов

runge_kutta_4(f=pendulum.vector_function_right_parts, t0=pendulum.t0, y0=pendulum.y0,
              h=h, n=n, control=control, pendulum=pendulum)

# Создаем графики
plt.figure(figsize=(10.5, 7))
plot_subplot(221, pendulum.result_t, pendulum.result_alfa, 'Угол от времени', 't, c', 'alfa, рад',
             axhline=required_angle, scatter=[control.list_t, control.list_alfa])

plot_subplot(222, pendulum.result_t, pendulum.result_alfa_dot, 'Угловая скорость от времени', 't, c',
             'alfa_dot рад/с', axhline=0, scatter=[control.list_t, control.list_alfa_dot])

plot_subplot(223, pendulum.result_alfa, pendulum.result_alfa_dot, 'Фазовая картина движения', 'alfa, рад',
             'alfa_dot рад/с')
plot_subplot(224, control.list_t, control.list_U, 'Управление от времени', 't, c', 'U')

plt.tight_layout()
plt.show()

# Показываем конечные значения
print(f"требуемый угол: {required_angle}")
print(f"итоговый угол: {pendulum.result_alfa[-1]}, итоговая угловая скорость: {pendulum.result_alfa_dot[-1]}")


