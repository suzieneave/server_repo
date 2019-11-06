##%% Clear interpreter.
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

# Import modules.
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

#%% First find corners in all images.

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points for chequerboard grid.
num_x = 6
num_y = 7
side_length = 15
objp = np.zeros((num_y*num_x,3), np.float32)
objp[:,:2] = np.mgrid[0:num_y,0:num_x].T.reshape(-1,2)*side_length


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(r'calib_image_*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (num_y,num_x), None, cv2.CALIB_CB_FAST_CHECK)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (num_y,num_x), corners2,ret)
        cv2.imshow('img',cv2.resize(img, (0,0), fx=0.5, fy=0.5))
        cv2.waitKey(100)

cv2.destroyAllWindows()

#%% Perform camera calibration.
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print("RMS error: ", ret, "pixels")
print("Distortion parameters [[k1 k2 p1 p2 k3]]:", dist)
np.savez('calib', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

#%% Undistort images.
for fname in images:
    img = cv2.imread(fname)
    h,  w = img.shape[:2]
    print(h)
    print(w)
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    
    # Undistort image.
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # Crop the image.
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    index = fname.find('calib')
    undistort_fname =  fname[:index] + 'undistorted_' + fname[index:]
    cv2.imwrite(undistort_fname,dst)
    
#%% Plot reprojection errors.
plt.close("all")
# Create colormap.
norm = mpl.colors.Normalize(vmin=1, vmax=len(objpoints))
cmap = cm.jet
m = cm.ScalarMappable(norm=norm, cmap=cmap)

for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = imgpoints[i] - imgpoints2  # imgpoints is the actual location (distorted) of our corners.
    								   # imgpoints2 is where the points on our boards would appear in the distorted image if we had correctly calculated the dostortion constants.
    for j in range(len(error)):
        pt_error = error[j]
        if j==0:
            plt.scatter(pt_error[0,0],pt_error[0,1], marker = 'o', alpha=1.0, color=m.to_rgba(i+1), label=str(i+1))
        else:
            plt.scatter(pt_error[0,0],pt_error[0,1], marker = 'o', alpha=1.0, color=m.to_rgba(i+1))
plt.xlim([-3,3])
plt.ylim([-3,3])
plt.xlabel('Horizontal error (px)')
plt.ylabel('Vertical error (px)')
plt.subplots_adjust(left=0.1, right=0.8, top=0.95, bottom=0.1)
plt.legend(loc=(1.05,0.1),frameon=False)
plt.savefig(fname[:index]+'Reprojection_Error.png', dpi=600) 
plt.show()