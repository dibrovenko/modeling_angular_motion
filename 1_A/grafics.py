from matplotlib import pyplot as plt


# Функция для построения графика
def plot_subplot(subplot_num, data_x, data_y, title, x_label, y_label):
    plt.subplot(subplot_num)
    plt.plot(data_x, data_y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)