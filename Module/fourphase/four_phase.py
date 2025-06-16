import numpy as np
import cv2
import os

class FourPhase():
    def __init__(self, list_image):
        self.list_image = list_image
        self.position_number = self.get_position_and_camera_number()[0]
        self.camera_number = self.get_position_and_camera_number()[1]

    def get_position_and_camera_number(self):
        """Get the position and the camera number from the name of an image.

        Keyword argument:
        list_images -- list of the image paths

        Returns the position number and the camera number.
        """
        folder, filename_extansion = self.list_image[0].split('\\',1)
        filename, extansion = filename_extansion.split('.',1)
        position_number , phase_value, camera_number = filename.split('_',3)
        return position_number, camera_number

    # Get array from image
    def get_image_array(self, image):
        """Read an image with OpenCV.

        Keyword argument:
        image -- image path

        Returns an array of all pixel values in greyscale of the image.
        """
        image_read = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        image_array = image_read.astype(float)
        return image_array
    
    # Calculate four-phase shift
    def calculate_four_phase_shifting(self):
        """Calculate the phase map from a list of four-phase shifted images

        Keyword argument:
        list_images -- list of the four-shifted image path

        Returns an array of pixel values from the four-phase shifting equation.
        Creates an image of the phase map and saves it in the folder 'Four_phase_images'.
        """
        # Determine the dimensions of the images
        number_pixel_x, number_pixel_y = self.get_image_array(self.list_image[0]).shape

        # Initialize four_phase_array array
        four_phase_array = np.zeros((number_pixel_x, number_pixel_y), dtype=float)

        # Calculate arctan value
        numerator = self.get_image_array(self.list_image[3]) - self.get_image_array(self.list_image[1])
        denominator = self.get_image_array(self.list_image[0]) - self.get_image_array(self.list_image[2])

        fraction = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)
        arctan_value = np.abs(np.arctan(fraction))

        # Initialize arctan and pi coefficient
        arctan_coefficient = np.zeros((number_pixel_x, number_pixel_y))
        pi_coefficient = np.zeros((number_pixel_x, number_pixel_y))

        # Set all the conditions and the choice values
        conditions = [(numerator > 0) & (denominator > 0), 
                    (numerator > 0) & (denominator < 0), 
                    (numerator < 0) & (denominator < 0),
                    (numerator < 0) & (denominator > 0),
                    (numerator == 0) & (denominator < 0),
                    (numerator > 0) & (denominator == 0),
                    (numerator < 0) & (denominator == 0),
                    (numerator == 0) & (denominator > 0),
                    (numerator == 0) & (denominator == 0)]

        choices_arctan_coefficient = [1, -1, 1, -1, 0, 0, 0, 0, 0]
        choices_pi_coefficient = [0, 1, 1, 2, 1, 1/2, 3/2, 0, 1/2]

        # Create a tuple of conditions and choices
        tuple_conditions_choices = zip(conditions, choices_arctan_coefficient, choices_pi_coefficient)

        for each_condition, each_choice_arctan_coefficient, each_choice_pi_coefficient in tuple_conditions_choices:
            arctan_coefficient[each_condition] = each_choice_arctan_coefficient
            pi_coefficient[each_condition] = each_choice_pi_coefficient
    
        four_phase_array = pi_coefficient * np.pi + arctan_coefficient * arctan_value

        # Scale and convert phase values
        four_phase_image = four_phase_array / (2 * np.pi) * 255
        four_phase_image = four_phase_image.astype(np.uint8)

        # Save picture
        #cv2.imshow('Four phase yield', four_phase_image)
        #cv2.waitKey(500)
        if os.path.exists('./Four_phase_images'):
            cv2.imwrite('./Four_phase_images/' + self.position_number + '_' + self.camera_number + '.tif', four_phase_image)
        else:
            os.mkdir('./Four_phase_images')
            cv2.imwrite('./Four_phase_images/' + self.position_number + '_' + self.camera_number + '.tif', four_phase_image)
        #cv2.destroyAllWindows()
