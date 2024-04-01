"""
Bottom stepper motor

"""
import time

import RPi.GPIO as GPIO

from back.BottomStepper import StepperMotor
"""

For ref: https://www.instructables.com/Raspberry-Pi-Python-and-a-TB6600-Stepper-Motor-Dri/
Motor driver position T6880
B-: orange
B+: blue
A-: green
A+: yellow

!!!NOTE!!!
Dir Pin set to GPIO20, duplicated with Lead Screw. We need to try with other pins (GPIO24)

-ve dir: 20
-ve ena: 16
-ve pul:22

Progress: Works fine.
Microstepping: 8

Next step is making it react to ArUco
Ken.

"""
#classify steps



time_sleep = 0.0005 #don't change this
step = 1000

if __name__ == "__main__":


    motor = StepperMotor()
    
    while True: 

        key = input('Press W to increase rotate clockwise , press S to rotate anticlockwise: ')

        if key == 'w':
            motor.spin(steps= step, sleep_time= time_sleep, clockwise=True)
            #current_postion_mm = motor.add_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))
            
        elif key == 's':
            motor.spin(steps=step, sleep_time= time_sleep, clockwise=False)
            #current_postion_mm = motor.subtract_position_mm(input_step, lead_screw_pitch)
            #print("'My current position in mm is :", format(current_postion_mm,".2f"))

    
        elif key == 'b':
            motor.stop()
            GPIO.cleanup()
            print("STOP")
            break

        
   
      
  
    GPIO.cleanup()
  
