import numpy as np
import os
from PIL import Image
#rajouter la génération du chessboard ici
class CircularFringe():
    def __init__(self, length_pixel, mean_intensity, amplitude, phase):
        self.length_pixel = length_pixel
        self.mean_intensity = mean_intensity
        self.amplitude = amplitude
        self.phase = phase
    
    def calculate_radius(self):
        """Calculate the radius for each pixel from the center of a square.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square

        Returns an array of (length_pixel, length pixel) with the radius value for each pixel.
        """
        # Create grid of coordinates
        y_pixel, x_pixel = np.ogrid[:self.length_pixel, :self.length_pixel]
    
        # Calculate distance from each pixel to the center
        radius_from_center = np.sqrt((y_pixel - self.length_pixel / 2) ** 2 + (x_pixel - self.length_pixel / 2) ** 2)
        return radius_from_center
    
    def generate_sinusoidal_fringe(self):
        """Calculate the intensity value for each pixel for a circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees

        Returns an array of all pixel values between 0 and 255 of the circular fringe.
        """
        # Calculate all pixels values from radius_from_center
        fringe_array = self.mean_intensity + self.amplitude * np.sin(2 * np.pi * self.calculate_radius() / self.length_pixel - np.radians(self.phase))

        # Fix the minimum and maximum values of the array
        return np.clip(fringe_array, 0, 255).astype(np.uint8)

class TargetGrid(CircularFringe):
    def __init__(self, length_pixel, mean_intensity, amplitude, phase, grid_length, grid_width, image_name):
        super().__init__(length_pixel, mean_intensity, amplitude, phase)
        self.grid_length = grid_length
        self.grid_width = grid_width
        self.image_name = image_name
    
    def generate_grid_target(self):
        """Generate a grid target from the circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees
        grid_length -- number of circular fringes on the length of the grid target
        grid_width -- number of circular fringes on the width of the grid target
        image_name -- string of the image name

        Returns an array of all pixel values between 0 and 255 of the grid target.
        Creates an image of the grid target and saves it in the folder 'Target_images'.
        """
        grid_array = np.concatenate([np.concatenate([self.generate_sinusoidal_fringe()] * self.grid_length, axis = 1)] * self.grid_width, axis = 0)

        image = Image.fromarray(grid_array)

        if os.path.exists('./Target_images'):
            image.save('./Target_images/' + self.image_name + '_' + str(self.phase).zfill(3) + '.tif')
            
        else:
            os.mkdir('./Target_images')
            image.save('./Target_images/' + self.image_name + '_' + str(self.phase).zfill(3) + '.tif')

        print(f'The active targets of phase {self.phase}° has been created.')
        return grid_array
