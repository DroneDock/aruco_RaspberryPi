"""
For importing IMU class
Technically same as original, but some constraints are 
added when error appears.
"""
# Standard Imports
import math
from typing import Tuple

# Third Party Imports
import numpy as np
import board
import busio
import adafruit_bno055

class AdafruitBNO055(object):
    """
    Establish an IMU class for the 9-axis Adafruit BNO055 IMU, capable of 
    returning 3-axis acceleration, 3-axis angular velocity, 3-axis magnetic
    field and temperature, along with further derived values such as 
    angles, quarternions, etc.

    The update rate of sensor is 100Hz. 

    V_in to 3.3V
    SDA to GPIO 2
    SCL to GPIO 3

    Attributes
    ----------
    """
    # Use V_in instead of 3V3, 

    def __init__(self, ADR: bool = False):
        """
        Initialize the AdafruitBNO055 class. Set ADR to True if the ADR pin
        of the BNO055 is set to HIGH (this must be done if a second BNO055 is 
        used along with the first)
        """
        i2c = busio.I2C(board.SCL, board.SDA)  # Initialize I2C connection
        
        if not ADR:  # Default address
            self._sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x28)
        else:        # When ADR is set HIGH
            self._sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

        print("Ideally, move the sensor in a figure 8 pattern twice to calibrate it")

    @property
    def temperature(self) -> float:
        """
        Return the temperature measured by the IMU.
        """
        return self._sensor.temperature

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """
        Return the 3-axis acceleration [m/s^2] measured by the IMU as a 
        tuple.
        """
        return self._sensor.acceleration
    
    @property
    def angularVelocity(self) -> Tuple[float, float, float]:
        """
        Return the 3-axis angular velocity [m/s] measured by the IMU as a 
        tuple.
        """
        return self._sensor.gyro

    def euler(self, wrap=False) -> Tuple[float, float, float]:
        """
        Get the Euler angle straight from the IMU as a tuple (yaw, roll, pitch)

        Note: This is not used in favour of eulerAngles which calculate the
        angles using quaternions.
        """
        return self._sensor.euler

    def _quaternion_to_euler(self, qw, qx, qy, qz):
        """
        Convert quarternions to euler angles in radians as a tuple of
        rotation around (x, y, z) axes.
        """
        if qw is None or qx is None or qy is None or qz is None:
            return None, None, None  # Return None if any quaternion component is None

        x_rot_rad = math.atan2(2*(qw*qx+qy*qz), 1-2*(qx*qx+qy*qy))
        y_rot_rad = 2*math.atan2(1+2*(qw*qy-qx*qz), 1-2*(qw*qy-qx*qz)) - math.pi/2
        z_rot_rad = math.atan2(2*(qw*qz+qx*qy), 1-2*(qy*qy+qz*qz))

        # Changes in signs for compensation (Yaw and pitch needs *-1)
        # Roll is only limited to +- 90 deg
        return x_rot_rad, y_rot_rad, z_rot_rad

    @property
    def eulerAngles(self) -> Tuple[float, float, float]:
        """
        Returns a tuple of (yaw, roll, pitch) of the IMU in degrees, calculate
        via quaternions to prevent gimbal lock.

        Yaw   - Positive clockwise  [-180, +180]
        Roll  - Positive right-down [- 90, + 90]
        Pitch - Positive nose-up    [-180, +180]

        This implementation is specific to the Adafruit BNO055 sensor, which
        defines pitch, roll, yaw as the x, y and z axes rotations respectively.

        Note: Move the IMU in a figure 8 pattern to calibrate the yaw in the 
        magnetic north direction. 
        """
        # For the BNO055, the yaw, roll, pitch are the x, y and z axis 
        # rotations respectively 
        pitch, roll, yaw = self._quaternion_to_euler(*self._sensor.quaternion)
        if pitch is None or roll is None or yaw is None:
            return None, None, None  # Return None if any quaternion component is None

        # Some are multipled by -1 to make direction consistent
        pitch = pitch * 180/math.pi * -1
        roll  = roll  * 180/math.pi * -1
        yaw   = yaw   * 180/math.pi * -1
        
        return yaw, roll, pitch
