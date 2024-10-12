import asyncio
from gpiozero import PWMOutputDevice, DigitalOutputDevice

class StepperMotor:
    def __init__(self, pin_step, pin_dir, pin_enable):
        self.pin_step = PWMOutputDevice(pin_step)
        self.pin_dir = DigitalOutputDevice(pin_dir)

        self.pin_enable = pin_enable

        if self.pin_enable is not None:
            self.pin_enable = DigitalOutputDevice(pin_enable)

    async def run_steps(self, steps, speed, direction, acc_step, dec_step, start_speed, end_speed):
        self.pin_dir.value = direction

        if self.pin_enable is not None:
            self.pin_enable.value = True  # Включаем двигатель

        if acc_step > 0:
            acceleration_steps = steps // acc_step
        else:
            acceleration_steps = 0

        if dec_step > 0:
            deceleration_steps = steps // dec_step
        else:
            deceleration_steps = 0

        constant_speed_steps = steps - acceleration_steps - deceleration_steps

        # Ускорение
        for i in range(acceleration_steps):
            current_speed = start_speed + (speed - start_speed) * (i + 1) / acceleration_steps
            self.pin_step.frequency = current_speed
            self.pin_step.value = 0.5
            await asyncio.sleep(1 / current_speed)

        # Постоянная скорость
        self.pin_step.frequency = speed
        for _ in range(constant_speed_steps):
            self.pin_step.value = 0.5
            await asyncio.sleep(1 / speed)

        # Замедление
        for i in range(deceleration_steps):
            current_speed = speed - (speed - end_speed) * (i + 1) / deceleration_steps
            self.pin_step.frequency = current_speed
            self.pin_step.value = 0.5
            await asyncio.sleep(1 / current_speed)

        if self.pin_enable is not None:
            self.pin_enable.value = False  # Выключаем двигатель


async def main():
    motor1 = StepperMotor(pin_step=12, pin_dir=23, pin_enable=7)
    motor2 = StepperMotor(pin_step=18, pin_dir=15, pin_enable=None)

    # Запуск двух двигателей асинхронно
    await asyncio.gather(
        motor1.run_steps(10000, 900, False, 10, 10, 100, 100),
        motor2.run_steps(10000, 900, False, 10, 10, 100, 100)
    )

if __name__ == "__main__":
    asyncio.run(main())
