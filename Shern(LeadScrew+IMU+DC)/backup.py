"""
Not used, using queue method.
"""


import time
import multiprocessing as mp
from multiprocessing import Queue
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from multiprocessing import Lock

# Project Specific Imports
from back.Leadscrew import StepperMotor
from back.ShernIMU import AdafruitBNO055
from back.PID_Tuner import PIDController

# Pin Definition using BCM numbering system -----------------------------------
#For DC motor
Motor1In1 = 17
Motor1In2 = 27
Motor1EN  = 18   # PWM Pin on Raspberry PI

  # Initialize GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor1In1, GPIO.OUT)
GPIO.setup(Motor1In2, GPIO.OUT)
GPIO.setup(Motor1EN, GPIO.OUT)

p = GPIO.PWM(Motor1EN, 2000)  # Set PWM frequency (in Hz)

# Constants for PID controller (to be tuned)
kp = 10
ki = kp *(0.001)
kd = kp *(0.000000001)
#PID limits
upper_bound = 500
lower_bound = 0
# Setpoint for the PID controller (desired angle)
setpoint = 0.0

# Constants for PWM control
DutyCycleUp = 80 # Initial duty cycle for going up
DutyCycledown = 40  # Initial duty cycle for going up

# Initialize PID controller
pid_controller = PIDController(kp, ki, kd, setpoint,upper_bound,lower_bound)

lead_screw_pitch = 8 #mm
time_sleep = 0.0000001 #don't change this

step_stop = 0 #to stop the motor

#to plot graph of PID tuning
angle_values = []
time_values = []
setpoint_values = []
lock = Lock()

#to put IMU readings into a queue
def fetchEulerAngle(queue: Queue):

    IMU = AdafruitBNO055()

    while True:
        # To prevent overfilling the queue
        if queue.qsize() < 50:
            queue.put(IMU.eulerAngles[1])
        else:
            print("Queue is full. Waiting...")
        # Manual delay (to be removed later)
        #time.sleep(0.005)
        #time.sleep

def printDC(queue: Queue):
    while True:
        for _ in range(15):  # Assuming you want to run the motor 5 times            
            try:
                p.start(DutyCycleUp)
                GPIO.output(Motor1In1, GPIO.HIGH) # High
                GPIO.output(Motor1In2, GPIO.LOW)
                time.sleep(0.1)
                p.stop()
                time.sleep(1)
                print("MovingUp")
            except TypeError:
                pass


        for _ in range(15):  # Assuming you want to run the motor 5 times
            # One direction movement, clockwise (up)
            try:
                print("vrfyadsmokcvjs")
                p.start(DutyCycledown)
                GPIO.output(Motor1In1, GPIO.LOW)
                GPIO.output(Motor1In2, GPIO.HIGH) # High
                time.sleep(0.1)
                p.stop()
                time.sleep(1)
                print("Moving down")
            except TypeError:
                pass

def printEulerAngle(queue: Queue):

    motor = StepperMotor()
    start_time = time.time()  # Record start time
    while True:
        if not queue.empty():
            angle = queue.get()
            #step = pid_controller.calculate(angle)#output step size
            # with lock: #to keep the values clean
            #     angle_values.append(angle)
            #     time_values.append(time.time())  # current time
            #     setpoint_values.append(pid_controller.setpoint)  # setpoint value
            try:
                while (angle>= 1):
                    print("EXTEND")
                    motor.spin(sleep_time= time_sleep, clockwise=True)
                    print(f"The step is Running")
                    angle = queue.get()
                    #print(angle)
                else:
                    print("bye bye")
                    pass
                
                while (angle <= -1):
                    print("RETRACT")
                    motor.spin(sleep_time= time_sleep, clockwise=False)
                    print(f"The step is Reversing")
                    angle = queue.get()
                    #print(angle)
                else:
                    angle = queue.get()
                    pass
            except TypeError:
                pass
            # Sometimes angle is None, so put in try block to resolve
            # try:
            #     if (angle > 0):
            #         print("EXTEND")
            #         motor.spin(motor, sleep_time= time_sleep, clockwise=True)
            #         print(f"The step is Running")
            #         #time.sleep(0.5)
                    
            #     elif (angle < 0):
            #         print("RETRACT")
            #         motor.spin(motor, sleep_time= time_sleep, clockwise=False)
            #         print(f"The step is Running")
            #         #time.sleep(0.5)
                    
            # except TypeError:
            #     pass
            # # Update plot periodically
            # plt.clf()
            # # First few points are ommited
            # plt.plot(time_values[2:], angle_values[2:], '-o', color='red', label='Angle')
            # plt.plot(time_values[2:], setpoint_values[2:], '--', color='blue', label='Setpoint')
            # plt.xlabel('Time')
            # plt.ylabel('Angle')
            # plt.legend()
            # plt.title('Real-Time Angle Response')
            # plt.pause(0.001)  # Pause to allow the plot to update
            # plt.savefig('PIDLSDCtuning.png')     

        else:
            print("Waiting for data")
            #motor.spin(sleep_time= time_sleep, clockwise=True)
            #time.sleep(1)

        end_time = time.time()  # Record end time
        execution_time = end_time - start_time  # Calculate execution time
        #print(f"Execution time: {execution_time} seconds")        
# Manual delay (to be removed later)
            
if __name__ == "__main__":
    #time.sleep(3)

    # Initial Setup
    dataQueue = Queue()
   #print (dataQueue) #doesn't actually print Queue, why?

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(dataQueue,))
    printProcess = mp.Process(target=printEulerAngle, args=(dataQueue,))
    DCrotationProcess = mp.Process(target=printDC, args=(dataQueue,))

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    printProcess.daemon = True
    DCrotationProcess.daemon = True

    # Start the processes
    #DCrotationProcess.start()
    fetchProcess.start()
    printProcess.start()
    
    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
            #time.sleep(0.5)

    except KeyboardInterrupt:
        print("Program has terminated")
