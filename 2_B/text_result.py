from prettytable import PrettyTable
import numpy as np

from classes import Orbit


def write_result(orbit: Orbit, where_save: str):
    # Находим индексы, где значение становится меньше предыдущего
    end_of_circle_indices = np.where(orbit.result_nu < np.roll(orbit.result_nu, 1))[0]

    # Создание первой таблицы
    table1 = PrettyTable()
    table1.field_names = ["Номер витка", "ДВУ", "Аргумент перицентра", "Большая полуось", "Эксцентриситет",
                          "Наклонение", "Истинная аномалия"]
    count = 0  # счетчик
    for i in end_of_circle_indices:
        count += 1
        table1.add_row([count, orbit.result_omega[i],  orbit.result_w[i], orbit.result_a[i], orbit.result_e[i],
                        orbit.result_i[i], orbit.result_nu[i]])

    # Создание второй таблицы
    table2 = PrettyTable()
    table2.field_names = ["ДВУ", "Аргумент перицентра", "Большая полуось", "Эксцентриситет", "Наклонение"]
    table2.add_row([orbit.result_omega[end_of_circle_indices[-1]] - orbit.result_omega[end_of_circle_indices[0]],
                    orbit.result_w[end_of_circle_indices[-1]] - orbit.result_w[end_of_circle_indices[0]],
                    orbit.result_a[end_of_circle_indices[-1]] - orbit.result_a[end_of_circle_indices[0]],
                    orbit.result_e[end_of_circle_indices[-1]] - orbit.result_e[end_of_circle_indices[0]],
                    orbit.result_i[end_of_circle_indices[-1]] - orbit.result_i[end_of_circle_indices[0]] ])

    # Создание третий таблицы
    th_delta_omega, th_delta_w = (count - 1) * np.array(orbit.theoretical_calculations_of_orbit_change())
    table3 = PrettyTable()
    table3.field_names = ["ДВУ", "Аргумент перицентра"]
    table3.add_row([th_delta_omega, th_delta_w])

    # Сохранение таблиц в текстовый файл
    with open(f"result/{where_save}output.txt", "w") as file:
        file.write(f"\nИзменение параметров за {count-1} витков:\n")
        file.write(str(table2))
        file.write(f"\nИзменение параметров за {count-1} витков теоретически:\n")
        file.write(str(table3))
        file.write("\n\n\n\nПараметры орбиты в начале каждого витка:\n")
        file.write(str(table1))


