import time

from robot import robot

from Decorators.wrapper import _timing


@_timing
def regulator_angle(x0, y0, z0, func):

	error_x = 10
	error_y = 10
	error_z = 10

	angle_x = 0
	angle_y = 120
	angle_z = 145

	h = 1
	i = 0
	t = 0
	
	delta_x = 0
	delta_y = 0
	delta_z = 0
	
	error = False

	

	while True:
		x, y, z, error_limit_x, error_limit_y, error_limit_z = func(angle_x, angle_y, angle_z)

		# print(f"angle_x: {angle_x} x: {x}")
		# print(f"angle_y: {angle_y} y: {y}")
		# print(f"angle_z: {angle_z} z: {z}")

		if y <= y0:
			if error_limit_y == False:
				angle_y -= 1* h

			if error_limit_z == False:
				angle_z -= 1 * h
		else:
			h = 0.01

			if error_limit_x == False:
				if x0 > 0:
					if x < x0:
						angle_x += 1 * h
				else:
					if x > x0:
						angle_x -= 1 * h
		
			if abs(x) >= abs(x0):
				if z <= z0:
					if error_limit_y == False:
						angle_y -= 1 * h

					if error_limit_z == False:
						angle_z -= 2 * h
				else:

					angle_y += 1 * h

					angle_z += 2 * h
				
		if error_limit_y == True:
			angle_y += 1 


		
		i += 1

		#print(i)
		
		if abs(x) >= abs(x0) and y >= y0 and z <= z0:
			#print(f"angle_x: {angle_x} x: {x}")
			#print(f"angle_y: {angle_y} y: {y}")
			#print(f"angle_z: {angle_z} z: {z}")
			print('ZZZZZZZZZZZZZZZZZZZZZZz', 'x0, y0, z0', x0, y0, z0)
			break
			
		

		# if  error_limit_x or error_limit_y or error_limit_z:
		# 	print('ERROR', error_limit_x, error_limit_y, error_limit_z)
		# 	break


	angle_x = round(angle_x, 3)
	angle_y = round(angle_y, 3)
	angle_z = round(angle_z, 3)

	# print(f"angle_x: {angle_x} {error_x}")
	# print(f"angle_y: {angle_y} {error_y}")
	# print(f"angle_z: {angle_z} {error_z}")

	return angle_x, angle_y, angle_z, error



# x0 = 9.8
# y0 = 13.8
# z0 = 24.5


# x0 = 10
# y0 = 13.7
# z0 = 27.8

# angle_x, angle_y, angle_z = regulator_angle(x0, y0, z0, robot.angle_to_coord)

if __name__ == '__main__':
	angle_x = -40
	angle_y = 0
	angle_z = 0

	# x, y, z,_,_,_ = robot.angle_to_coord(0, 2, 35)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 35)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 55)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 90)

	# x, y, z,_,_,_ = robot.angle_to_coord(0, 2, 145)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 145)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 125)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 90)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 40, 90)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 120, 35)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 100, 55)
	# x, y, z,_,_,_ = robot.angle_to_coord(0, 80, 75)

	x, y, z,_,_,_ = robot.angle_to_coord(0, 2, 35)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 35)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 55)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 22, 90)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 40, 90)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 120, 145)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 100, 125)
	x, y, z,_,_,_ = robot.angle_to_coord(0, 80, 115)

	x, y, z,_,_,_ = robot.angle_to_coord(45, 10, 100)

	input('GGGGG')


	

	# angle_x2, angle_y2, angle_z2, error = regulator_angle(14, 18, 12, robot.angle_to_coord)
	
	# print(x, y, z)
	# print(angle_x2, angle_y2, angle_z2)

	while True:
		x = 16
		y = 15
		z = 13

		angle_x2, angle_y2, angle_z2, error = regulator_angle(x, y, z, robot.angle_to_coord)
		input('GGGGG')

	
