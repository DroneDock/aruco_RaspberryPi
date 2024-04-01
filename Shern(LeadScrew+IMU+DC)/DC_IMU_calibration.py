"""
Test Code for calibration, not running
For getting the angles of IMU while DC motor is turning
Not done yet
Managed to get the graphs as shown...in Angle_graphs
"""
import time
import multiprocessing as mp
# Project Specific Imports
from back.ShernIMU import AdafruitBNO055
from back.DCMotor import DCMotor
from back.IMU_Plots import graph #change this to graph for plotting all 3 angles


#to put IMU readings into a queue
def fetchEulerAngle(timing,yaw,roll,pitch):
    IMU_2 = AdafruitBNO055(ADR=True)
    start_time = time.time()  # Record start time

    # prev_prev_roll_value = None  # Store the roll value from two iterations ago
    # prev_roll_value = None  # Store the previous roll value
    while True:
        try:
            timing.value = time.time() - start_time
            yaw_value, roll_value, pitch_value = IMU_2.eulerAngles
            
            # # Check for anomaly in roll value
            # if prev_prev_roll_value is not None and prev_roll_value is not None:
            #     prev_roll_diff = abs(prev_roll_value - prev_prev_roll_value)
            #     current_roll_diff = abs(roll_interim - prev_roll_value)
            #     print("The current roll is",roll_interim)
            #     print ("The current diff is",current_roll_diff)
            #     print ("The prev roll diff is",prev_roll_diff)
            #     if current_roll_diff > 30 + prev_roll_diff:
            #         print(f"Anomaly detected in roll value: Previous={prev_roll_value}, Current={roll_interim}")
            #         # Handle anomaly here, such as logging, alerting, or corrective action
            #         pass
            #     else:
            #         roll.value = roll_interim
            # # Update previous roll values
            # prev_prev_roll_value = prev_roll_value
            # print("The prev prev is",prev_prev_roll_value)
            # print("the prev value",prev_roll_value)
            # prev_roll_value = roll_interim

            # Update shared memory values
            yaw.value = yaw_value
            roll.value = roll_value
            pitch.value = pitch_value
            
            #print(f"The yaw angle is {yaw.value}, the roll angle is {roll.value}, and the pitch angle is {pitch.value}.")

        except TypeError:
            pass  # Skip updating angle if None


def printEulerAngle(timing,yaw,roll,pitch):

    plots = graph()

    while True:
        # Sometimes angle is None, so put in try block to resolve
        try:
            #Used to plot 3 seperate graphs of each angles
            #plots.graph(timing.value,yaw.value,roll.value,pitch.value)
            plots.graph_singular(timing.value,roll.value)
            print("The angle is",roll.value)

        except TypeError:
            pass  


def dcmotor(roll):
    DC_motor = DCMotor(In1=17, In2=27, EN=18, Duty=100)

    # Check if command-line arguments are provided
    while True:
        try:
            # if roll.value<5 or roll.value <-85:
            #     DC_motor.stop()

            # else:
            print("Going clockwise")
            DC_motor.clockwise(0)
            DC_motor.stop()
            time.sleep(5)
            print("Going anticlockwise")
            DC_motor.anticlockwise(0.5)
            DC_motor.stop()
            time.sleep(5)
            print ("Stop")
            DC_motor.stop()
            
        except TypeError:
            pass  

if __name__ == "__main__":
    #Initial setup
    time.sleep(3)
    timing = mp.Value('f', 0.0)  
    yaw = mp.Value('f', 0.0)  
    roll = mp.Value('f', 0.0)  
    pitch = mp.Value('f', 0.0) 

    # Initiate processes
    fetchProcess = mp.Process(target=fetchEulerAngle, args=(timing,yaw,roll,pitch))
    printProcess = mp.Process(target=printEulerAngle, args=(timing,yaw,roll,pitch))
    DCrotationProcess = mp.Process(target=dcmotor, args=(roll,))

    # Set processes as daemon which are automatically killed when the main
    # process ends, simplifying cleanup
    fetchProcess.daemon = True
    printProcess.daemon = True
    DCrotationProcess.daemon = True

    # Start the processes
    DCrotationProcess.start()
    fetchProcess.start()
    printProcess.start()
    
    # Wait indefinitely until program is terminated
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program has terminated")

