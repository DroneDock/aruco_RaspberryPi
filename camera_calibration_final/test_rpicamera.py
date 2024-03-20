"""
This script performs a quick sanity check over the functionability of the RPI camera

Created by: Jalen
"""

# PICAMERA LIBRARY -------------------------------
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(20)
camera.stop_preview()
