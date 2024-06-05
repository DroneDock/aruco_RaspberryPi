# aruco_RaspberryPi
Full documentation/code on detecting ArUco markers and pose estimate their positions via Picamera Module V2 connected to Raspberry Pi

### Project Structure
The main folders/files of the project are shown
```
|
|----- 📁 aruco_tags/DICT_6x6_50
|
|----- 📁 camera_calibration_final
|       |----- 🐍 test_rpicamera.py
|       |----- 🐍 aruco_board_generation.py
|       |----- 🐍 data_generation.py
|       |----- 🐍 camera_calibration.py
|       |----- 🐍 real_time_validation.py
|       |----- 📁 aruco_calibration_data
|       |----- ...
|
|----- 🐍 arucoDict.py
|
|----- 🐍 aruco_detector_video.py
|
|----- 🐍 aruco_generator.py
|
|----- 🐍 pose estimation.py
|
```
* 📁 **aruco_tags/DICT_6x6_50** - Contains all the aruco tags of the specific aruco dictionary 6x6_50. In this project, we will be using aruco ID 25.
* 📁 **camera_calibration_final** - Contains all the files to run camera calibration via the ArUco board approach. These files are arranged sequentially, where a simple test of the camera should be conducted with 'test_rpicamera.py, followed by generating the aruco board --> generating data --> calibrating the camera --> validating it.
* 🐍 **arucoDict.py** - Dictionary for aruco markers. In this project, we will be using the 6x6_50 dictionary.
* 🐍 **aruco_detector_video.py** - Performs a quick real-time detection of the aruco marker using the camera. It only annotates the marker upon detected, but does not carry out pose estimation.
* 🐍 **aruco_generator.py** - Generates the aruco tags and store them as PNG files within directories of the same ArUco dictionary - aruco_tags/DICT_6x6_50
* 🐍 **pose estimation.py** - Detects the ArUco marker and pose estimate the translational (cartesian & polar coordinates) and rotational vectors of the marker respective to the camera.
* 📁 **docs** - Contain the documentations for properly setting up OpenCV within Raspberry Pi and Jetson Nano. It includes solutions for common issues, such as compatibility between OpenCV, Python, and the camera module.

## Setup
### Configuring Virtual Environment
To setup the python environment for the Raspberry Pi Model 4 (main board for 
this project), **python 3.9.4** is used due to dependency limitations of the 
ArUco detection code. Since the default python version for the Pi 4 is version
3.11.2, we can change the environment with the **pyenv** program. The tutorial
on how to use this is shown in [this youtube video](https://www.youtube.com/watch?v=QdlopCUuXxw&t=6s).

The required packages are listed in *requirements.txt*.

Run the following code:
```code
pip install -r requirements.txt
```

## Running the program
To run the program of pose estimation, simply run the following command in the project root:
```code
python pose_estimation.py
```



