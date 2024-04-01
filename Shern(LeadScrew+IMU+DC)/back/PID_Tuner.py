"""
Class and definitions used for PID control
Unused here, but backup.py needs this to run, not important
"""
#Code used to tune PID controller for IMU+Leadscrew

class PIDController:
    def __init__(self, kp, ki, kd, setpoint,upper_bound,lower_bound):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.prev_error = 0
        self.integral = 0
    def calculate(self, angle):
        error = self.setpoint - angle
        self.integral += error
        derivative = error - self.prev_error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        output = round(output)
        output = abs(output)
        if(output >= self.upper_bound):
            output = self.upper_bound
        elif(output <= self.lower_bound):
            output = self.lower_bound       

        return output
