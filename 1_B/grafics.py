from matplotlib import pyplot as plt
import numpy as np


# Функция для построения графика
def plot_subplot(subplot_num: int, data_x: np.ndarray, data_y: np.ndarray, title: str, x_label: str, y_label: str,
                 scatter: list = None, axhline: float = None):
    plt.subplot(subplot_num)
    plt.plot(data_x, data_y, label='real')

    if scatter is not None:
        # Создаем точечный график
        plt.scatter(scatter[0], scatter[1], color='green', s=2, marker='o', label='measured')
    if axhline is not None:
        # Создаем горизонтальную прямую линию
        plt.axhline(y=axhline, color='red', linestyle='--', label='required', alpha=0.5)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()