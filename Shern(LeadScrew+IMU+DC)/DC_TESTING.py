"""
Just to test importing the DC motor class,
but can used to adjust its angle

"""
import RPi.GPIO as GPIO
import time

# Import the DCMotor class from the dc_motor module
from back.DCMotor import DCMotor

# Create an instance of the DCMotor class
# Specify the GPIO pins and other parameters as needed
motor = DCMotor(In1=17, In2=27, EN=18, Duty=100)

# Perform operations with the motor

#Change directions here
motor.clockwise(1)   

motor.anticlockwise(0)# Bring up


# Or other operations as needed

# Don't forget to clean up GPIO ports when done
del motor
