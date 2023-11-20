import numpy as np


class Pendulum:
    t0 = None
    y0 = None
    result_t = None
    result_alfa = None
    result_alfa_dot = None
    E = None

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

    def vector_function_right_parts(self, t: float, y: np.ndarray, U: float):
        """
        Рассчитывает правые части векторной функции для дифференциальных уравнений математического маятника.

        :param t: Время (секунды).
        :param y: NumPy массив, содержащий текущие значения угла (y[0]) и угловой скорости (y[1]) маятника.
        :param U: Управление маятника.

        :return: NumPy массив, содержащий правые части дифференциальных уравнений: [y[1], -g/l * sin(y[0]) + U],
        """
        alfa = y[0]
        alfa_dot = y[1]

        # Вычисление правых частей
        right_parts = np.array([alfa_dot, -self.g / self.l * np.sin(alfa) + U])
        return right_parts

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


class Control:
    U = 0
    list_U = []
    list_t = []
    list_alfa = []
    list_alfa_dot = []
    mean_glm = 0
    mean_angle = 0
    std_angle = None
    std_angle_dot = None
    time_work = None
    kf_alfa = None
    kf_beta = None

    def __init__(self, params: Pendulum, required_angle: float, std_glm: float = 0.01):
        """
            Инициализирует объект управления.
            Параметры:
                - params: объект Pendulum с параметрами маятника
                - required_angle: желаемый угол
                - std_glm: стандартное отклонение гауссового шума для парматеров маятника  (по умолчанию 0.01)
        """
        self.g_noise = params.g + np.random.normal(self.mean_glm, std_glm)
        self.l_noise = params.l + np.random.normal(self.mean_glm, std_glm)
        self.m_noise = params.m + np.random.normal(self.mean_glm, std_glm)
        self.required_angle = required_angle
        self.std_glm = std_glm

    def add_control_characteristics(self, time_work: float, kf_alfa: float, kf_beta: float,
                                    std_angle: float, std_angle_dot: float):
        """
            Устанавливает характеристики управления.
            Параметры:
                - time_work: время работы управления
                - kf_alfa: коэффициент для угловой ошибки
                - kf_beta: коэффициент для скорости угла
                - std_angle: стандартное отклонение для гауссового шума в угле
                - std_angle_dot: стандартное отклонение для гауссового шума в скорости угла
        """
        self.time_work = time_work
        self.kf_alfa = kf_alfa
        self.kf_beta = kf_beta
        self.std_angle = std_angle
        self.std_angle_dot = std_angle_dot
        self.__check_characteristics()

    def __check_characteristics(self):
        """
            Проверяет характеристики управления на корректность.
            Если характеристики некорректны, вызывает исключение.
        """
        if self.kf_beta < 0 or self.kf_alfa - self.g_noise / self.l_noise * np.sin(self.required_angle) > 0:
            raise Exception

    def get_control(self, alfa: float, alfa_dot: float, time_now: float):
        """
            Возвращает значение управления на основе текущих данных.

            Параметры:
                - alfa: текущий угол
                - alfa_dot: текущая скорость угла
                - time_now: текущее время

            Возвращает:
                - U: значение управления
        """
        alfa = alfa + np.random.normal(self.mean_angle, self.std_angle)
        alfa_dot = alfa_dot + np.random.normal(self.mean_angle, self.std_angle_dot)

        self.U = self.kf_alfa * (alfa - self.required_angle) - self.kf_beta * alfa_dot + \
                 self.g_noise / self.l_noise * np.sin(self.required_angle)

        self.list_U.append(self.U)
        self.list_t.append(time_now)
        self.list_alfa.append(alfa)
        self.list_alfa_dot.append(alfa_dot)

        return self.U