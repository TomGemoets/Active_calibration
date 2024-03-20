import yaml, sys
import numpy as np
import os.path

class Deck():
    """Read the inputs from the yaml file.

    Keyword argument:
    path of the yaml file
    
    Returns a dictionary of all the inputs
    """
    
    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)

                # Load grid parameters
                self.grid_parameters = self.doc['grid_parameters']
                self.grid_length = np.intc(self.grid_parameters['grid_length'])
                self.grid_width = np.intc(self.grid_parameters['grid_width'])

                # Load screen resolution
                self.screen_resolution = self.doc['screen_resolution']
                self.resolution_length = np.single(self.screen_resolution['resolution_length'])
                self.resolution_width = np.single(self.screen_resolution['resolution_width'])

                # Load fringe intensity properties
                self.fringe_intensities = self.doc['fringe_intensities']
                self.mean_pixel_value = np.single(self.fringe_intensities['mean_pixel_value'])
                self.sinusoidal_amplitude = np.single(self.fringe_intensities['sinusoidal_amplitude'])

                # Load phase properties
                self.phase_properties = self.doc['phase_properties']
                self.phase_shift = np.intc(self.phase_properties['phase_shift'])
                self.phase_number = np.intc(self.phase_properties['number'])

                # Load plate properties
                self.plate_properties = self.doc['plate_properties']
                self.grid_spacing = np.single(self.plate_properties['grid_spacing'])

                # Load image properties
                self.image_properties = self.doc['image_properties']
                self.name_image_left = self.image_properties['name_image_left']
                self.name_image_right = self.image_properties['name_image_right']
                self.path_target_image = self.image_properties['path_target_image']
                self.path_calibration_image = self.image_properties['path_calibration_image']
                self.extension = self.image_properties['extension']