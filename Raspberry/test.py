from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

# Конфигурация пинов
STEP_PIN = 12  # Пин для шагового сигнала
DIR_PIN = 23   # Пин для направления

# Создание объекта PWM для шагового сигнала
step_pwm = PWMOutputDevice(STEP_PIN, frequency=1000)  # Частота 500 Гц (2 мс на шаг)
step_pwm2 = PWMOutputDevice(18, frequency=1000)
# Создание объекта для управления направлением
dir_pin = DigitalOutputDevice(DIR_PIN)
enable_pin = DigitalOutputDevice(7)

try:
    # Установка направления (1 для одного направления, 0 для другого)
    dir_pin.on()  # Установите dir_pin.off() для другого направления
    enable_pin.on()
    # Установка скважности для постоянной скорости
    step_pwm.value = 0.5  # 50% скважность
    step_pwm2.value = 0.5

    # Вращение двигателя в течение 5 секунд
    time.sleep(25)

except KeyboardInterrupt:
    print("Программа остановлена пользователем")

finally:
    # Остановка PWM и очистка
    step_pwm.off()
    step_pwm2.off()
    dir_pin.off()
    enable_pin.off()
