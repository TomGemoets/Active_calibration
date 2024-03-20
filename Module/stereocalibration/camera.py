import numpy as np 
import cv2
import glob
from scipy.spatial.transform import Rotation


class GridTarget():
    def __init__(self, dot_grid_size, dot_grid_spacing):
        self.dot_grid_size = dot_grid_size
        self.dot_grid_spacing = dot_grid_spacing
    
    # Define the grid of the calibration target
    def define_grid_target(self):
        """Create grid target from the grid size and the grid spacing

        Keyword arguments:
        dot_grid_size -- tuple of the number of dots (length, width)
        dot_grid_spacing -- spacing between each dot in mm

        Returns an array of all the positions in mm of the grids.
        """
        grid_target_points = np.zeros((self.dot_grid_size[0] * self.dot_grid_size[1], 3), np.float32)
        grid_target_points[:,:2] = np.mgrid[0 : self.dot_grid_size[0], 0 : self.dot_grid_size[1]].T.reshape(-1,2)* self.dot_grid_spacing
        return grid_target_points


class Camera(GridTarget):
    def __init__(self,  dot_grid_size, dot_grid_spacing, list_image):
        super().__init__(dot_grid_size, dot_grid_spacing)
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
                list_object_points.append(self.define_grid_target())

                list_image_points.append(circle_center)

                cv2.drawChessboardCorners(image, self.dot_grid_size, circle_center, boolean_detection)
                cv2.imshow('image', image)

                cv2.waitKey(500)
        cv2.destroyAllWindows()
        return list_object_points, list_image_points, image_gray, stock_image
    
    def calibrate(self):
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
        list_object_points, list_image_points, image_gray, stock_image = self.detect_centers()

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