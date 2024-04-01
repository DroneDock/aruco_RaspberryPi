"""
Importing DC motor's configurations and running it

"""
# Third Party Imports
import RPi.GPIO as GPIO
import time
class  DCMotor(object):
    """
    DC motor class to control the motor.

    Attributes
    ----------


    Methods
    -------

    """

    def __init__(self, In1: int, In2: int, EN:int,Duty:int, input_mode=GPIO.BCM):
        """Initialize a DC Motor class used to control the motor.

        Args:
            In1 (int): First GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            In2 (int): Second GPIO pin number (BCM) connected to H Bridge of 
            motor driver.

            EN  (int): The ENABLE pin number (BCM) connected to the PWM 
            connection of the motor driver used to control motor speed.
        """
        GPIO.setmode(input_mode)
        # Configure Pins
        self._in1Pin = In1
        self._in2Pin = In2
        self._PWMPin = EN
        self.Duty = Duty #Duty cycle

        GPIO.setup(In1, GPIO.OUT)
        GPIO.setup(In2, GPIO.OUT)
        GPIO.setup(EN, GPIO.OUT)

        # Configure and start PWM
        self._PWM = GPIO.PWM(self._PWMPin, 2000)  # Set PWM frequency as 2000
        self._PWM.start(50)   # Start the PWM instance at zero duty cycle (i.e. static)


    def clockwise(self,duration) -> None:
        """(Public) Rotate the DC motor clockwise at a given duty cycle.

        Args:
            DutyCycle (int, optional): PWM duty cycle supplied to the motor. 
            Defaults to 100.
        """
        
        GPIO.output(self._in1Pin, GPIO.LOW)
        GPIO.output(self._in2Pin, GPIO.HIGH)
        self._PWM.ChangeDutyCycle(self.Duty)
        time.sleep (duration)


    def anticlockwise(self,duration) -> None:
        """(Public) Rotate the DC Motor anticlockwise at a given duty cycle,

        Args:
            DutyCycle (int, optional): PWM duty cycle supplied to the motor.
            Defaults to 100.
        """
        GPIO.output(self._in1Pin, GPIO.HIGH)
        GPIO.output(self._in2Pin, GPIO.LOW)
        self._PWM.ChangeDutyCycle(self.Duty)
        time.sleep (duration)

    def stop(self) -> None:
        """
        (Public) Stop the DC motor from rotating.
        
        Implementation: set the duty cycle to zero.
        """
        self._PWM.ChangeDutyCycle(0)


    def __del__(self):
        """Destructor to cleanup GPIO ports"""
        GPIO.cleanup()
    