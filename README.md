# Active_calibration
Python package to perform an active calibration using sinusoidal circular fringe targets.

# Main features

- [x] Create the targets
- [x] Perform the four-phase shifting method
- [x] Perform the stereo-calibration
- [x] Export the results in an XML file
- [ ] Visualisation of the results

# Getting started

## Packages and modules installation

To run Active_calibration, the following softwares are required: 
* Python 3.12 or higher
* python3-pip
* python3-venv

Several packages and modules are required. A list is provided in `requirements.txt`. These packages can be installed using pip.
A clean virtual environment is recommended to avoid any conflict between versions of already existing on your computer.

To create a new virtual environment `.venv`, run the following commands in your terminal:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt 
```

## Usage

This package requires images of the active target in the folder "Calibration_images" and a valid `deck.yaml` file to run.
An example of calibration images is provided in the current folder.

To execute the package:
```
python main.py
```

## deck.yaml

Here is the structure of the yaml file:

```yaml
grid_parameters:
  grid_length: 6 # number of fringes
  grid_width: 3 # number of fringes

screen_resolution:
  resolution_length: 2388 # number of pixels of the screen where the targets are displayed
  resolution_width: 1668  # number of pixels of the screen where the targets are displayed

fringe_intensities: # pixels intensities set by default
  mean_pixel_value: 160 # mean intensity of a circular fringe
  sinusoidal_amplitude: 80 # amplitude of the sinusoidal pattern

phase_properties:
  phase_shift: 90 #deg
  number: 4       # four shifts in total

plate_properties:
  grid_spacing: 80 #mm

image_properties:
  name_image_left: _0 # suffix for images from the left camera
  name_image_right: _1 # suffix for images from the right camera
  path_target_image: Calibration_images # file where images of the active targets are saved
  path_calibration_image: Four_phase_images # file where images of the phase maps are saved
  extension: .tif
```

