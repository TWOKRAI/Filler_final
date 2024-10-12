# import numpy as np
# from scipy.optimize import curve_fit


# # Пример данных
# # Пиксельные координаты (x, y)
# points1 = np.array([
#     (0, 13.0),
#     (0, 18.1),
#     (0, 22.3),
#     (0, 25.5),
#     (0, 28.4), 
#     (0, 30.4), 
#     (0, 32.5),
#     (0, 34), 
# ])

# # Реальные координаты (x_real, y_real)
# points2 = np.array([
#     (0, 13),
#     (0, 16),
#     (0, 19),
#     (0, 22),
#     (0, 25),
#     (0, 28),
#     (0, 31),
#     (0, 34),
# ])

# # Функция для подбора
# def quadratic_function(y, a, b):
#     return a * y + b * y**2

# # Подбор коэффициентов
# params, _ = curve_fit(quadratic_function, pixel_points[:, 1], real_points[:, 1])
# a, b = params

# print(f"a = {a}, b = {b}")


# import numpy as np
# from numpy.polynomial.polynomial import Polynomial

# # Измеренные координаты
# points1 = np.array([
#     (0, 13.0),
#     (0, 18.1),
#     (0, 22.3),
#     (0, 25.5),
#     (0, 28.4),
#     (0, 30.4),
#     (0, 32.5),
#     (0, 34),
# ])

# # Реальные координаты
# points2 = np.array([
#     (0, 13),
#     (0, 16),
#     (0, 19),
#     (0, 22),
#     (0, 25),
#     (0, 28),
#     (0, 31),
#     (0, 34),
# ])

# # Извлекаем y-координаты
# y_measured = points1[:, 1]
# y_real = points2[:, 1]

# # Полиномиальная регрессия (например, степень 2)
# degree = 2
# p = Polynomial.fit(y_measured, y_real, degree)

# # Преобразуем координаты
# y_transformed = p(y_measured)

# # Вычисляем погрешность
# error = y_transformed - y_real

# # Выводим результаты
# for i in range(len(y_measured)):
#     print(f"Измеренная координата: {y_measured[i]}, Реальная координата: {y_real[i]}, Преобразованная координата: {y_transformed[i]}, Погрешность: {error[i]}")



import numpy as np
from numpy.polynomial.polynomial import Polynomial


# Измеренные координаты
points1 = np.array([
    (0, 12.5),
    (0, 17.4),
    (0, 21.6),
    (0, 24.8),
    (0, 27.7),
    (0, 29.9),
    (0, 32.0),
    (0, 33.5),
])

# Реальные координаты
points2 = np.array([
    (0, 12.5),
    (0, 15.5),
    (0, 18.5),
    (0, 21.5),
    (0, 24.5),
    (0, 27.5),
    (0, 20.5),
    (0, 33.5),
])
    

# Извлекаем y-координаты
y_measured = points1[:, 1]
y_real = points2[:, 1]

# Полиномиальная регрессия (например, степень 2)
degree = 2
p = Polynomial.fit(y_measured, y_real, degree)

# Функция для преобразования одной координаты
def transform_coordinate(y_measured):
    return p(y_measured)

# Проходим по цифрам от 13 до 35 с шагом 0.1
for y_measured in np.arange(13, 35.1, 0.1):
    y_transformed = transform_coordinate(y_measured)
    # Находим ближайшую реальную координату
    y_real_closest = y_real[np.argmin(np.abs(y_real - y_transformed))]

    print(f"Измеренная координата: {y_measured}, Преобразованная координата: {y_transformed}")
