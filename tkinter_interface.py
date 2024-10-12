from tkinter import *
import time

import tkinter_var as tkinter_var 
from Filler_robot.Robots.robot_module import Robot_module
from Filler_robot.PumpStation.pumps import Pump_station

robot = Robot_module()
pump_station = Pump_station()


def label_update():
    label_X.config(text=str(robot.axis_x.motor.value))
    label_Y.config(text=str(robot.axis_y.motor.value))
    label_Z.config(text=str(robot.axis_z.motor.value))


def null():
	robot.null_value()	
	
	label_update()
	

def move(axis, direction):
	distance = int(txt_2.get())

	if direction:
		distance = distance
	else:
		distance = -distance
	
	if axis == 'x':
		robot.axis_x.motor.speed_def = float(txt_1.get())
		robot.axis_x.motor.move(distance)
	elif axis == 'y':
		robot.axis_y.motor.speed_def = float(txt_1.get())
		robot.axis_y.motor.move(distance)
	elif axis == 'z':
		robot.axis_z.motor.speed_def = float(txt_1.get())
		robot.axis_z.motor.move(distance)
	
	label_update()
	

def go():
	robot.axis_x.motor.speed_def = float(txt_1.get())
	robot.axis_y.motor.speed_def = float(txt_1.get())
	robot.axis_z.motor.speed_def = float(txt_1.get())

	step_x = int(txt_6.get())
	step_y = int(txt_7.get())
	step_z = int(txt_8.get())
	
	robot.move(step_x, step_y, step_z)
	
	label_update()
	
	
def home():
	step_x = int(txt_6.get())
	step_y = int(txt_7.get())
	step_z = int(txt_8.get())
	
	robot.move(-step_x, -step_y, -step_z)
	
	label_update()


def enable_all():
	if tkinter_var.enable == False:
		robot.axis_x.motor.enable_on(True)
		robot.axis_y.motor.enable_on(True)
		robot.axis_z.motor.enable_on(True)

		pump_station.pump_1.motor.enable_on(True)
		pump_station.pump_2.motor.enable_on(True)

		tkinter_var.enable = True
	else:
		robot.axis_x.motor.enable_on(False)
		robot.axis_y.motor.enable_on(False)
		robot.axis_z.motor.enable_on(False)

		pump_station.pump_1.motor.enable_on(False)
		pump_station.pump_2.motor.enable_on(False)

		tkinter_var.enable = False
	
	print('enable', tkinter_var.enable)


def pump1_pour(direction):
	pump_station.pump_1.step_amount = int(txt_13.get())

	distance = int(txt_9.get())

	if direction == False:
		distance = -1 * distance
	
	print(distance)
	
	pump_station.pump_1.motor.speed_def = float(txt_11.get())
	pump_station.pump_1.pour(distance)



def pump2_pour(direction):
	pump_station.pump_2.step_amount = int(txt_14.get())

	distance = int(txt_10.get())

	if direction == False:
		distance = -1 * distance

	print(distance)
		
	pump_station.pump_2.motor.speed_def = float(txt_12.get())
	pump_station.pump_2.pour(distance)
	

window = Tk ()
window.title('Управление шаговиком')

window.geometry('420x700')

txt_1 = Entry(window)
txt_1.grid (column=10, row=10)
txt_1.place(x=320, y=20, width=80, height=40)
txt_1.insert(END, '0.0001')

txt_2 = Entry(window)
txt_2.grid (column=10, row=10)
txt_2.place(x=320, y=70, width=80, height=40)
txt_2.insert(END, '500')

txt_6 = Entry(window)
txt_6.grid (column=10, row=10)
txt_6.place(x=300, y=160, width=80, height=40)
txt_6.insert(END, '0')

txt_7 = Entry(window)
txt_7.grid (column=10, row=10)
txt_7.place(x=300, y=200, width=80, height=40)
txt_7.insert(END, '0')

txt_8 = Entry(window)
txt_8.grid (column=10, row=10)
txt_8.place(x=300, y=240, width=80, height=40)
txt_8.insert(END, '0')


txt_9 = Entry(window)
txt_9.grid (column=10, row=10)
txt_9.place(x=70, y=450, width=80, height=40)
txt_9.insert(END, '50')

txt_10 = Entry(window)
txt_10.grid (column=10, row=10)
txt_10.place(x=250, y=450, width=80, height=40)
txt_10.insert(END, '50')


label_X = Label (window, text="Pour") 
label_X.place(x=20, y=450, width=30, height=40)

label_Y = Label (window, text="Speed") 
label_Y.place(x=20, y=500, width=40, height=40)


txt_11 = Entry(window)
txt_11.grid (column=10, row=10)
txt_11.place(x=70, y=500, width=80, height=40)
txt_11.insert(END, '0.000001')

txt_12 = Entry(window)
txt_12.grid (column=10, row=10)
txt_12.place(x=250, y=500, width=80, height=40)
txt_12.insert(END, '0.000001')


txt_13 = Entry(window)
txt_13.grid (column=10, row=10)
txt_13.place(x=70, y=550, width=80, height=40)
txt_13.insert(END, '200')

txt_14 = Entry(window)
txt_14.grid (column=10, row=10)
txt_14.place(x=250, y=550, width=80, height=40)
txt_14.insert(END, '200')


label_X = Label (window, text="X") 
label_X.place(x=90, y=160, width=80, height=40)

label_Y = Label (window, text="Y") 
label_Y.place(x=90, y=200, width=80, height=40)

label_Z = Label (window, text="Z") 
label_Z.place(x=90, y=240, width=80, height=40)


button_6 = Button (window, text="X+", command = lambda: move('x', False))
button_6.place(x=30, y=20, width=30, height=40)

button_3 = Button (window, text="X-", command = lambda: move('x', True))
button_3.place(x=30, y=70, width=30, height=40)

button_1 = Button (window, text="Y+", command = lambda: move('y', True))
button_1.place(x=60, y=20, width=30, height=40)

button_2 = Button (window, text="Y-", command = lambda: move('y', False))
button_2.place(x=60, y=70, width=30, height=40)

button_5 = Button (window, text="Z+", command = lambda: move('z', True))
button_5.place(x=90, y=20, width=30, height=40)

button_4 = Button (window, text="Z-", command = lambda: move('z', False))
button_4.place(x=90, y=70, width=30, height=40)



button_19 = Button (window, text="Home", command = lambda: home())
button_19.place(x=0, y=300, width=100, height=40)

button_20 = Button (window, text="Null", command = lambda: null())
button_20.place(x=70, y=300, width=100, height=40)

button_21 = Button (window, text="enable_all", command = lambda: enable_all())
button_21.place(x=0, y=600, width=100, height=40)

button_22 = Button (window, text="GO", command = lambda: go())
button_22.place(x=250, y=300, width=100, height=40)

button_23 = Button (window, text="Pump 1 (-)", command = lambda: pump1_pour(False))
button_23.place(x=70, y=350, width=100, height=40)

button_24 = Button (window, text="Pump 2 (-)", command = lambda: pump2_pour(False))
button_24.place(x=250, y=350, width=100, height=40)

button_25 = Button (window, text="Pump 1 (+)", command = lambda: pump1_pour(True))
button_25.place(x=70, y=400, width=100, height=40)

button_26 = Button (window, text="Pump 2 (+)", command = lambda: pump2_pour(True))
button_26.place(x=250, y=400, width=100, height=40)


download_label_1 = Label (window, text="Скорость") 
download_label_1.place(x=210, y=20, width=80, height=40)

download_label_2 = Label (window, text="Дистанция") 
download_label_2.place(x=210, y=70, width=80, height=40)

download_label_3 = Label (window, text="X") 
download_label_3.place(x=20, y=160, width=80, height=40)

download_label_4 = Label (window, text="Y") 
download_label_4.place(x=20, y=200, width=80, height=40)

download_label_5 = Label (window, text="Z") 
download_label_5.place(x=20, y=240, width=80, height=40)

download_label_7 = Label (window, text="Задать") 
download_label_7.place(x=220, y=120, width=80, height=40)

download_label_6 = Label (window, text="Текущие") 
download_label_6.place(x=70, y=120, width=80, height=40)

download_label_8 = Label (window, text="X") 
download_label_8.place(x=180, y=160, width=80, height=40)

download_label_9 = Label (window, text="Y") 
download_label_9.place(x=180, y=200, width=80, height=40)

download_label_10 = Label (window, text="Z") 
download_label_10.place(x=180, y=240, width=80, height=40)


download_label_11 = Label (window, text="Y") 
download_label_11.place(x=180, y=200, width=80, height=40)

download_label_12 = Label (window, text="Z") 
download_label_12.place(x=180, y=240, width=80, height=40)


label_update()

window.mainloop()
