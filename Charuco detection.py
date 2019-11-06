# Import modules.
import numpy as np
import cv2
from cv2 import aruco
import glob
import scipy.io as sio

# ChAruco board variables
square_width = 44  #number of squares width
square_height =28  #number of squares height
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_5X5_1000)

#Camera_matrix = np.array([[ 3474.23634,0.0,1640.03816],[ 0.0,3536.488,1230.75273],[ 0.0,0.0,1.0]],np.float32 )
#dist_coeffs  = np.array([[ 0.7705997, -1.5690791, 0.00656675, 0.0172006, 1.77142052]],np.float32 )

# Create constants to be passed into OpenCV and Aruco methods
CHARUCO_BOARD = aruco.CharucoBoard_create(
        squaresX=square_width,
        squaresY=square_height,
        squareLength=0.005,
        markerLength=0.003,
        dictionary=ARUCO_DICT)

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.001)

# Create the arrays and variables storing corners and IDs from images processed
corners_all = [] # Corners discovered in all images processed
ids_all = [] # Aruco ids corresponding to corners discovered
image_size = None # Determined at runtime

# Images used
camera_name = 'Cam_2'
img_path = 'D:\\Data\\' + camera_name
images = glob.glob(img_path + '\\*.jpg')

# import the Initial Camera Parameters
#Camera_matrix = np.load(img_path + '\\calib_param_' + camera_name + '.npz')['mtx']
#dist_coeffs= np.load(img_path + '\\calib_param_' + camera_name + '.npz')['dist']

# Loop through images glob'ed
for fname in images:
    img = cv2.imread(fname)
    #cv2.imshow('test', img)
    #cv2.waitKey(0)

# Grayscale the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find aruco markers in image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        image=gray,
        dictionary=ARUCO_DICT,
        #cameraMatrix=Camera_matrix,
        #distCoeff=dist_coeffs
    )

# Outline the aruco markers found in image
    img = aruco.drawDetectedMarkers(
        image=img,
        corners=corners,
        borderColor = (0, 255, 255))
    cv2.imshow('frame', img)
    cv2.waitKey(2000)

# Get charuco corners and ids from detected aruco markers
    if len(corners)>0:
        #SUB PIXEL DETECTION
        #for corner in corners:
           #cv2.cornerSubPix(gray, corner, winSize=(11, 11), zeroZone=(-1, -1),criteria=criteria)

        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
        markerCorners=corners,
        markerIds=ids,
        image=gray,
        board=CHARUCO_BOARD,
        #cameraMatrix=Camera_matrix,
        #distCoeffs=dist_coeffs
        )

        # Refine Charucocorner in sub pixel level twice with different searching Windows size
        charuco_corners2 = cv2.cornerSubPix(gray, charuco_corners, (80, 80), (-1, -1), criteria)
        charuco_corners3 = cv2.cornerSubPix(gray, charuco_corners2, (20, 20), (-1, -1), criteria)

# If Charuco board found, Collect corner points in image plane
    if response > 0:  # Requiring at least 20 squares or more
        corners_all.append(charuco_corners3)
        ids_all.append(charuco_ids)

        print('charuco_corners:',corners_all)
        #print('Id:',ids_all)

# Draw the Charuco board to show properly detected or not
        dst = aruco.drawDetectedCornersCharuco(
            image=img,
            charucoCorners=charuco_corners3,
            charucoIds=charuco_ids)
        cv2.imwrite("charuco_detectedconers.jpg", dst)

# display image, waiting for key press
        cv2.imshow('Charuco board', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
