"""
This script perform a quick real-time detection of the ArUco marker using the camera. Note that this script only annotates the marker upon detected, but does not carry out pose estimation.

Created by: Jalen
"""
# Standard Imports
import time

# Third-Party Imports
import cv2
import imutils
from imutils.video import VideoStream

# Project-Specific Imports
from arucoDict import ARUCO_DICT
from aruco_detector import annotate_tags


# DEFINE ARUCO DICTIONARY AND DETECTION PARAMETER ----------------------------------------------------------------------
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_6X6_50"])  # Define what type of aruco markers to look for
arucoParams = cv2.aruco.DetectorParameters_create()              # Use default parameters


# DETECT IMAGE IN VIDEO ------------------------------------------------------------------------------------------------
# Initialize the PiCamera
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)  # Set camera resolution
    camera.framerate = 32  # Set camera framerate
    time.sleep(2)  # Allow camera to warm up

    # Loop over frames from video stream
    for _ in camera.capture_continuous(picamera.array.PiRGBArray(camera)):
        frame = camera.array

        # Resize the frame
        frame = cv2.resize(frame, (1000, 1000))

        # Detect markers in the current frame
        start_time = time.time()
        corners, ids, rejected = cv2.aruco.detectMarkers(image=frame,
                                                          dictionary=arucoDict,
                                                          parameters=arucoParams)

        detection_time = time.time() - start_time
        print(f"Detection takes {detection_time * 1000} ms")

        # If at least one marker is detected
        if len(corners) > 0:
            # Print analytics
            ids = ids.flatten()
            print(f"Within the image of size {frame.shape}:")
            print(f"    {len(ids)} tags are detected, with IDs {ids}.")
            print(f"    {len(rejected)} tags are rejected.")

            for markerCorners, markerID in zip(corners, ids):
                # Corner are always in the order: top-left, top-right, bottom-right, bottom-left
                topLeft, topRight, btmRight, btmLeft = markerCorners.reshape((4, 2))

                # Convert the coordinates to integers to be used by OpenCV
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                topRight = (int(topRight[0]), int(topRight[1]))
                btmRight = (int(btmRight[0]), int(btmRight[1]))
                btmLeft = (int(btmLeft[0]), int(btmLeft[1]))

                # Draw information onto the frame
                annotate_tags(frame, markerID, topLeft, topRight, btmRight, btmLeft)

            cv2.imshow("frame", frame)
            key = cv2.waitKey(1) & 0xFF  # Waits for a key event for 1ms, extract the least significant 8 bits of results

            # Break the loop if the key 'q' is pressed
            if key == ord('q'):
                break

    # Cleanup
    cv2.destroyAllWindows()
