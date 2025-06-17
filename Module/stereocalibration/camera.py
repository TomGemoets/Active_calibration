import numpy as np 
import cv2
from ..calibration_grid_generation import *



import glob
from scipy.spatial.transform import Rotation


class Camera():
    def __init__(self,list_images_pour_calibration):
        self.list_images_pour_calibration = list_images_pour_calibration

    def calibrate(self, list_object_points, list_image_points, image_gray, stock_image):
        """Perform the linear calibration from the images of the grid target.

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm
        list_image --  list of all the calibration image paths

        Returns a list of the grid target properties from ```define_grid_target()```.
        Returns a list of the positions of the grids in number of pixels on the images.
        Returns a list of all the image paths.
        Returns the camera matrix.
        Returns the distortion coefficients.
        Returns the rotation vectors estimated for each pattern view.
        Returns the translation vectors estimated for each pattern view.
        Returns the total RMS re-projection error.
        """
        # Detection of the features on each image
        #list_object_points, list_image_points, image_gray, stock_image = self.detect_centers()

        # Calibration
        boolean_calibration, camera_matrix, distortion_coefficient, rotation_camera, translation_camera = cv2.calibrateCamera(list_object_points, list_image_points, image_gray.shape[::-1], None, None)

        #reprojection error
        mean_error_reprojection = 0
        for grid_point in range(len(list_object_points)):
            projection_target, jacobian_matrix = cv2.projectPoints(list_object_points[grid_point], rotation_camera[grid_point], translation_camera[grid_point], camera_matrix, distortion_coefficient)
            error = np.linalg.norm(list_image_points[grid_point] - projection_target) / len(projection_target)
            mean_error_reprojection += error

        total_error = mean_error_reprojection/len(list_object_points)

        return list_object_points, list_image_points, stock_image ,camera_matrix, distortion_coefficient, rotation_camera, translation_camera, total_error


class CameraActive(Camera):
    def __init__(self, list_image, dot_grid_size, dot_grid_spacing):
        super().__init__(list_image)
        self.dot_grid_spacing = dot_grid_spacing
        self.dot_grid_size = dot_grid_size
        self.list_image = list_image
    
    def detect_centers(self):
        """Detect the grids on a calibration plate on several images.

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm
        list_image --  list of all the calibration image paths

        Returns a list of the grid target properties from ```define_grid_target()```.
        Returns a list of the positions of the grids in number of pixels on the images.
        Returns the last image in greyscale.
        Returns a list of all the image paths.
        """
        list_object_points = []
        list_image_points = []

        stock_image = []

        # Blob detector properties
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.filterByCircularity = True
        params.filterByConvexity = False
        params.filterByInertia = True
        params.filterByColor = False
        params.minArea = 200
        params.maxArea = 10e4
        params.minCircularity = 0.3
        params.minInertiaRatio = 0.01
        params.minRepeatability = 6
        params.minDistBetweenBlobs = 1
        detector = cv2.SimpleBlobDetector_create(params)

        for each_image in self.list_image:
            image = cv2.imread(each_image)
            stock_image.append(image)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            boolean_detection, circle_center = cv2.findCirclesGrid(image_gray, self.dot_grid_size, flags=(cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING), blobDetector = detector)

            if boolean_detection == True:
                active_dot_target = ActiveDottedGrid("plaque de calibrage active", self.dot_grid_size, self.dot_grid_spacing, self.list_image)
                list_object_points.append(active_dot_target.define_dotted_grid_target())
                #list_object_points.append(self.define_grid_target())

                list_image_points.append(circle_center)

                cv2.drawChessboardCorners(image, self.dot_grid_size, circle_center, boolean_detection)
                cv2.imshow('image', image)

                cv2.waitKey(500)
        cv2.destroyAllWindows()
        return list_object_points, list_image_points, image_gray, stock_image

    #def calibrate(list_object_points, list_image_points, image_gray, stock_image):
        """Perform the linear calibration from the images of the grid target.

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm
        list_image --  list of all the calibration image paths

        Returns a list of the grid target properties from ```define_grid_target()```.
        Returns a list of the positions of the grids in number of pixels on the images.
        Returns a list of all the image paths.
        Returns the camera matrix.
        Returns the distortion coefficients.
        Returns the rotation vectors estimated for each pattern view.
        Returns the translation vectors estimated for each pattern view.
        Returns the total RMS re-projection error.
        """
        # Detection of the features on each image
        """list_object_points, list_image_points, image_gray, stock_image = self.detect_centers()

        # Calibration
        boolean_calibration, camera_matrix, distortion_coefficient, rotation_camera, translation_camera = cv2.calibrateCamera(list_object_points, list_image_points, image_gray.shape[::-1], None, None)

        #reprojection error
        mean_error_reprojection = 0
        for grid_point in range(len(list_object_points)):
            projection_target, jacobian_matrix = cv2.projectPoints(list_object_points[grid_point], rotation_camera[grid_point], translation_camera[grid_point], camera_matrix, distortion_coefficient)
            error = np.linalg.norm(list_image_points[grid_point] - projection_target) / len(projection_target)
            mean_error_reprojection += error

        total_error = mean_error_reprojection/len(list_object_points)

        return list_object_points, list_image_points, stock_image ,camera_matrix, distortion_coefficient, rotation_camera, translation_camera, total_error
"""

class CameraPassive(Camera):
    def __init__(self, list_image ):
        self.list_images = list_image

    def find_corners(self, col_chessboard, ligne_chessboard):
        # Cherche les coins pour chaque sample image left
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros(((col_chessboard - 1) * (ligne_chessboard - 1), 3), np.float32)
        objp[:, :2] = np.mgrid[0:col_chessboard - 1, 0:ligne_chessboard - 1].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.
        stock_img = [] #contient toutes les photos qui passe dans la calibration

        for fname in self.list_images:
            img = cv2.imread(fname)
            stock_img.append(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (col_chessboard - 1, ligne_chessboard - 1), None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
            elif ret == False:
                print("rien trouvé")

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (col_chessboard - 1, ligne_chessboard - 1), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)
        #cv2.destroyAllWindows()
        return objpoints, imgpoints, gray, stock_img

