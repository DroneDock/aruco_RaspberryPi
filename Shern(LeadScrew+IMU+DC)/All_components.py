"""
Shern Kai working code, 

Result
Now only using shared variable. Works.

Implement all motors into one code.
Progress 31 March 2024

"""
#Standard imports
import time
import multiprocessing as mp
#from multiprocessing import Queue
#Not used

# Project Specific Imports
from back.Leadscrew import StepperMotor
from back.ShernIMU import AdafruitBNO055
from back.DCMotor import DCMotor
from back.BottomStepper import StepperMotor

import RPi.GPIO as GPIO



#to put IMU readings into a value
def fetchEulerAngle(top_angle,bot_angle):
    Top_IMU = AdafruitBNO055() #Top IMU
    Bot_IMU = AdafruitBNO055(ADR=True) #Bottom IMU
    while True:
        try:
            top_angle.value = Top_IMU.eulerAngles[1]
            bot_angle.value = Bot_IMU.eulerAngles[1]
            print ("Top IMU angle is",Top_IMU.eulerAngles[1])
            print ("Bot IMU angle is",Bot_IMU.eulerAngles[1])
        except TypeError:
            pass  # Skip updating angle if None

def printEulerAngle(top_angle):
    time_sleep = 0.0005 #don't change this, for lead screw
    motor = StepperMotor()
    while True:
        try:
            while (top_angle.value >= 2):
                print("EXTEND")
                motor.spin(sleep_time= time_sleep, clockwise=True)
            while (top_angle.value < -2):
                print("RETRACT")
                motor.spin(sleep_time= time_sleep, clockwise=False)
            else:
                print("Flat")
                pass
        except TypeError:
            pass

#Currently not completed, angle just used to move DC motor
def reach(bot_angle):
    DC_motor = DCMotor(In1=17, In2=27, EN=18, Duty=100)
    print ("The angle for DC is",bot_angle.value)
    time.sleep(3)
    while True:
        try:
            if -90 <= bot_angle.value <= -70:
                DC_motor.clockwise(0.5)   # Bring down
                DC_motor.anticlockwise(0.8) #Bring up
                #Just moving, but will stop if limit reached
                print ("Moving")
                print ("Moving")
                print ("Moving")
                print ("Moving")
                print ("Moving")
                print ("Moving")
                print ("Moving")
            else:
                DC_motor.clockwise(0)
                print("NotMoving")
                pass
        
        except KeyboardInterrupt:
            print("Cleaning up GPIO pins")
            DC_motor.stop()
            GPIO.cleanup()

def spin():
    bottom_motor = StepperMotor()
    time_sleep = 0.0005 #don't change this?Ken said so
    step = 1000
    while True:
        try:
            bottom_motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
            time.sleep(2)
            bottom_motor.spin(steps=step, sleep_time= time_sleep, clockwise=False)
            time.sleep(2)
            print("I am spinning")
        except KeyboardInterrupt:
            print ("CLeaning up GPIO pins")
            bottom_motor.stop()
            GPIO.cleanup()


if __name__ == "__main__":
    # Initial Setup
    top_angle = mp.Value('f', 0.0)  # Use 'f' for float type
    bot_angle = mp.Value('f', 0.0)  # Use 'f' for float type

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(top_angle,bot_angle))
    #printProcess = mp.Process(target=printEulerAngle, args=(top_angle,))
    DCProcess = mp.Process(target=reach, args=(bot_angle,))
    BotProcess = mp.Process(target=spin, args=())
    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    #printProcess.daemon = True
    DCProcess.daemon = True
    BotProcess.daemon = True


    # Start the processes
    fetchProcess.start()
    #printProcess.start()
    DCProcess.start()
    BotProcess.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program has terminated")
        GPIO.cleanup()

