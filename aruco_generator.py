"""

This script generates the ArUco tags and store them as PNG files within directories of the same ArUco dictionary.

Created by: Jalen
"""

import sys
import argparse
from pathlib import Path
import numpy as np
import cv2
from arucoDict import ARUCO_DICT


# ARGUMENTS -----------------------------------------------------------------------------------------------------------
arg = argparse.ArgumentParser()
arg.add_argument("-t", "--type", type=str, default="DICT_6X6_50", help="type of ArUco marker to generate")
args = vars(arg.parse_args())  # Convert argument to dictionary


# CHECK IF DICTIONARY EXISTS -------------------------------------------------------------------------------------------
if ARUCO_DICT.get(args["type"], None) is None:
    print(f"ArUco tag type {args['type']} is not supported.")
    sys.exit(0)
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])


# SAVE IMAGE -----------------------------------------------------------------------------------------------------------
# Save all possible IDs for the specified dictionary within the same directory

# Create a folder to store markers if not already
folder_path = Path(Path(__file__).parent, "aruco_tags", args["type"]).resolve()
folder_path.mkdir(parents=True, exist_ok=True)

# Save each marker by looping over its ID
for marker_id in range(len(arucoDict.bytesList)):

    # Save ArUco tag as an array called "tag". (P.S. ArUco is a binary image)
    tag = np.zeros((300, 300, 1), dtype="uint8")
    cv2.aruco.drawMarker(dictionary=arucoDict,
                         id=marker_id,
                         sidePixels=300,
                         img=tag,
                         borderBits=1)

    # Save the marker as a file within a folder corresponding to its dictionary
    file_path = Path(folder_path, f"ID_{marker_id}").resolve()
    cv2.imwrite(str(file_path) + ".png", img=tag)

print("All images saved.")
