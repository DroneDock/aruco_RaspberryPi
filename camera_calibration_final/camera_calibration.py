"""
CAMERA CALIBRATION PART (C)

This script performs camera calibration using ArUco markers on a board. Here are a few steps to follow prior to running this script:
    a) Preparing the resources for camera calibration as carried out in 'aruco_board_generation.py' and 'data_generation.py'.
        1) Print the aruco marker board of DICT_6x6_50
        2) Take around 50 images of the printed board pasted on a flat card-board, from different angles.
        3) Set path to store images first

    b) Calibrating Camera
        1) Measure length of the side of individual marker and spacing between two marker
        2) Input above data (length and spacing) in "camera_calibration.py"
        3) Set path to stored images of aruco marker

There are in total two functions of this code:
    a) Camera Calibration (if calibrate_camera is True):
        - The camera matrix and distortion coefficients will be calculated and stored in the YAML file.

    b) Real-time Validation (if calibrate_camera is False)
        - The real-time validation assumes a calibration has been performed and the calibration data is stored in calibration.yaml. 
        - The pose of the ArUco marker board is estimated, and the result is visualized with markers and coordinate axes.
        - This validation piece of code still has issues, hence a separate 'pose_estimation.py' code has been constructed to carry out similar purposes.

Created by: Jalen
"""

# Imports
import time
import cv2
from cv2 import aruco
import yaml
import numpy as np
from pathlib import Path
from tqdm import tqdm
import picamera
import picamera.array


# Root directory of repo for relative path specification.
root = Path(__file__).parent.absolute()

# Set this flsg True for calibrating camera and False for validating results real time
calibrate_camera = True

# Set path to the images
calib_imgs_path = root.joinpath("aruco_calibration_data")



# DEFINING ARUCO BOARD PARAMETERS ----------------------------------------------------------------------------------------------------------
# For validating results, show aruco board to camera.
aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_6X6_50 )

#Provide length of the marker's side
markerLength = 3.50  # Here, measurement unit is centimetre.

# Provide separation between markers
markerSeparation = 0.5   # Here, measurement unit is centimetre.

# create arUco board
board = aruco.GridBoard_create(4, 5, markerLength, markerSeparation, aruco_dict)


'''uncomment following block to draw and show the board'''
# img = board.draw((864,1080))
# cv2.imshow("aruco", img)

arucoParams = aruco.DetectorParameters_create()



# CAMERA CALIBRATION ----------------------------------------------------------------------------------------------------------
# To generate the camera matrix and distortion coefficients
if calibrate_camera == True:
    img_list = []
    calib_fnms = calib_imgs_path.glob('*.jpg')
    print('Using ...', end='')
    for idx, fn in enumerate(calib_fnms):
        print(idx, '', end='')
        img = cv2.imread( str(root.joinpath(fn) ))
        img_list.append( img )
        h, w, c = img.shape
    print('Calibration images')

    counter, corners_list, id_list = [], [], []
    first = True
    for im in tqdm(img_list):
        img_gray = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=arucoParams)
        if first == True:
            corners_list = corners
            id_list = ids
            first = False
        else:
            corners_list = np.vstack((corners_list, corners))
            id_list = np.vstack((id_list,ids))
        counter.append(len(ids))
    print('Found {} unique markers'.format(np.unique(ids)))

    counter = np.array(counter)
    print ("Calibrating camera .... Please wait...")
    #mat = np.zeros((3,3), float)
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners_list, id_list, counter, board, img_gray.shape, None, None )

    # Save the camera matrix and distortion coefficients to a YAML file (calibration.yaml).
    print("Camera matrix is \n", mtx, "\n And is stored in calibration.yaml file along with distortion coefficients : \n", dist)
    data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
    with open("calibration.yaml", "w") as f:
        yaml.dump(data, f)




# REAL TIME VALIDATION (TRIAL 1) ----------------------------------------------------------------------------------------------------------
else:

    # Load the camera matrix and distortion coefficients from YAML file
    with open('calibration.yaml') as f:
        loadeddict = yaml.load(f, Loader=yaml.FullLoader)
    mtx = loadeddict.get('camera_matrix')
    dist = loadeddict.get('dist_coeff')
    mtx = np.array(mtx)
    dist = np.array(dist)

    with picamera.PiCamera() as camera:
    time.sleep(2)  # Allow camera to warm up
    camera.resolution = (500, 500)  # Set camera resolution
    camera.framerate = 30  # Set camera framerate

        last_print_time = time.time()

        # Capture frames continuously
        for frame in camera.capture_continuous(picamera.array.PiRGBArray(camera)):
            img = frame.array
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            h, w = img_gray.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

            img_aruco = img

            # Undistort image
            dst = cv2.undistort(img_gray, mtx, dist, None, newcameramtx)
            corners, ids, _ = aruco.detectMarkers(dst, aruco.getPredefinedDictionary(aruco.DICT_6X6_250))

            if corners is not None:
                # Estimate pose
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 60, newcameramtx, dist)

                # Draw axis and markers
                img_aruco = aruco.drawDetectedMarkers(img_aruco, corners, ids, (0, 255, 0))
                for i in range(len(ids)):
                    img_aruco = aruco.drawAxis(img_aruco, newcameramtx, dist, rvec[i], tvec[i], 100)

                # Print relative distance values every 2 seconds
                current_time = time.time()
                if current_time - last_print_time >= 2.0:
                    for i in range(len(ids)):
                        print(f"Marker ID: {ids[i]}")
                        print(f"Translation Vector (tvec): {tvec[i]} mm")
                        print("-----------------------------")
                    last_print_time = current_time

            cv2.imshow("World co-ordinate frame axes", img_aruco)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()



# REAL TIME VALIDATION (TRIAL 2) ----------------------------------------------------------------------------------------------------------
else:
    with picamera.PiCamera() as camera:
    camera.resolution = (500, 500)  # Set camera resolution
    camera.framerate = 30  # Set camera framerate
    time.sleep(2)  # Allow camera to warm up

    # Load the camera matrix and distortion coefficients from YAML file
    with open('calibration.yaml') as f:
        loadeddict = yaml.load(f, Loader=yaml.FullLoader)
    mtx = loadeddict.get('camera_matrix')
    dist = loadeddict.get('dist_coeff')
    mtx = np.array(mtx)
    dist = np.array(dist)

    count = 0
    last_print_time = time.time()
    for _ in camera.capture_continuous(picamera.array.PiRGBArray(camera)):
        # Read a frame from the camera
        frame = camera.array

        # Check if the frame is not None
        if frame is not None:
            # Print the shape of the frame for debugging
            print(frame.shape)

            # Detect ArUco markers in undistorted frames
            im_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            h, w = im_gray.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            dst = cv2.undistort(im_gray, mtx, dist, None, newcameramtx)
            corners, ids, rejectedImgPoints = aruco.detectMarkers(dst, aruco_dict)

            if corners is not None:
                # ret, rvec, tvec = aruco.estimatePoseBoard(corners, ids, board, newcameramtx, dist)  # For a board
                ret, rvec, tvec = aruco.estimatePoseBoard(corners, ids, board, newcameramtx, dist, rvec=None, tvec=None)

                if ret != 0:
                    frame = aruco.drawDetectedMarkers(frame, corners, ids, (0, 255, 0))
                    frame = aruco.drawAxis(frame, newcameramtx, dist, rvec, tvec, 10)  # axis length 100 can be changed

                    # Print relative distance values every 2 seconds
                    current_time = time.time()
                    if current_time - last_print_time >= 2.0:
                        print("Rotation:", rvec.flatten())
                        print("Translation:", tvec.flatten())
                        print("-----------------------------")
                        last_print_time = current_time

            # Display the current frame
            cv2.imshow("img", frame)

        # If 'q' key is pressed, exit the loop
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    # Close the OpenCV window
    cv2.destroyAllWindows()