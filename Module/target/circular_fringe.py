import numpy as np
import os
from PIL import Image

class CircularFringe():
    def __init__(self, length_pixel):
        self.length_pixel = int(length_pixel)

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

    def generate_sinusoidal_fringe(self, mean_intensity, amplitude, phase):
        """Calculate the intensity value for each pixel for a circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees

        Returns an array of all pixel values between 0 and 255 of the circular fringe.
        """
        # Calculate all pixels values from radius_from_center
        fringe_array = mean_intensity + amplitude * np.sin(
            2 * np.pi * self.calculate_radius() / self.length_pixel - np.radians(phase))

        # Fix the minimum and maximum values of the array
        return np.clip(fringe_array, 0, 255).astype(np.uint8)

    def generate_sinusoidal_fringe_with_hole(self, mean_intensity, amplitude, phase):
        """Calculate the intensity value for each pixel for a circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees
        ratio_dot -- width ratio for the white circle inside the black circle

        Returns an array of all pixel values between 0 and 255 of the circular fringe.

            Generate a circular fringe with:
            - White center (phase = 3π/2) → φ superposé ≈ 255
            - Sinusoidal ring (π/2 to 3π/2) → frange contrastée
            - White background (phase = 3π/2) → φ superposé ≈ 255
        """

        # Calculate the base sinusoidal fringe
        radius = self.calculate_radius()
        fringe_array = mean_intensity + amplitude * np.sin(
            2 * np.pi * radius / self.length_pixel - np.radians(phase))


        # Dephased sinusoidal peak amplitude with doubled frequency
        peak_amplitude = amplitude * np.sin(
            3 * 2 * np.pi * radius / self.length_pixel - np.radians(phase+180))

        if phase == 0:
            sinusoidal_peak = mean_intensity + abs(peak_amplitude)
        elif phase == 180:
            sinusoidal_peak = mean_intensity - abs(peak_amplitude)
        else :
            sinusoidal_peak = mean_intensity + peak_amplitude

        # Combine the sinusoidal fringe with the dephased peak, applying it only near the center
        fringe_array = np.where(radius < self.length_pixel / 4, sinusoidal_peak, fringe_array)

        # Clip the values to ensure they stay between 0 and 255
        return np.clip(fringe_array, 0, 255).astype(np.uint8)

    def generate_black_circle(self):
        """Calculate the intensity value for each pixel for a circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees

        Returns an array of all pixel values between 0 and 255 of the circular fringe.
        """
        # Calculate all pixels values from radius_from_center
        radius = self.calculate_radius()
        black_circle = np.where(radius < self.length_pixel / 4, 0, 255)

        # Fix the minimum and maximum values of the array
        return np.clip(black_circle, 0, 255).astype(np.uint8)

    def generate_black_circle_with_hole(self):
        """Calculate the intensity value for each pixel for a circular fringe.

        Keyword arguments:
        length_pixel -- number of pixels on a side of the square
        mean_intensity -- mean intensity value of the sinusoid
        amplitude -- amplitude of the sinusoid
        phase -- phase value in degrees

        Returns an array of all pixel values between 0 and 255 of the circular fringe.
        """
        # Calculate all pixels values from radius_from_center
        radius = self.calculate_radius()
        black_circle = np.where(((radius < self.length_pixel / 4) & (radius > self.length_pixel / 12)), 0, 255)

        # Fix the minimum and maximum values of the array
        return np.clip(black_circle, 0, 255).astype(np.uint8)


class TargetGrid(CircularFringe):
    def __init__(self, length_pixel,  grid_length, grid_width, exit_file_path):
        self.length_pixel = int(length_pixel)
        print("length_pixel =", self.length_pixel)
        super().__init__(self.length_pixel)
        self.grid_length = grid_length
        self.grid_width = grid_width
        self.exit_file_path = exit_file_path

    def save_images(self, grid_array, image_name):
        image = Image.fromarray(grid_array)

        if os.path.exists(self.exit_file_path) == False:
            os.mkdir(self.exit_file_path)

        image.save(self.exit_file_path + image_name + '.tif')
        print(f"The target  {image_name} has been created dans le dossier ' {self.exit_file_path} '.")

    def generate_grid_active(self, mean_intensity, amplitude, phase, image_name):
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
        # Generate base grid with regular fringes
        base_fringe = self.generate_sinusoidal_fringe(mean_intensity, amplitude, phase)
        grid_array = np.concatenate([np.concatenate([base_fringe] * self.grid_length, axis=1)] * self.grid_width, axis=0)

        # Save the resulting grid
        image_name = image_name + '_' + str(phase).zfill(3)
        self.save_images(grid_array, image_name)

    def generate_grid_active_VIC(self, mean_intensity, amplitude, phase, offset_X, offset_Y, length_X, length_Y, image_name):
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
        # Generate base grid with regular fringes
        base_fringe = self.generate_sinusoidal_fringe(mean_intensity, amplitude, phase)
        grid_array = np.concatenate([np.concatenate([base_fringe] * self.grid_length, axis=1)] * self.grid_width, axis=0)
        hole_fringe = self.generate_sinusoidal_fringe_with_hole(mean_intensity, amplitude, phase)

        # Positions of the three fringes with holes
        positions = [((offset_X - 1) * self.length_pixel, (offset_Y - 1) * self.length_pixel),              # First point
                     ((offset_X - 1) * self.length_pixel, (offset_Y - 1 + length_Y) * self.length_pixel),   # Second point
                     ((offset_X - 1 + length_X) * self.length_pixel, (offset_Y - 1) * self.length_pixel)]   # Third point

        for x, y in positions:
            if (x // self.length_pixel < self.grid_length and y // self.length_pixel < self.grid_width and x >= 0 and y >= 0 ):
                grid_array[y:y + self.length_pixel, x:x + self.length_pixel] = hole_fringe

        # Flip the grid vertically to start Y from the bottom
        grid_array = np.flipud(grid_array)

        # Save the resulting grid
        image_name = image_name + '_' + str(phase).zfill(3)
        self.save_images(grid_array, image_name)

    def generate_grid_passive(self, image_name):
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
        # Generate base grid with regular fringes
        base_fringe = self.generate_black_circle()
        grid_array = np.concatenate([np.concatenate([base_fringe] * self.grid_length, axis=1)] * self.grid_width, axis=0)

        # Save the resulting grid
        self.save_images(grid_array, image_name)

    def generate_grid_passive_VIC(self, offset_X, offset_Y, length_X, length_Y, image_name):
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
        # Generate base grid with regular fringes
        base_fringe = self.generate_black_circle()
        grid_array = np.concatenate([np.concatenate([base_fringe] * self.grid_length, axis=1)] * self.grid_width, axis=0)
        hole_fringe = self.generate_black_circle_with_hole()

        # Positions of the three fringes with holes
        positions = [((offset_X - 1) * self.length_pixel, (offset_Y - 1) * self.length_pixel),              # First point
                     ((offset_X - 1) * self.length_pixel, (offset_Y - 1 + length_Y) * self.length_pixel),   # Second point
                     ((offset_X - 1 + length_X) * self.length_pixel, (offset_Y - 1) * self.length_pixel)]   # Third point

        for x, y in positions[:3]:
            if (x // self.length_pixel < self.grid_length and y // self.length_pixel < self.grid_width and x >= 0 and y >= 0 ):
                grid_array[y:y + self.length_pixel, x:x + self.length_pixel] = hole_fringe

        # Flip the grid vertically to start Y from the bottom
        grid_array = np.flipud(grid_array)

        # Save the resulting grid
        self.save_images(grid_array, image_name)