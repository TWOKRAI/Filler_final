from pins_table import pins
import time
import tkinter as tk


class ToggleButton:
    def __init__(self, root):
        self.root = root

        self.running = False
        
        # Добавление полей для ввода step_value и speed
        self.step_value_entry = tk.Entry(root)
        self.step_value_entry.insert(0, "100000")  # Значение по умолчанию
        self.step_value_entry.pack()

        self.speed_entry = tk.Entry(root)
        self.speed_entry.insert(0, "0.0001")  # Значение по умолчанию
        self.speed_entry.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()

        spacer = tk.Frame(root, height=20)
        spacer.pack()


        
        self.pin_enable = pins.motor_y_enable
        self.pin_enable.set_value(0)
        self.state = False
        self.button1 = tk.Button(root, text=f"enable {self.pin_enable}", command=lambda: self.enable(self.pin_enable))
        self.button1.pack()

        
        self.pin_step = pins.motor_y_step
        self.pin_step.set_value(0)
        self.state2 = False
        self.button2 = tk.Button(root, text=f"step {self.pin_step}", command=lambda: self.step(self.pin_step))
        self.button2.pack()

        self.button4 = tk.Button(root, text=f"step_while {self.pin_step}", command=lambda: self.step_while(self.pin_step))
        self.button4.pack()


        self.pin_dir = pins.motor_y_dir
        self.pin_step.set_value(0)
        self.state3 = False
        self.button3 = tk.Button(root, text=f"dir {self.pin_dir}", command=lambda: self.dir(self.pin_dir))
        self.button3.pack()
        
        spacer = tk.Frame(root, height=20)
        spacer.pack()




        # self.pin_enable2 = 17
        # pins.set_value(self.pin_enable2 , False)
        # self.state = False
        # self.button5 = tk.Button(root, text=f"enable_x {self.pin_enable2}", command=lambda: self.enable(self.pin_enable2))
        # self.button5.pack()


        # self.pin_step2 = 22
        # pins.set_value(self.pin_step2 , False)
        # self.state2 = False
        # self.button6 = tk.Button(root, text=f"step_x {self.pin_step2}", command=lambda: self.step(self.pin_step2))
        # self.button6.pack()

        # self.button7 = tk.Button(root, text=f"step_x_while {self.pin_step2}", command=lambda: self.step_while(self.pin_step2))
        # self.button7.pack()


        # self.pin_dir2 = 27
        # pins.set_value(self.pin_dir2, False)
        # self.state3 = False
        # self.button8 = tk.Button(root, text=f"dir_x {self.pin_dir2}", command=lambda: self.dir(self.pin_dir2))
        # self.button8.pack()

        # spacer = tk.Frame(root, height=20)
        # spacer.pack()

        
        
        # self.pin_enable3 = 2
        # pins.set_value(self.pin_enable3 , False)
        # self.state = False
        # self.button9 = tk.Button(root, text=f"enable_y {self.pin_enable3}", command=lambda: self.enable(self.pin_enable3))
        # self.button9.pack()


        # self.pin_step3 = 4
        # pins.set_value(self.pin_step3 , False)
        # self.state2 = False
        # self.button10 = tk.Button(root, text=f"step_y {self.pin_step3}", command=lambda: self.step(self.pin_step3))
        # self.button10.pack()

        # self.button11 = tk.Button(root, text=f"step_y_while {self.pin_step3}", command=lambda: self.step_while(self.pin_step3))
        # self.button11.pack()


        # self.pin_dir3 = 3
        # pins.set_value(self.pin_dir3, False)
        # self.state3 = False
        # self.button12 = tk.Button(root, text=f"dir_y {self.pin_dir3}", command=lambda: self.dir(self.pin_dir3))
        # self.button12.pack()

        # spacer = tk.Frame(root, height=20)
        # spacer.pack()




        # self.pin_enable4 = 16
        # pins.set_value(self.pin_enable4 , False)
        # self.state = False
        # self.button13 = tk.Button(root, text=f"enable_z {self.pin_enable4}", command=lambda: self.enable(self.pin_enable4))
        # self.button13.pack()


        # self.pin_step4 = 21
        # pins.set_value(self.pin_step4, False)
        # self.state2 = False
        # self.button14 = tk.Button(root, text=f"step_z {self.pin_step4}", command=lambda: self.step(self.pin_step4))
        # self.button14.pack()

        # self.button15 = tk.Button(root, text=f"step_z_while {self.pin_step4}", command=lambda: self.step_while(self.pin_step4))
        # self.button15.pack()


        # self.pin_dir4 = 20
        # pins.set_value(self.pin_dir4, False)
        # self.state3 = False
        # self.button16 = tk.Button(root, text=f"dir_z {self.pin_dir4}", command=lambda: self.dir(self.pin_dir4))
        # self.button16.pack()

        # spacer = tk.Frame(root, height=20)
        # spacer.pack()



        # self.pin_enable5 = 14
        # pins.set_value(self.pin_enable5 , False)
        # self.state = False
        # self.button17 = tk.Button(root, text=f"enable_p1p2 {self.pin_enable5}", command=lambda: self.enable(self.pin_enable5))
        # self.button17.pack()


        # self.pin_step5 = 18
        # pins.set_value(self.pin_step5 , False)
        # self.state2 = False
        # self.button18 = tk.Button(root, text=f"step_p1 {self.pin_step5}", command=lambda: self.step(self.pin_step5))
        # self.button18.pack()

        # self.button19 = tk.Button(root, text=f"step_p1_while {self.pin_step5}", command=lambda: self.step_while(self.pin_step5))
        # self.button19.pack()


        # self.pin_dir5 = 15
        # pins.set_value(self.pin_dir5, False)
        # self.state3 = False
        # self.button20 = tk.Button(root, text=f"dir_p1 {self.pin_dir5}", command=lambda: self.dir(self.pin_dir5))
        # self.button20.pack()

        # spacer = tk.Frame(root, height=20)
        # spacer.pack()



        # self.pin_step6 = 24
        # pins.set_value(self.pin_step6 , False)
        # self.state2 = False
        # self.button21 = tk.Button(root, text=f"step_p2 {self.pin_step6}", command=lambda: self.step(self.pin_step6))
        # self.button21.pack()

        # self.button22 = tk.Button(root, text=f"step_p2_while {self.pin_step6}", command=lambda: self.step_while(self.pin_step6))
        # self.button22.pack()


        # self.pin_dir6 = 23
        # pins.set_value(self.pin_dir6, False)
        # self.state3 = False
        # self.button23 = tk.Button(root, text=f"dir_p2 {self.pin_dir6}", command=lambda: self.dir(self.pin_dir6))
        # self.button23.pack()




    def enable(self, pin):
        self.state = not self.state

        if self.state:
            pin.set_value(1)
        else:
            pin.set_value(0)



    def step(self, pin):
        self.state2 = not self.state2

        if self.state2:
            pin.set_value(1)
        else:
            pin.set_value(0)


    def dir(self, pin):
        self.state3 = not self.state3
        
        if self.state3:
            pin.set_value(1)
        else:
            pin.set_value(0)

        pin.get_value(pin)

    
    def step_while(self, pin):
        self.running = True
        step_value = int(self.step_value_entry.get())
        speed = float(self.speed_entry.get())
        i = 0

        while i < step_value and self.running:
            pin.set_value(1)
            # pins.get_value_log()
            time.sleep(speed)

            pin.set_value(0)
            # pins.get_value_log(pin)
            time.sleep(speed)

            i += 1
            print(i)

        
    def stop(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    toggle_button = ToggleButton(root)
    root.mainloop()