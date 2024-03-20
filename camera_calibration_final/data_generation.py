"""
CAMERA CALIBRATION PART (B) 

This script generates data in the form of images.
Prior to running this script, we will need to print the ArUco board as detailed in 'aruco_board_generation.py'.

    1) Provide desired path to store images.
    2) Press 'c' to capture image and display it.
        a) Capture the ArUco board from various angles for better calibration purposes.
    3) Press any button to continue.
    4) Press 'q' to quit.

Quick note regarding the main difference between Jetson Nano & Raspberry Pi, to initialize the camera:
    - The IMX camera module, connected to a Jetson Nano uses the imutils video stream function
    - The Raspberry Pi (RPI) V2 camera module uses the picamera library

Created by: Jalen
"""

# RASPBERRY PI -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

# Initialize the PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180

# Initialize the video stream
raw_capture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(2)

# Define an OpenCV window to display video
cv2.namedWindow("Frame")

# Path to store images
path = "/home/gdp49/Codes/aruco_markers/aruco_pose/camera_calibration_final/aruco_calibration_data/"

count = 0

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    name = path + str(count) + ".jpg"

    # Display the frame
    cv2.imshow("Frame", image)

    # Save the frame when 'c' key is pressed
    if cv2.waitKey(20) & 0xFF == ord('c'):
        cv2.imwrite(name, image)
        cv2.imshow("Frame", image)
        count += 1

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Clear the stream for the next frame
    raw_capture.truncate(0)

# Release resources
cv2.destroyAllWindows()

