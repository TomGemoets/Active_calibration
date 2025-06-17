import xml.etree.ElementTree as ET
import numpy as np
from  math import *


class ExportToXML():
    def __init__(self, camera_matrix_left, distortion_coefficient_left, camera_matrix_right, distortion_coefficient_right, euler_angles, translation_vector):
        self.camera_matrix_left = camera_matrix_left
        self.camera_matrix_right = camera_matrix_right

        self.distortion_coefficient_left = distortion_coefficient_left
        self.distortion_coefficient_right = distortion_coefficient_right

        self.euler_angles = euler_angles
        self.translation_vector = translation_vector
    
    def write_XML(self):
        """Export the calibration data in a XML file.

        Keyword arguments:
        camera_matrix_left -- camera matrix of the left camera
        distortion_coefficient_left -- distortion coefficients of the left camera
        camera_matrix_right -- camera matrix of the right camera
        distortion_coefficient_right -- distortion coefficients of the right camera
        euler_angles -- euler angles from the rotation matrix in degrees
        translation_vector -- translation vector between the cameras

        Returns an XML file with the calibration data.
        """
        # Extract data
        center_x_left = self.camera_matrix_left[0][2]
        center_y_left = self.camera_matrix_left[1][2]
        focal_length_x_left = self.camera_matrix_left[0][0]
        focal_length_y_left = self.camera_matrix_left[1][1]
        kappa_1_left = self.distortion_coefficient_left[0][0]
        kappa_2_left = self.distortion_coefficient_left[0][1]
        kappa_3_left = self.distortion_coefficient_left[0][4]

        center_x_right = self.camera_matrix_right[0][2]
        center_y_right = self.camera_matrix_right[1][2]
        focal_length_x_right = self.camera_matrix_right[0][0]
        focal_length_y_right = self.camera_matrix_right[1][1]
        kappa_1_right = self.distortion_coefficient_right[0][0]
        kappa_2_right = self.distortion_coefficient_right[0][1]
        kappa_3_right = self.distortion_coefficient_right[0][4]

        alpha = self.euler_angles[0]
        beta = self.euler_angles[1]
        gamma = self.euler_angles[2]

        translation_x = self.translation_vector[0][0]
        translation_y = self.translation_vector[1][0]
        translation_z = self.translation_vector[2][0]

        magnitude = sqrt(translation_x ** 2 + translation_y ** 2 + translation_z ** 2)

        # Create the root element
        root = ET.Element("calibration")
        root.set("lri", "calibration")
        root.text="\n"

        # Create the first camera element
        camera_left = ET.SubElement(root, "camera")
        camera_left.set("id", "0")
        camera_left.text = f'{center_x_left} {center_y_left} {focal_length_x_left} {focal_length_y_left} {kappa_1_left} {kappa_2_left} {kappa_3_left}'
        camera_left.tail = "\n"

        # Create the second camera element
        camera_right = ET.SubElement(root, "camera")
        camera_right.set("id", "1")
        camera_right.text = f'{center_x_right} {center_y_right} {focal_length_x_right} {focal_length_y_right} {kappa_1_right} {kappa_2_right} {kappa_3_right}'
        camera_right.tail = "\n"

        # Create orientation
        orientation = ET.SubElement(root, "orientation")
        orientation.text = "\n"
        rotation = ET.SubElement(orientation, "rotation")
        rotation.text = f'{alpha} {beta} {gamma}'
        rotation.tail ="\n"
        translation = ET.SubElement(orientation, "translation")
        translation.text = f'{translation_x} {translation_y} {translation_z}'
        translation.tail = "\n"
        magnitude = ET.SubElement(orientation, "magnitude")
        magnitude.text = f'{magnitude}'
        magnitude.tail = "\n"
        orientation.tail = "\n"


        # Create the XML tree
        tree = ET.ElementTree(root)

        # Write the XML tree to a file
        tree.write("calibration_parameters.xml", encoding="ISO-8859-1", xml_declaration=True)


    def write_XML_VIC(self, repere_general):
        """Export the calibration data in a XML file.

        Keyword arguments:
        camera_matrix_left -- camera matrix of the left camera
        distortion_coefficient_left -- distortion coefficients of the left camera
        camera_matrix_right -- camera matrix of the right camera
        distortion_coefficient_right -- distortion coefficients of the right camera
        euler_angles -- euler angles from the rotation matrix in degrees
        translation_vector -- translation vector between the cameras

        Returns an XML file with the calibration data.
        """
        # Extract data
        center_x_left = self.camera_matrix_left[0][2]
        center_y_left = self.camera_matrix_left[1][2]
        focal_length_x_left = self.camera_matrix_left[0][0]
        focal_length_y_left = self.camera_matrix_left[1][1]
        skew_left = self.camera_matrix_left[0][1]
        kappa_1_left = self.distortion_coefficient_left[0][0]
        kappa_2_left = self.distortion_coefficient_left[0][1]
        kappa_3_left = self.distortion_coefficient_left[0][4]

        center_x_right = self.camera_matrix_right[0][2]
        center_y_right = self.camera_matrix_right[1][2]
        focal_length_x_right = self.camera_matrix_right[0][0]
        focal_length_y_right = self.camera_matrix_right[1][1]
        skew_right = self.camera_matrix_right[0][1]
        kappa_1_right = self.distortion_coefficient_right[0][0]
        kappa_2_right = self.distortion_coefficient_right[0][1]
        kappa_3_right = self.distortion_coefficient_right[0][4]

        alpha = self.euler_angles[0]
        beta = self.euler_angles[1]
        gamma = self.euler_angles[2]

        translation_x = self.translation_vector[0][0]
        translation_y = self.translation_vector[1][0]
        translation_z = self.translation_vector[2][0]

        # Transfer parameters into VIC format

        alpha0 = repere_general[0][0]
        beta0 = repere_general[0][1]
        gamma0 = repere_general[0][2]
        x0 = repere_general[1][0]
        y0 = repere_general[1][1]
        z0 = repere_general[1][2]

        alpha_left = alpha0
        beta_left = beta0
        gamma_left = gamma0

        alpha_right = alpha0 - alpha
        beta_right = beta0 - beta
        gamma_right = gamma0 - gamma

        translation_x_left = x0
        translation_y_left = y0
        translation_z_left = z0

        translation_x_right = translation_x - x0
        translation_y_right = translation_y - y0
        translation_z_right = translation_z - z0

        # Create the root element
        root = ET.Element("project")
        root.set("dir", "chemin")
        root.text = "\n"
        root.tail = "\n"

        # Create the root element
        calibration = ET.SubElement(root,"calibration")
        calibration.set("lri", "calibration")
        calibration.text = "\n"

        # Create the first camera element
        camera_left = ET.SubElement(calibration, "camera")
        camera_left.set("id", "0")
        camera_left.text = f'{center_x_left} {center_y_left} {focal_length_x_left} {focal_length_y_left} {skew_left} {kappa_1_left} {kappa_2_left} {kappa_3_left}'
        orientation_left = ET.SubElement(camera_left, "orientation")
        orientation_left.text = f' {alpha_left} {beta_left} {gamma_left} {translation_x_left} {translation_y_left} {translation_z_left}'
        orientation_left.tail = "\n"
        camera_left.tail = "\n"

        # Create the second camera element
        camera_right = ET.SubElement(calibration, "camera")
        camera_right.set("id", "1")
        camera_right.text = f'{center_x_right} {center_y_right} {focal_length_x_right} {focal_length_y_right} {skew_right} {kappa_1_right} {kappa_2_right} {kappa_3_right}'
        orientation_right = ET.SubElement(camera_right, "orientation")
        orientation_right.text = f' {alpha_right} {beta_right} {gamma_right} {translation_x_right} {translation_y_right} {translation_z_right}'
        orientation_right.tail = "\n"
        camera_right.tail = "\n"


        # Create the XML tree
        tree = ET.ElementTree(root)

        # Write the XML tree to a file
        tree.write("project.xml", encoding="ISO-8859-1", xml_declaration=True)


    def rotationMatrixEuler(self, alpha, beta, gamma):
        alpha = radians(alpha)
        beta = radians(beta)
        gamma = radians(gamma)
        R = np.array([[cos(beta) * cos(gamma), sin(alpha) * sin(beta) * cos(gamma) - cos(alpha) * sin(gamma),
                       cos(alpha) * sin(beta) * cos(gamma) + sin(alpha) * sin(gamma)],
                      [cos(beta) * sin(gamma), sin(alpha) * sin(beta) * sin(gamma) + cos(alpha) * cos(gamma),
                       cos(alpha) * sin(beta) * sin(gamma) - sin(alpha) * cos(gamma)],
                      [-sin(beta), sin(alpha) * cos(beta), cos(alpha) * cos(beta)]])
        return R

test = [[[4.69177326e+03, 0.00000000e+00, 1.14997865e+03], [0.00000000e+00, 4.69195035e+03, 1.08197998e+03], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], [[-6.87284926e-02, -1.53296516e+00,  1.01792327e-03, -3.56298259e-03,  -5.93088358e+01]], [[4.68490841e+03, 0.00000000e+00, 1.13693331e+03], [0.00000000e+00, 4.68644278e+03, 1.05681962e+03], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], [[-7.92820681e-02, -5.63249090e+00, -1.31658829e-04, -4.42416335e-03,   2.05720954e+02]], [[ 0.99542649, -0.05189491,  0.08020617], [ 0.05134249,  0.99864113,  0.00893598], [-0.08056091, -0.00477713,  0.99673824]], [[-208.44747426], [   3.10579127], [ -15.67951203]], [ 2.98431905,  4.60041637, -0.5136559 ]]

ExportToXML(test[0], test[1], test[2], test[3],test[6], test[5]).write_XML_VIC([[0,0,0],[0,0,0]])


