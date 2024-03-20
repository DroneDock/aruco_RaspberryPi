# Standard Imports
import time
import os
from pathlib import Path
import csv

# Third-Party Imports
import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
import yaml

# Project-Specific Imports
from aruco_calibration_data.arucoDict import ARUCO_DICT

# Load camera calibration data
def load_calibration_data():
    with open('calibration.yaml') as f:
        loadeddict = yaml.load(f, Loader=yaml.FullLoader)
    mtx = loadeddict.get('camera_matrix')
    dist = loadeddict.get('dist_coeff')
    mtx = np.array(mtx)
    dist = np.array(dist)
    return mtx, dist

# Definitions
MARKER_SIZE = 80
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_6X6_50"])
arucoParams = cv2.aruco.DetectorParameters_create()

# Load camera calibration data
camMatrix, distCof = load_calibration_data()

# Create VideoStream object
vs = VideoStream().start()
time.sleep(2)  # Allow camera to warm up

last_print_time = time.time()

while True:
    frame = vs.read()
    frame = cv2.resize(frame, (700, 600))

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = cv2.aruco.detectMarkers(image=gray_frame, dictionary=arucoDict, parameters=arucoParams)

    # If checkerboard is detected
    if corners:
        rVec, tVec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners=corners, markerLength=MARKER_SIZE, cameraMatrix=camMatrix, distCoeffs=distCof
        )

        total_markers = range(0, ids.size)

        # Polylines - draw for every marker on screen

        for markerID, corner, i in zip(ids, corners, total_markers):

            topLeft, topRight, btmRight, btmLeft = corner.reshape((4, 2))
            
            # Calculate center of the ArUco marker
            marker_center = np.mean([topLeft, btmRight], axis=0)

            cv2.polylines(
                frame, [corner.astype(np.int32)], isClosed=True, color=(0, 255, 255), thickness=4, lineType=cv2.LINE_AA
            )

            # Calculate relative distance from the camera center
            camera_center_x, camera_center_y = camMatrix[0, 2], camMatrix[1, 2]
            relative_distance_x = camera_center_x - marker_center[0]
            relative_distance_y = camera_center_y - marker_center[1]
            relative_distance_z = tVec[i][0][2]  # Z-direction is already in camera coordinate system

            # Draw a cross-mark at the center of the frame
            cv2.drawMarker(frame, (int(camera_center_x), int(camera_center_y)), color=(0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)


            # Print relative distance values every 2 second
            current_time = time.time()
            if current_time - last_print_time >= 2.0:
                print(f"Marker ID: {markerID}")
                print(f"Relative Distance (x): {-(relative_distance_x)} mm")        # rightwards = +ve
                print(f"Relative Distance (y): {relative_distance_y} mm")           # upwards = +ve
                print(f"Relative Distance (z): {relative_distance_z} mm")
                print("-----------------------------")
                last_print_time = current_time

            # Annotate Pose
            cv2.drawFrameAxes(frame, camMatrix, distCof, rVec[i], tVec[i], length=4, thickness=4)

    cv2.imshow("Coloured Frame", frame)

    # Terminate program and cleanup when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
vs.stop()


