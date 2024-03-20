import numpy as np 
import cv2
import glob
from scipy.spatial.transform import Rotation

class StereoCameras:
    def __init__(self, calibration_left, calibration_right):
        self.calibration_left = calibration_left
        self.calibration_right = calibration_right
    
    def stereo_calibrate(self):
        """Perform the stereocalibration of two cameras.

        Keyword arguments:
        calibration_left -- calibration properties of the left camera from the object instanced with the Class ```Camera```
        calibration_right -- calibration properties of the right camera from the object instanced with the Class ```Camera```

        Returns the camera matrix of the left camera.
        Returns the distortion coefficients of the left camera.
        Returns the camera matrix of the right camera.
        Returns the distortion coefficients of the right camera.
        Returns the rotation matrix between the cameras.
        Returns the translation vector between the cameras.
        Returns the euler angles from the rotation matrix in degrees.
        """
        list_object_points = self.calibration_left[0]

        list_image_points_left = self.calibration_left[1]
        stock_image_left = self.calibration_left[2]
        camera_matrix_left = self.calibration_left[3]
        distortion_coefficient_left = self.calibration_left[4]

        list_image_points_right = self.calibration_right[1]
        stock_image_right = self.calibration_right[2]
        camera_matrix_right = self.calibration_right[3]
        distortion_coefficient_right = self.calibration_right[4]

        boolean_stereo, stereo_matrix_left, stereo_distortion_left, stereo_matrix_right, stereo_distortion_right, rotation_matrix, translation_vector, essential_matrix, fundamental_matrix = cv2.stereoCalibrate(list_object_points, list_image_points_left, list_image_points_right, camera_matrix_left, distortion_coefficient_left, camera_matrix_right, distortion_coefficient_right, (stock_image_left[0].shape[1], stock_image_right[0].shape[0]), flags=cv2.CALIB_FIX_INTRINSIC)

        # Print the calibration parameters
        

        #get euler angles
        rotation = Rotation.from_matrix(rotation_matrix)
        euler_angles = rotation.as_euler('zyx', degrees =True)

        print('Camera matrix of the left camera:\n', stereo_matrix_left)
        print('Distortion coefficients of the left camera:\n', stereo_distortion_left)
        print('Linear calibration error from the left camera:\n', self.calibration_left[7], '\n')

        print('Camera matrix of the right camera:\n', stereo_matrix_right)
        print('Distortion coefficients of the right camera:\n', stereo_distortion_right)
        print('Linear calibration error from the right camera:\n', self.calibration_right[7], '\n')

        print("Translation vector between the cameras:\n", translation_vector)
        print('Rotation angles:\n', euler_angles)

        return stereo_matrix_left, stereo_distortion_left, stereo_matrix_right, stereo_distortion_right, rotation_matrix, translation_vector, euler_angles