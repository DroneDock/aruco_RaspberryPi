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
from camera_class import aruco_cam


import RPi.GPIO as GPIO

def cam(R,theta_degrees):
    
    detect = aruco_cam()
    detect.cam_run(R,theta_degrees)

# Just used to test getting the output from camera
# def out (R,theta_degrees):
#     while True:
#         print ("IT WORKS")
        
#         print ("the R values is",R.value)
#         print ("the theta values is",theta_degrees.value)
#         print ("SOMEHTING")
#         time.sleep(1)
#     #return R,theta

#to put IMU readings into a value
def fetchEulerAngle(yaw_angle,top_angle,bot_angle):
    Top_IMU = AdafruitBNO055() #Top IMU
    Bot_IMU = AdafruitBNO055(ADR=True) #Bottom IMU
    while True:
        try:
            yaw_angle.value = Top_IMU.eulerAngles[0] #Getting Yaw for camera
            top_angle.value = Top_IMU.eulerAngles[1] #Using roll for balancing
            bot_angle.value = Bot_IMU.eulerAngles[1] #Bottom IMU for reach limit
            #print ("Top IMU angle is",Top_IMU.eulerAngles)
            #print ("Bot IMU angle is",Bot_IMU.eulerAngles[1])
        except TypeError:
            pass  # Skip updating angle if None

def printEulerAngle(top_angle):
    time_sleep = 0.0005 #don't change this, for lead screw
    motor = StepperMotor()
    # TO balance the top platform
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
def reach(bot_angle,R):
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
                print ("Should STOP") # Doesnt work...
                pass
        
        except KeyboardInterrupt:
            print("Cleaning up GPIO pins")
            DC_motor.stop()
            GPIO.cleanup()

#Just spinning bottom motor with no inputs yet
def spin(yaw_angle,theta_degrees):
    bottom_motor = StepperMotor()
    time_sleep = 0.0005 #don't change this?Ken said so
    step = 50
    while True:
        calculated = 270 - theta_degrees.value
        diff = yaw_angle.value - calculated
        try:
            print ("Yaw is ",yaw_angle.value)
            print ("Theta is ", theta_degrees.value)
            if 30 > yaw_angle.value >-30:

                print ("The diff is",diff)
                if diff < 0:
                    bottom_motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
                    print ("I'm moving clockwise")
                elif diff > 0:
                    bottom_motor.spin(steps= step, sleep_time= time_sleep, clockwise=False)
                    print ("I'm moving anticlockwise")
            elif yaw_angle.value > 30:
                bottom_motor.spin(steps= step, sleep_time= time_sleep, clockwise=False)
            elif yaw_angle.value <-30:
                bottom_motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)

            else:
                print("STOP LIMIT REACHED")
                pass
        
        except KeyboardInterrupt:
            print ("CLeaning up GPIO pins")
            bottom_motor.stop()
            GPIO.cleanup()



if __name__ == "__main__":
    time.sleep(3)
    # Initial Setup
    yaw_angle = mp.Value('f', 0.0)  # Use 'f' for float type
    top_angle = mp.Value('f', 0.0)  # Use 'f' for float type
    bot_angle = mp.Value('f', 0.0)  # Use 'f' for float type
    R = mp.Value('f', 0.0)  # Use 'f' for float type
    theta_degrees = mp.Value('f', 0.0)  # Use 'f' for float type

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(yaw_angle,top_angle,bot_angle))
    #printProcess = mp.Process(target=printEulerAngle, args=(top_angle,))
    #DCProcess = mp.Process(target=reach, args=(bot_angle,))
    BotProcess = mp.Process(target=spin, args=(yaw_angle,theta_degrees))
    CameraProcess = mp.Process(target=cam, args=(R,theta_degrees))
    
    #For testing
    #OutProcess = mp.Process(target=out, args=(R,theta_degrees))

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    #printProcess.daemon = True
    #DCProcess.daemon = True
    BotProcess.daemon = True
    CameraProcess.daemon = True
    
    #For testing
    #OutProcess.daemon = True



    # Start the processes
    fetchProcess.start()
    #printProcess.start()
    #DCProcess.start()
    BotProcess.start()
    CameraProcess.start()

    #For testing
    #OutProcess.start()

    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program has terminated")
        GPIO.cleanup()

