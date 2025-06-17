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

        alpha0 = repere_general[0][1]
        beta0 = repere_general[1][1]
        gamma0 = repere_general[2][1]
        x0 = repere_general[0][0]
        y0 = repere_general[1][0]
        z0 = repere_general[2][0]

        alpha_left = alpha0
        beta_left = beta0
        gamma_left = gamma0

        alpha_right = alpha0 - alpha
        beta_right = beta0 - beta
        gamma_right = gamma0 - gamma

        translation_x_left = translation_x
        translation_y_left = translation_y
        translation_z_left = translation_z

        print("test")



        # Create the root element
        root = ET.Element("calibration")
        root.set("lri", "calibration")
        root.text = "\n"

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
        rotation.tail = "\n"
        translation = ET.SubElement(orientation, "translation")
        translation.text = f'{translation_x} {translation_y} {translation_z}'
        translation.tail = "\n"
        orientation.tail = "\n"

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

