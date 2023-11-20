import numpy as np
import ctypes
import os
from datetime import datetime, timedelta
import ephem


class Gravity:
    def __init__(self, start_datetime: datetime, N_harmonics: int = 10, model: str = 'egm2008'):

        lib = ctypes.CDLL(f"{os.path.dirname(os.path.abspath(__file__))}/Gravity/build/libgravity_ITRF.dylib")

        # Определение типа аргумента и возвращаемого значения функции
        lib.gravityVector_ITRF.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double,
                                           ctypes.c_int, ctypes.c_char_p]
        lib.gravityVector_ITRF.restype = ctypes.POINTER(ctypes.c_double)

        # Определение типа аргумента функции освобождения памяти
        lib.freeArrayMemory.argtypes = [ctypes.POINTER(ctypes.c_double)]

        self.lib = lib
        self.N_harmonics = N_harmonics
        self.model = model
        self.start_datetime = start_datetime

    def get_vector(self, xyz_ITRF_np: np.ndarray, t: float):
        # Текущее время шага
        current_datetime = self.start_datetime + timedelta(seconds=t)
        # Преобразование в юлианские дни
        current_datetime_jd = ephem.julian_date(current_datetime)

        # Получение указателя на данные массива NumPy
        xyz_ITRF_ptr = xyz_ITRF_np.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        # Вызов функции из библиотеки
        result_ptr = self.lib.gravityVector_ITRF(
            xyz_ITRF_ptr, current_datetime_jd, self.N_harmonics, self.model.encode('utf-8'))

        # Преобразование указателя на результат в массив NumPy
        result_np = np.ctypeslib.as_array(result_ptr, shape=(3,))

        right_parts = np.zeros(6)
        right_parts[3:6] = result_np

        # Освобождение памяти, выделенной под массив
        self.lib.freeArrayMemory(result_ptr)

        return right_parts


class Orbit:
    t0 = 0
    y0 = None
    result_t = None
    result_x = result_y = result_z = result_dotx = result_doty = result_dotz = None
    result_a = result_e = result_i = result_w = result_omega = result_nu = None

    def __init__(self, a: float, e: float, i: float, w: float, omega: float, nu: float,
                 mu: float, start_datetime: datetime):
        """
        Конструктор класса, который инициализирует объект орбиты с заданными параметрами.

            :param a: Большая полуось.
            :param e: Эксцентриситет.
            :param i: Наклонение.
            :param w: Аргумент перицентра.
            :param omega: Долгота восходящего узла.
            :param nu: Истиная аномалия.
            :param mu: Гравитационный параметр.
            :param start_datetime: Дата и время начальных параметров.

        """
        self.a = a  # Большая полуось
        self.e = e  # Эксцентриситет
        self.i = i  # Наклонение
        self.w = w  # Аргумент перицентра
        self.omega = omega  # Долгота восходящего узла
        self.nu = nu  # Истиная аномалия
        self.mu = mu  # Гравитационный параметр
        self.gravity = Gravity(start_datetime=start_datetime)  # Класс Гравитация для модели сложного поля

        # добавляем начальные данные
        self.y0 = self.from_elements_to_xyz(a=a, e=e, i=i, w=w, omega=omega, nu=nu)

    def vector_function_right_parts(self, t: float, y: np.ndarray):
        """
        Рассчитывает правые части векторной функции для задачи двух тел

            :param t: Время (секунды).
            :param y: NumPy массив, содержащий текущие значения вектора r (y[0:3]) и вектора v (y[3:6]).

        :return: NumPy массив, содержащий правые части дифференциальных уравнений задачи двух тел
        """
        right_parts = self.gravity.get_vector(y[0:3], t=t)
        right_parts[0:3] = y[3:6]
        return right_parts

    def from_elements_to_xyz(self, a: float, e: float, i: float, w: float, omega: float, nu: float):
        """
        Рассчитывает вектор состояния в декартовой системе координат по орбитальным элементам.

            :param a: Большая полуось.
            :param e: Эксцентриситет.
            :param i: Наклонение.
            :param w: Аргумент перицентра.
            :param omega: Долгота восходящего узла.
            :param nu: Истиная аномалия.

            :return: Вектор состояния в декартовой системе координат.
        """
        # эксцентрическая аномалия
        E = 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(nu / 2))
        # малая полуось
        b = a * np.sqrt(1 - e ** 2)

        # вектор состояния в орбитальной системе коррдинат ξηζ
        orbit_coords = np.array([a * (np.cos(E) - e),
                                 b * np.sin(E),
                                 0,
                                 np.sqrt(self.mu / (a * (1 - e ** 2))) * -np.sin(nu),
                                 np.sqrt(self.mu / (a * (1 - e ** 2))) * (np.cos(nu) + e),
                                 0
                                 ])

        # Вычисление коэффициентов b в матрице A
        b11 = np.cos(omega) * np.cos(w) - np.sin(omega) * np.sin(w) * np.cos(i)
        b12 = -np.cos(omega) * np.sin(w) - np.sin(omega) * np.cos(w) * np.cos(i)
        b13 = np.sin(omega) * np.sin(i)

        b21 = np.sin(omega) * np.cos(w) + np.cos(omega) * np.sin(w) * np.cos(i)
        b22 = -np.sin(omega) * np.sin(w) + np.cos(omega) * np.cos(w) * np.cos(i)
        b23 = -np.cos(omega) * np.sin(i)

        b31 = np.sin(w) * np.sin(i)
        b32 = np.cos(w) * np.sin(i)
        b33 = np.cos(i)

        A = np.array([
            [b11, b12, b13],
            [b21, b22, b33],
            [b31, b32, b33]
        ])

        # переводит в декртовые координаты и возвращаем их
        xyz_coords = np.append(A @ orbit_coords[0:3], A @ orbit_coords[3:])
        return xyz_coords

    def from_xyz_to_elements(self, xyz_coords: np.ndarray):
        """
        Рассчитывает орбитальные элементы по декартовым координатам.

            :param xyz_coords: NumPy массив, содержащий вектор состояния в декартовых координатах.

            :return: NumPy массив с орбитальными элементами (a, e, i, w, omega, nu).
        """
        r = xyz_coords[0:3]
        v = xyz_coords[3:]

        # базисные векторы в декартовых координатах
        Ox = np.array([1, 0, 0])
        Oy = np.array([0, 1, 0])
        Oz = np.array([0, 0, 1])

        # первые интегралы
        c = np.cross(r, v)
        f = np.cross(v, c) - self.mu * r / np.linalg.norm(r)

        # находим еще два новых базисных вектора в дополнении к с
        l = np.cross(Oz, c) / np.linalg.norm(np.cross(Oz, c))
        m = np.cross(c, l) / np.linalg.norm(np.cross(c, l))

        # находим элементы орбиты
        i = np.arccos(np.dot(c, Oz) / np.linalg.norm(c))
        omega = np.arctan2(np.dot(l, Oy), np.dot(l, Ox))
        w = np.arctan2(np.dot(f, m), np.dot(f, l))
        nu = np.arctan2(np.dot(r, m), np.dot(r, l)) - w
        if nu < 0:
            nu += 2 * np.pi  # Добавляем 2π радиан
        e = np.linalg.norm(f) / self.mu
        a = np.dot(c, c) / (self.mu * (1 - e ** 2))

        return np.array([a, e, i, w, omega, nu])

    def add_results(self, t: np.ndarray, y: np.ndarray):
        """
        Добавляет результаты расчетов.
        """
        self.result_t = t

        # Разделите координаты на компоненты x, y и z и так далее
        self.result_x, self.result_y, self.result_z, self.result_dotx, self.result_doty, self.result_dotz = y.T

        # Получим элементы орбиты в каждый момент времени
        self.result_a, self.result_e, self.result_i, self.result_w, self.result_omega, self.result_nu = \
            np.array(list(map(self.from_xyz_to_elements, y))).T
