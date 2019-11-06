import cv2
import glob
import os

#%% Define ArUco dictionary and detection parameters.
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters =  cv2.aruco.DetectorParameters_create()

#%% Get list of all images in folder.
cwd = os.getcwd()
filepath = os.path.join(cwd, 'ChArUco_Calibration/3D')
#os.chdir(filepath)
#images = glob.glob(r'calib_*.jpg')
print(os.path.exists('printed_charuco.jpg'))
images = glob.glob(r'printed_charuco.jpg')

#%% Load images and detect markers.
num_points = 0
for fname in images:
    img = cv2.imread(fname)
    print (img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print('corners: ', type(corners), 'ids: ', type(ids), 'rejected image poitns: ', type(rejectedImgPoints))

    gray = cv2.aruco.drawDetectedMarkers(gray, corners, ids, borderColor = (255, 255, 0))
    cv2.imshow('frame',gray)
    cv2.waitKey(50000)
    num_points = num_points + len(corners)

    size_of_marker =  0.003 # side lenght of the marker in meter
    rvecs,tvecs = cv2.aruco.estimatePoseSingleMarkers(corners, size_of_marker , mtx, dist)

#cv2.destroyAllWindows()
#os.chdir(cwd)
