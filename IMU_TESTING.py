"""Run this script to verify readings from the IMU"""

# Standard Imports
import time

# Project-Specific Imports
from back.ShernIMU import AdafruitBNO055

## ========================================================================= ##

if __name__ == '__main__':
    
    IMU_1 = AdafruitBNO055() #Top IMU
    IMU_2 = AdafruitBNO055(ADR=True) #Bottom IMU

    while True:
        print(f"1st IMU Angles (Yaw, Roll, Pitch): {IMU_1.eulerAngles}")
        print(f"2nd IMU Angles (Yaw, Roll, Pitch): {IMU_2.eulerAngles}")
        time.sleep(1)
