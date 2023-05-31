from simple_pid import PID
import math

# Set the PID gains
kp = 0.5
ki = 0.1
kd = 0.2

PWM = [0, 0, 0, 0, 0, 0]
# Create an instance of the PID controller
pidController = PID(kp, ki, kd, setpoint=0)

angle1 = 0.0    # Offset for motor1
angle2 = 2 * math.pi / 3  # Offset for motor2
angle3 = 4 * math.pi / 3  # Offset for motor3
    
def Movement(currentPosition, goalPosition):
    
    errorx = goalPosition[0] - currentPosition[0]
    errory = goalPosition[1] - goalPosition[1]
    
    velocity_x = pidController(errorx,0.01)
    velocity_y = pidController(errory,0.01)
        
    # Calculate the motor velocities based on the velocity components and wheel configuration
    PWM[0] = velocity_x * math.cos(angle1) + velocity_y * math.sin(angle1) 
    PWM[1] = velocity_x * math.cos(angle2) + velocity_y * math.sin(angle2) 
    PWM[2] = velocity_x * math.cos(angle3) + velocity_y * math.sin(angle3) 
    print("seemstowork")
    if PWM[0] > 0:
        PWM[3] = 1
    else:
        PWM[3] = 0
        PWM[0] = abs(PWM[0])
    if PWM[1] > 0:
        PWM[4] = 1
    else:
        PWM[4] = 0
        PWM[1] = abs(PWM[1])
    if PWM[2] > 0:
        PWM[5] = 1
    else:
        PWM[5] = 0
        PWM[2] = abs(PWM[2])
    return PWM