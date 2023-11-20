from matplotlib import pyplot as plt
import numpy as np

from classes import Orbit
from graffics_plotly import orbit_plot_plotly


def orbit_plot(orbit: Orbit):
    # Создаем фигуру и 3D-подграфик
    r_apofocus = 1.05 * orbit.result_a[0] * (1 + orbit.result_e[0])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Создаем сферу, представляющую Землю
    r = 6371 * 1000  # Радиус Земли примерно 6371 км
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))

    # Отображаем сферу
    earth = ax.plot_surface(x, y, z, color='b', alpha=0.3, label='Земля')

    # Добавляем нулевой меридиан
    zero_meridian = np.array([r * np.cos(u), np.zeros(100), r * np.sin(u)])
    ax.plot(zero_meridian[0], zero_meridian[1], zero_meridian[2], color='b', linewidth=1, label='Нулевой меридиан')

    # Добавляем плоскость экватора
    xx, yy = np.meshgrid(np.linspace(-r_apofocus, r_apofocus, 10), np.linspace(-r_apofocus, r_apofocus, 10))
    zz = np.zeros(xx.shape)
    plane = ax.plot_surface(xx, yy, zz, color='g', alpha=0.5, label='Плоскость экватора')

    # Добавляем орбиту
    ax.plot(orbit.result_x, orbit.result_y, orbit.result_z, color='r', linewidth=2, label='Орбита спутника')

    # Добавляем точку старта
    ax.scatter(orbit.result_x[0], orbit.result_y[0], orbit.result_z[0], color='k', s=10, label='Точка старта')

    # Метки осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Масштабируйте оси
    ax.set_xlim(-r_apofocus, r_apofocus)
    ax.set_ylim(-r_apofocus, r_apofocus)
    ax.set_zlim(-r_apofocus, r_apofocus)

    # Отобразите график
    ax.legend()
    plt.tight_layout()
    plt.show()


# Функция для построения графика
def plot_subplot(subplot_num, data_x, data_y, title, x_label, y_label):
    plt.subplot(subplot_num)
    plt.plot(data_x, data_y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def save_and_close_plot(figure, filename):
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(figure)


def start_plot(orbit: Orbit):
    # Графики орбитальных элементов
    fig_elements = plt.figure(figsize=(10.5, 7))
    plot_subplot(321, orbit.result_t, orbit.result_a, 'Большая полуось', 't, c', 'a')
    plot_subplot(322, orbit.result_t, orbit.result_e, 'Эксцентриситет', 't, c', 'e')
    plot_subplot(323, orbit.result_t, orbit.result_i, 'Наклонение', 't, c', 'i')
    plot_subplot(324, orbit.result_t, orbit.result_omega, 'Долгота восходящего узла ', 't, c', 'Ω')
    plot_subplot(325, orbit.result_t, orbit.result_w, 'Аргумент перицентра', 't, c', 'w')
    plot_subplot(326, orbit.result_t, orbit.result_nu, 'Истинная аномалия', 't, c', ' ν')
    save_and_close_plot(fig_elements, 'result/days_14/result_elements.png')

    # Cтроим орбиту
    orbit_plot_plotly(orbit=orbit)  # для моделирования дольше чем день или больше чем 12 оборотов
    #orbit_plot(orbit=orbit)  # для модели меньше дня

