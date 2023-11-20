#include <iostream>
#include <cmath>
#include <GeographicLib/GravityModel.hpp>


// Функция для освобождения памяти, выделенной под массив
extern "C" {
void freeArrayMemory(double *array) {
    delete[] array;
}
}


// Функция для вычисления вектора гравитационного ускорения в инерциальной системе отсчета (ITRF)
extern "C" {
double* gravityVector_ITRF(const double* inputArray, double t_jd, int N_harmonics, char *model) {
    // Выделяем память под результат
    double *resultArray = new double[3];

    // Вычисляем количество дней с момента J2000
    const double DJ00 = 2451545.0;
    double t_jd_from_J2000 = (t_jd - DJ00);

    // Вычисляем угол theta
    double theta = 2 * M_PI * (0.7790572732640 + 1.00273781191135448 * t_jd_from_J2000);
    double COS = cos(theta);
    double SIN = sin(theta);

    // Переводим координаты из ITRF в GCRF
    double x_GCRF = inputArray[0] * COS + inputArray[1] * SIN;
    double y_GCRF = inputArray[0] * -SIN + inputArray[1] * COS;
    double z_GCRF = inputArray[2];

    // Инициализируем объект GravityModel с использованием модели egm2008 и пути к данным гравитационной модели
    GeographicLib::GravityModel gravity(model, "/opt/homebrew/Cellar/geographiclib/gravity", N_harmonics, N_harmonics);

    // Рассчитываем вектор гравитационного ускорения в GCRF
    double gx_GCRF, gy_GCRF, gz_GCRF;
    gravity.V(x_GCRF, y_GCRF, z_GCRF, gx_GCRF, gy_GCRF, gz_GCRF);

    // Переводим результат обратно в ITRF
    resultArray[0] = gx_GCRF * COS - gy_GCRF * SIN;
    resultArray[1] = gx_GCRF * SIN + gy_GCRF * COS;
    resultArray[2] = gz_GCRF;

    // Выводим в консоль полученный вектор гравитационного ускорения
    //std::cout << "Gravity вектор: (" << resultArray[0] << ", " << resultArray[1] << ", " << resultArray[2] << ")\n";

    return resultArray;
}
}