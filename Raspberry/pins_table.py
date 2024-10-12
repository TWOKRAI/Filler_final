import gpiod
import gpiozero as gz


class Pins():
    def __init__(self):
        self.chip = gpiod.Chip('gpiochip4')

        self.release_all_lines()
    
        self.motor_step = gz.PWMOutputDevice(13)

        self.motor_dir = self.pin_init(19)
        self.motor_enable = self.pin_init(26)

        self.laser = self.pin_init(24)

        self.button_stop = self.pin_init(14)
        self.button = self.pin_init(5)
        self.switch_out = self.pin_init(8)
        self.switch_in = self.pin_init(6)

        self.switch_x = self.pin_init(25)
        self.switch_y = self.pin_init(10)

        self.motor_x_step = self.pin_init(22)
        self.motor_x_dir = self.pin_init(27)
        self.motor_x_enable = self.pin_init(17)

        self.motor_y_step = self.pin_init(4)
        self.motor_y_dir = self.pin_init(3)
        self.motor_y_enable = self.pin_init(2)

        self.motor_z_step = self.pin_init(21)
        self.motor_z_dir = self.pin_init(20)
        self.motor_z_enable = self.pin_init(16)

        # self.motor_p1_step = self.pin_init(18)
        self.motor_p1_step = gz.PWMOutputDevice(12)
        self.motor_p1_dir = self.pin_init(23)
        
        # self.motor_p2_step = self.pin_init(24)
        self.motor_p2_step = gz.PWMOutputDevice(18)
        self.motor_p2_dir = self.pin_init(15)

        self.motor_p1p2_enable = self.pin_init(7)

        self.laser.set_value(1)


    def release_all_lines(self):
        for line_offset in range(self.chip.num_lines()):
            line = self.chip.get_line(line_offset)
            if line.is_requested():
                line.release()


    def pin_init(self, pin_number):
        line = self.chip.get_line(pin_number)
        if not line.is_requested():
            line.request(consumer="GPIODController", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
        
        return line
    

    def get_value_log(self, pin):
        if pin.get_value() == 1:
            print(f'{pin} - ON')
        elif pin.get_value() == 0:
            print(f'{pin} - OFF')



pins = Pins()


if __name__ == '__main__':
    import time

    pins.motor_enable.set_value(1)
    pins.motor_x_enable.set_value(0)
    pins.motor_y_enable.set_value(0)
    pins.motor_z_enable.set_value(0)
    pins.motor_p1p2_enable.set_value(0)

    pins.get_value_log(pins.motor_enable)
    pins.get_value_log(pins.motor_x_enable)
    pins.get_value_log(pins.motor_y_enable)
    pins.get_value_log(pins.motor_z_enable)
    pins.get_value_log(pins.motor_p1p2_enable)

    pins.motor_p1p2_enable.set_value(1)

    pins.motor_p2_dir.set_value(1)

    while True:
        # pins.get_value_log(pins.switch_y)
        # pins.get_value_log(pins.button_stop)
        # pins.get_value_log(pins.button)

        # time.sleep(1)
        
        # pins.laser.set_value(1)
        # pins.get_value_log(pins.laser)

        # time.sleep(1)

        # pins.laser.set_value(1)

        # pins.get_value_log(pins.laser)

        pins.motor_p2_step.frequency = 30
        
        pins.motor_p2_step.value = 0.5
