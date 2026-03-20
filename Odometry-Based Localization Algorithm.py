import math


# robot values
wheel_diameter = 0 
wheel_circumference = math.pi* wheel_diameter
axle_track = 0 


# used to avoid error
last_linear = 0
last_robot_heading = 0


# updates values related with calculation of localization
def update_robot_sensors():
  global last_linear, last_robot_heading 
  global linear_difference, robot_heading_difference, current_robot_heading 

  # reads sensors and sets current values
  right_motor_angle = 0 # right encoder motor angle read (in radians)
  left_motor_angle = 0 # left encoder motor angle read (in radians)
  current_linear = (right_motor_angle + left_motor_angle) * wheel_circumference/(4*math.pi)
  current_robot_heading =  (right_motor_angle - left_motor_angle) * wheel_circumference/(2*math.pi*axle_track) # robot angle relative to the cartesian plane (in radians). Gyro can be used if available

  # finds the difference with the values of previous check
  linear_difference = current_linear - last_linear
  robot_heading_difference = current_robot_heading - last_robot_heading

  # saves current values for future use
  last_linear = current_linear
  last_robot_heading = current_robot_heading


def localization():  
  global robot_x, robot_y, current_robot_heading, linear_difference, robot_heading_difference

  if robot_heading_difference != 0:
    trajectory_radius = linear_difference/robot_heading_difference
    overall_displacement = 2*trajectory_radius*math.sin(robot_heading_difference/2)

  else:
    overall_displacement = linear_difference

  robot_x += overall_displacement * math.cos(current_robot_heading - robot_heading_difference/2)
  robot_y += overall_displacement * math.sin(current_robot_heading - robot_heading_difference/2)


# forever loop to run the code
while True:
  update_robot_sensors()
  localization()