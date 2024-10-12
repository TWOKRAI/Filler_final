import time

from Filler_robot.Robot.robot import robot, axis_x, axis_y, axis_z

from Decorators.wrapper import _timing


@_timing
def regulator_angle(x0, y0, z0, func):
	def error_fix(name, coord0, coord, angle, direct):
		error = coord - coord0

		if error <= 0 and direct == True or error >= 0 and direct == False:
			if abs(error) > 0.1:
				angle += 0.01 * abs(error)
			else:
				angle += 0.001 * abs(error) 
		else:
			if abs(error) > 0.1:
				angle -= 0.01 * abs(error)
			else:
				angle -= 0.001 * abs(error) 
		



		# print(f"{name}: {angle} {error}")

		return angle, error


	error_x = 1
	error_y = 1
	error_z = 1

	angle_x0 = 0
	angle_y0 = 0
	angle_z0 = 0

	angle_x = 0
	angle_y = 0
	angle_z = 0

	d = 0.5

	i = 0
	t = 0
	
	delta_x = 0
	delta_y = 0
	delta_z = 0
	
	error = False

	while abs(error_x) > d + delta_x or abs(error_y) > d + delta_y or abs(error_z) > d + delta_z:
		x, y, z = func(angle_x, angle_y, angle_z)

		#print(error_x, error_y, error_z)

		angle_x, error_x = error_fix('x', x0, x, angle_x, False)
		angle_y, error_y = error_fix('y', y0, y, angle_y, True)
		angle_z, error_z = error_fix('z', z0, z, angle_z, True)
		
		i += 1
		
		if i > 500:
			# error = True
			# print('ERORR COORD')
			# print('£££££££££££££££££££££££££££££££££££££££££££')
			# print(f"angle_x: {angle_x} {error_x}")
			# print(f"angle_y: {angle_y} {error_y}")
			# print(f"angle_z: {angle_z} {error_z}")
			if abs(error_x) > d + delta_x:
				delta_x += 0.2
			
			if abs(error_y) > d + delta_y:
				delta_y += 0.1
				
			if abs(error_z) > d + delta_z:
				delta_z += 0.1
			
			i = 0

			#break
		elif t > 10000:
			print('ERORR COORD')
			error = True
		
		t += 1
	

	print('i', i)
	
	if abs(angle_x) >= 360:
		angle_x = angle_x % 360
	
	if abs(angle_y) >= 360:
		angle_y = angle_y % 360 
			
	if abs(angle_z) >= 360:
		angle_z = angle_z % 360 

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

	x, y, z = robot.angle_to_coord(38, -110, -60)

	

	angle_x2, angle_y2, angle_z2, error = regulator_angle(14, 18, 12, robot.angle_to_coord)
	
	print(x, y, z)
	print(angle_x2, angle_y2, angle_z2)

	while False:
		while True:
			print('----------------------------')
			
			# angle_x = int(input('angle_x:'))
			# angle_y = int(input('angle_y:'))
			# angle_z = int(input('angle_z:'))
			
			error = False
			
			x, y, z = robot.angle_to_coord(angle_x, angle_y, angle_z)
			
			
			# print(f"angle_to_x: {angle_x} {x}")
			# print(f"angle_to_y: {angle_y} {y}")
			# print(f"angle_to_z: {angle_z} {z}")
			
			angle_x2, angle_y2, angle_z2, error = regulator_angle(x, y, z, robot.angle_to_coord)

			x2, y2, z2 = robot.angle_to_coord(angle_x2, angle_y2, angle_z2)
			
			delta_x = abs(x - x2)
			delta_y = abs(y - y2)
			delta_z = abs(z - z2)
			
			delta_ang_x = abs(angle_x - angle_x2)
			delta_ang_y = abs(angle_y - angle_y2)
			delta_ang_z = abs(angle_z - angle_z2)
			
			
			if delta_ang_x > 1 or delta_ang_y > 1 or delta_ang_y > 1:
				print(f"x_to_angle: {x} {x2} {delta_x} angle {angle_x} {angle_x2} {delta_ang_x} ")
				print(f"y_to_angle: {y} {y2} {delta_y} angle {angle_y} {angle_y2} {delta_ang_y} ")
				print(f"z_to_angle: {z} {z2} {delta_z} angle {angle_z} {angle_z2} {delta_ang_z} ")
				
			angle_x += 0
			angle_y -= 1
			
			
			if angle_y <= -90:
				angle_y = 0
				break

			if error == True:
				break
			
			#time.sleep(0.1)
			
		angle_z -= 1

		if error == True:
			break
		
		if angle_z <= -90:
			break

