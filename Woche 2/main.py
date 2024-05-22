# Write a simple python script that can calibrate a camera and rectify an input image (see
# e.g. https://docs.opencv.org/master/dc/dbb/ tutorial_py_calibration.html). To validate your program,
# use the handsome gui-based MRT Camera Calibration Toolbox (see https://github.com/MT-MRT/
# MRT-Camera-Calibration-Toolbox) to obtain a calibration corresponding to the data given in the file
# calibrationImagesCheckerboard.zip.
import cv2
import numpy as np
import cv2 as cv
import glob

def read_images(path: str):
    return glob.glob(path)

def undistort(images: list[str], get_error: bool, mode: str, draw: bool):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    i = 0
    for fname in images:
        img = cv.imread(fname)
        # img = cv2.resize(src=img, dsize=[1000, 1333], fx=0.3, fy=0.3)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7, 6), None)
        # ret, centers = cv.findCirclesGrid(gray, (# number of centers), output_array)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (7, 6), corners2, ret)

        if draw:
            cv.imshow('img', img)
            # cv.waitKey(500) # why?

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        # img = cv.imread('left12.jpg')

        h, w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        if mode == 'remapping':
            # undistort
            mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
            dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

            # crop the image
            x, y, w, h = roi
            # dst = dst[y:y + dst.shape[0], x:x + dst.shape[1]]
            dst = dst[y:y + h, x:x + w]
            cv.imwrite(mode+str(i)+'calibresult.png', dst)
            i += i

        elif mode == 'cv':
            # undistort
            dst = cv.undistort(img, mtx, dist, None, newcameramtx)

            # crop the image
            x, y, w, h = roi
            #dst = dst[y:y + dst.shape[0], x:x + dst.shape[1]]
            dst = dst[y:y + h, x:x + w]
            cv.imwrite(mode+str(i)+'calibresult.png', dst)
            i+=i

        if get_error:
            mean_error = 0
            for i in range(len(objpoints)):
                imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
                error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
                mean_error += error

            print("total error: {}".format(mean_error / len(objpoints)))




if __name__ == '__main__':
    images = read_images('Test\\*.jpg') # only five of the test pictures"
#    images = read_images('calibrationImagesCheckerboard\\*.jpg')

    # undistort(images, get_error=True, mode='cv', draw=False)

    undistort(images, get_error=True, mode='remapping', draw=False)

    cv.destroyAllWindows()

