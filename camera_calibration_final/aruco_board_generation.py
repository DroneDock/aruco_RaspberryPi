"""
CAMERA CALIBRATION PART (A)

This script generates an ArUco board that will need to be printed out physically to be used for camera calibration.
    a) Note that the ArUco boad (multiple ArUco markers on a single board) is used in this case.
    b) Alternative calibration methods, including the following have also been uploaded to GitHub under a separate branch
        - Chessboard Pattern
        - Single ArUco marker
        - CharUco 

Created by: Jalen
"""

# GENERATE ARUCO BOARD IN PDF FORMAT ---------------------------------------------------------------------------------------------------------------------------------
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_6X6_50 )

# Provide length of the marker's side
markerLength = 3.75  # Here, measurement unit is centimetre.

# Provide separation between markers
markerSeparation = 0.5   # Here, measurement unit is centimetre.

# create arUco board
board = aruco.GridBoard_create(4, 5, markerLength, markerSeparation, aruco_dict)

# Uncomment the following block to draw and show the board
img = board.draw((864, 1080))

# Save the image as a PDF
pdf_path = "aruco_board.pdf"
with PdfPages(pdf_path) as pdf:
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.savefig(pdf, format='pdf', bbox_inches='tight')
    plt.close()

print(f"ArUco board image saved as {pdf_path}")


# GENERATE ARUCO BOARD IN PNG FORMAT ---------------------------------------------------------------------------------------------------------------------------------
import cv2
from cv2 import aruco

# Use the large ArUco dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)

# Create a 4x5 ArUco grid board
# Marker length  = 3.75 cm
# Marker separation = 0.5 cm
board = aruco.GridBoard_create(4, 5, 3.75, 0.5, aruco_dict)

# Draw the ArUco board
img = board.draw((864, 1080))  # You can adjust the size here

# Save the image in a format of your choice (e.g., PNG)
image_path = "aruco_board.png"
cv2.imwrite(image_path, img)

print(f"ArUco board image saved as {image_path}")


