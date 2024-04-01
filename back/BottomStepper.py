"""
Latest for motor driver TB6600 for bottom stepper motor
26/3
"""
import RPi.GPIO as GPIO
import time

# Pin Definitions





class StepperMotor(object):
    def __init__(self, steps_per_revolution = 200, ena_pin: int =23, dir_pin: int = 24, pul_pin: int = 25):
                
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        self.steps_per_revolution = steps_per_revolution
        
        GPIO.setmode(GPIO.BCM)

        # Configure Pins
        GPIO.setup(ena_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(pul_pin, GPIO.OUT)
        
        #Current position of lead screw (in steps)
        self.current_postion = 0


    
    def spin(self, steps, sleep_time, clockwise=True):
        """
        dirPin = High for clockwise
        """
        GPIO.output(self.ena_pin, GPIO.HIGH)  # Enable motor driver
        GPIO.output(self.dir_pin, GPIO.HIGH if clockwise else GPIO.LOW)  # Set motor direction

        # Spin motor
        for _ in range(steps):
            GPIO.output(self.pul_pin, GPIO.HIGH)
            time.sleep(sleep_time)  # Delay in seconds
            GPIO.output(self.pul_pin, GPIO.LOW)
            time.sleep(sleep_time)  # Delay in seconds
        
        GPIO.output(self.ena_pin, GPIO.LOW)  # Disable motor driver after spinning

    def stop(self) -> None:
            GPIO.output(self.pul_pin, GPIO.LOW)
            time.sleep(0.005)  # Delay in seconds
            GPIO.output(self.pul_pin, GPIO.HIGH)
            time.sleep(0.005)  # Delay in seconds

    # def spin(self, steps ,sleep_time,clockwise=True ):

    #     """
    #     dirPin = High for clockwise
    #     """
    #     GPIO.output(self.ena_pin, GPIO.HIGH)
    #     GPIO.output(self.dir_pin, GPIO.HIGH if clockwise else GPIO.LOW)
    #     # Set motor direction
        
    #     #GPIO.output(self.ena_pin, GPIO.HIGH)
    #     # Spin motor
    #     for _ in range(steps):
    #         GPIO.output(self.pul_pin, GPIO.HIGH)
    #         time.sleep(sleep_time)  # Delay in seconds
    #         GPIO.output(self.pul_pin, GPIO.LOW)
    #         time.sleep(sleep_time)  # Delay in seconds
    #     GPIO.output(self.ena_pin, GPIO.LOW)
                
            
           