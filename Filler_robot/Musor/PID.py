import math

from Decorators.wrapper import _timing


def angle_to_coord(angle_x, angle_y, angle_z): 
    angle_x0 = 0
    angle_y0 = 120
    angle_z0 = -30

    y0 = 0
    z0 = 22

    arm_lenght_y = 12
    arm_lenght_z = 12
    lenght_filler = 4


    angle_x1 = angle_x0 + angle_x
    angle_y1 = angle_y0 + angle_y
    angle_z1 = angle_z0 + angle_z

    y1 = y0 + arm_lenght_y * math.cos(math.radians(angle_y1))
    z1 = z0 + arm_lenght_y * math.sin(math.radians(angle_y1))

    #print('angle_to_1', 0, round(y1, 1), round(z1, 1))

    y2 = y1 + arm_lenght_z * math.cos(math.radians(angle_z1 - angle_y))
    
    z2 = z1 + arm_lenght_z * math.sin(math.radians(angle_z1)) 

    #print('angle_to_2', 0, round(y2, 1), round(z2, 1) )

    y3 = y2 * math.cos(math.radians(angle_x1)) + lenght_filler
    x3 = y2 * math.sin(math.radians(angle_x1))

    #print('angle_to_1',round(x3, 3), round(y3, 3), round(z2, 3))

    return round(x3, 3), round(y3, 3), round(z2, 3)


@_timing
def pid_controller(x0, y0, z0):
    def error_fix(name, coord0, coord, angle, direct):
        error = coord - coord0
		
        if error <= 0 and direct == True or error >= 0 and direct == False:
            if abs(error) > 0.01:
                angle += 1 * abs(error)
            else:
                angle += 0.001 * abs(error) 
        else:
            if abs(error) > 0.01:
                angle -= 1 * abs(error)
            else:
                angle -= 0.001 * abs(error) 

        # print(f"{name}: {angle} {error}")

        return angle


    # Определить начальные значения ошибок и производных ошибок
    error_x = 10
    error_y = 10
    error_z = 10

    angle_x = 0
    angle_y = 0
    angle_z = 0

    d = 0.01

    # Цикл регулятора
    while abs(error_x) > d or abs(error_y) > d or abs(error_z) > d:
        # Вычислить новые координаты с помощью функции angle_to_coord
        x, y, z = angle_to_coord(angle_x, angle_y, angle_z)

        # Вычислить ошибки
        error_x = x - x0
        error_y = y - y0
        error_z = z - z0

        #print(error_x, error_y, error_z)

        # Обновить углы

        angle_x = error_fix('x', x0, x, angle_x, True)
        angle_y = error_fix('y', y0, y, angle_y, False)
        angle_z = error_fix('z', z0, z, angle_z, True)

    angle_x = round(angle_x, 1)
    angle_y = round(angle_y, 1)
    angle_z = round(angle_z, 1)

    print(f"angle_x: {angle_x}")
    print(f"angle_y: {angle_y}")
    print(f"angle_z: {angle_z}")

    return angle_x, angle_y, angle_z


# Для x = 9.8, y = 13.8, z = 24.5:

# angle_x = 45.0
# angle_y = -40.0
# angle_z = -21.0




# angle_x = 30.0
# angle_y = -30.0
# angle_z = -30.0

# Начальные значения

x, y, z = angle_to_coord(0, -20, 0)
print('11111111111', x, y, z)

angle_x0 = 0
angle_y0 = 0
angle_z0 = 0


x0 = 9.8
y0 = 13.8
z0 = 24.5


angle_x, angle_y, angle_z = pid_controller(x0, y0, z0)




# angle_to_coord(45, -40, -20)


# x0 = 5.2
# y0 = 13.0
# z0 = 23.6

# # Выполнить регулятор
# angle_x, angle_y, angle_z = pid_controller(x0, y0, z0)


# x0 = 0
# y0 = 14.0
# z0 = 22.6

# angle_x, angle_y, angle_z = pid_controller(x0, y0, z0)


# x0 = -14.5
# y0 = 20
# z0 = 17

# angle_x, angle_y, angle_z = pid_controller(x0, y0, z0)
