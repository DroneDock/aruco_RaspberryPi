"""
This script detects the ArUco marker and pose estimate the translational (cartesian & polar coordinates) and rotational vectors of the marker respective to the camera.
This script can be divided into three sections:
    1) Definitions
        - Define the marker size and dictionary

    2) Load camera data
        - Load the camera matrix and distortion coefficients calculated and stored in the YAML file.

    3) Execution
        - Initialize the camera
        - Detect any ArUco marker present in the camera frame by drawing polylines and frame axes
        - Pose estimate and print out the translational (cartesian & polar coordinates) and rotational values of the marker
        - Annotate the pose for better visualization purposes

Quick note regarding the main difference between Jetson Nano & Raspberry Pi, to initialize the camera:
    - The IMX camera module, connected to a Jetson Nano uses the imutils video stream function
    - The Raspberry Pi (RPI) V2 camera module uses the picamera library

Created by: Jalen

Changes made by Ken: 
- Working in headless mode, commented out cv2.imshow

"""

# Standard Imports
import time
from pathlib import Path
import os

# Third-Party Imports
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import yaml

# Project-Specific Imports
from arucoDict import ARUCO_DICT



# DEFINITIONS ---------------------------------------------------------------------------------------------------------------------------------
# Marker
MARKER_SIZE = 60  # Square size [mm] - allow for pose and distance estimation
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_6X6_50"])
arucoParams = cv2.aruco.DetectorParameters_create()  # Use default parameters



# LOAD CAMERA DATA -----------------------------------------------------------------------------------------------------------------------------
# Load the camera matrix and distortion coefficients from YAML file
with open('camera_calibration_final/calibration.yaml') as f:
    loadeddict = yaml.load(f, Loader=yaml.FullLoader)
camMatrix = loadeddict.get('camera_matrix')
distCof = loadeddict.get('dist_coeff')
camMatrix = np.array(camMatrix)
distCof = np.array(distCof)

print("Loaded calibration data successfully")



# EXECUTION ------------------------------------------------------------------------------------------------------------
# Initialize the picamera
camera = PiCamera()
camera.resolution = (640, 480) #camera resolution here
camera.framerate = 32
camera.rotation = 180 #rotation, depends on the position of the camera
raw_capture = PiRGBArray(camera, size=(640, 480))
time.sleep(2)

last_print_time = time.time()

# # Create a VideoWriter object to save the video
# output_folder = 'Videos'
# os.makedirs(output_folder, exist_ok=True)
# output_path = os.path.join(output_folder, 'test.avi')

# # 10s framerate, 1000x800 resolution
# result = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), 10, (1000, 800))     

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (corners, ids, rejected) = cv2.aruco.detectMarkers(image=gray_frame,
                                                       dictionary=arucoDict,
                                                       parameters=arucoParams)

    # If ArUco marker is detected
    if corners:
        rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners=corners, markerLength=MARKER_SIZE, cameraMatrix=camMatrix, distCoeffs=distCof
        )

        total_markers = range(0, ids.size)

        # Print pose estimation values every 2s for each marker
        current_time = time.time()
        if current_time - last_print_time >= 2.0:
            for markerID, i in zip(ids, total_markers):

                #  Translation vector coordinates
                translation_vector = tVec[i].flatten()
                x, y, z = translation_vector

                # Calculate radius (R)
                R = np.sqrt(x**2 + y**2) #need to make changes here. Potentially remove z
        
                # Calculate polar angle (theta) in radians
                theta = np.arctan2(y, x)  # arctan2 ensures correct usage of four quadrants
        
                # Convert theta to degrees for better readability
                theta_degrees = np.degrees(theta) + 180

                print(f"Marker ID: {markerID}")
                print(f"Translation Vector (Cartesian): {translation_vector} mm")
                print(f"Translation Vector (Polar): R = {R} mm, θ = {theta_degrees} degrees")
                """
                So we're gonna use R and theta_degree here. 
                R will provide input info for DC motor
                Theta will provide input for Bottom stepper rotation

                Probably need to add to queue as well
                """

                print("-----------------------------")

                # print("Translation Vector (tvec):")
                # for value in tVec.flatten():
                #     print(f"    {value}")
                
                # print("Rotation Vector (rvec):")
                # for value in rVec.flatten():
                #     print(f"    {value}")
            
            # For better visualization purposes by separating out every time step of 2 seconds
            print()
            print()
            print()
            last_print_time = current_time

        
        for markerID, corner, i in zip(ids, corners, total_markers):

            topLeft, topRight, btmRight, btmLeft = corner.reshape((4, 2))

            # Draw polylines on marker for better visualization
            cv2.polylines(
                image, [corner.astype(np.int32)], isClosed=True, color=(0, 255, 255), thickness=3, lineType=cv2.LINE_AA
            )

            # Annotate Pose
            cv2.drawFrameAxes(image, camMatrix, distCof, rVec[i], tVec[i], length=50, thickness=3)

    #cv2.imshow("Pose Estimation Frame", image)

    # Terminate program and cleanup when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # Clear the stream for the next frame
    raw_capture.truncate(0)

cv2.destroyAllWindows()
vs.stop()

