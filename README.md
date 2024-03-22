# Active_calibration
Python package to perform an active calibration using sinusoidal circular fringe targets.

*This software is for research purposes only.*

# Background
## Stereo-calibration

Stereo calibration involves determining the intrinsic, extrinsic parameters, and distortion coefficients for each camera, providing a comprehensive description of their positions and orientations relative to objects in space. 
The standard procedure begins by simultaneously capturing sets of images of a known calibration pattern, typically a checkerboard or circular grid pattern, from various orientations and positions using the cameras. 
An algorithm detects the calibration pattern features in each image.
The detection principle aims to identify key points, such as corners in a checkerboard or centers of circles in a circular grid pattern, by analyzing the intensity of pixels within a circular region surrounding each pixel.
Generally, circular grid patterns tend to provide more stable, robust, and redundant detection in computer vision due to their geometric characteristics.
Assuming that each circle is well-defined and covers a sufficient number of pixels in the image, the distribution of intensities surrounding each circle's center would indeed be denser than the distribution around a single intersecting point in the case of a checkerboard.
This denser distribution can offer a more robust detection of circular features, making it easier to accurately compute each center of the circles.
A general guideline mentions that each circle should cover at least 10 pixels.
From the detected position $(x_{distorted}, y_{distorted})$ of each feature of the calibration pattern in each image, the distortion coefficients $(k_1, k_2, p_1, p_2, k_3)$ can be estimated from across multiple images:

**For the radial distortion:**
```math
\begin{equation}
\begin{split}
    x_{distorted} = x (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)\\
    y_{distorted} = y (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)
\end{split}
\end{equation}
```

**For the tangential distortion:**
```math
\begin{equation}
\begin{split}
    x_{distorted} = x + (2 p_1 x y + p_2 (r^2 + 2 x^2))\\
    y_{distorted} = y + (p_1 (r^2 + 2 y^2) + 2 p_2 x y)
\end{split}
\end{equation}
```
with $(k_1, k_2, p_1, p_2, k_3)$, denoting the distortion coefficients accounting for the radial on tangential distortions.


Once these coefficients are determined, the intrinsic and extrinsic parameters of each camera, along with their relative orientation and position, can be obtained. 
This is achieved through the utilization of the linear camera model and a triangulation algorithm that establishes a relationship between the 3D coordinates of points in the calibration pattern, considering the known geometry of the pattern, and their corresponding 2D coordinates in the image.

Let $(X, Y, Z)$, be the 3D coordinates of an object point, and $(x, y)$, be the coordinates of the image point on the sensor plane.

**Linear camera model:**
```math
\begin{equation}
    \begin{bmatrix}
    x\\[6pt]
    y\\[6pt]
    1
    \end{bmatrix}
    =
    \begin{bmatrix}
        f_x & 0 & c_x\\[6pt]
        0 & f_y & c_y\\[6pt]
        0 & 0   &  1
    \end{bmatrix}
    \cdot
    \begin{bmatrix}
    X \\[6pt]
    Y \\[6pt]
    Z
    \end{bmatrix}
\end{equation}
```

with, $f_x = S_x f$ and $f_y = S_y f$, the focal lengths in pixels along the $x$ and $y$ axis of the sensor plane.

This approach of using a calibration target is the most common and widely adopted due to the ease of creating such a target.
Nevertheless, it comes with notable drawbacks that will be detailed below.

## Active calibration and four-phase shifting method

The active calibration method employs specialized active targets to enhance the calibration process. 
These targets utilize structured-light schemes that can be projected onto a screen. 
One potential active target includes a phase-shifted circular fringe pattern, replicating the conventional circular grid pattern. 
Within this pattern, the intensity of each fringe varies sinusoidally.
Additionally, the pattern displayed on the target undergoes four distinct phase shifts $\phi_i$ with $i = [1, 2, 3, 4]$.
By capturing multiple images of a stable target undergoing phase shifts of $[0, \pi/2, \pi, 3\pi/2]$, the four-phase shifting method enables the reconstruction of a virtual circular grid pattern in the phase map $\Phi$ corresponding to the specific position and orientation of the target relative to the cameras.
Let, $I_i (x, y)$ be the light intensity at pixel coordinates $(x, y)$ in the $i$-th phase shift.
The phase map $\Phi (x,y)$ is obtained from a simple mathematical expression written bellow:

**Four-phase shifting equation:**
```math
\begin{equation}
\begin{split}
    \Phi (x,y) = \textbf{F[}  I_4 (x, y) - I_2 (x, y), I_1 (x, y) - I_3 (x, y) \textbf{]}
\end{split}
\end{equation}
```

with $I_1 (x, y) - I_3 (x, y) \neq 0$,

```math
\begin{equation*}
    \textbf{F[x, y]} = 
        \begin{cases}
            arctan( \textbf{x} / \textbf{y}) & \text{if $\textbf{x} \geq 0$ and $\textbf{y} > 0$,}\\
            \pi - arctan( \textbf{x} / \textbf{y}) & \text{if $\textbf{x} \geq 0$ and $\textbf{y} < 0$,}\\
            \pi + arctan( \textbf{x} / \textbf{y}) & \text{if $\textbf{x} < 0$ and $\textbf{y} < 0$,}\\
            - arctan( \textbf{x} / \textbf{y}) & \text{if $\textbf{x} < 0$ and $\textbf{y} > 0$.}
        \end{cases}
\end{equation*}
```

With $I_1 (x, y) - I_3 (x, y) = 0$,

```math
\begin{equation*}
    \textbf{F[x, y]} = 
        \begin{cases}
            \pi/2 & \text{if $\textbf{x} > 0$,}\\
            3 \pi/2 & \text{if $\textbf{x} < 0$,}\\
            0 & \text{if $\textbf{x} = 0$.}
        \end{cases}
\end{equation*}
```

The multiple-phase maps from sets of four-phase shifted images for different target positions and orientations can then be obtained. 
These maps featuring the virtual circular grid pattern can then be used for the stereo calibration of the cameras.

## Advantage of active calibration

For an accurate 3D reconstruction, the conventional calibration patterns, such as checkerboards or grids, should have clear and well-defined features in the collected images, ensuring all pattern features are within the depth of field of the cameras for proper focus. 
The images should cover a wide range of pattern orientations and positions within the fields of view, ideally covering at least 1/3 of the field of view. 
Proper positioning and alignment of the cameras relative to each other and the scene are crucial, necessitating overlapping fields of view and minimal distortion.
For large objects, which necessitate a substantial field of view and depth of field to ensure proper focus, this process can become laborious. 
For instance, if the object spans 10 meters in width, the calibration target should ideally extend at least 3 meters in width to cover 1/3 of the field of view. 
The orientation and positioning of such a sizable target may pose significant challenges.
Another factor arises with conventional patterns from detecting features themselves and the lighting conditions of the scene in which images are acquired.
The estimation of each key point may be misled by reflections, shadows, or light variations across the images.
Overall, while calibration is essential for ensuring accurate and reliable performance in computer vision and imaging systems, the standard procedure also comes with various challenges and limitations that need to be carefully considered and addressed in practice.
On the other hand, the active calibration that utilizes active targets tackles these challenges.
This method offers several advantages over the conventional ones. 
One key advantage is the ability to maintain accuracy even in challenging imaging conditions, such as defocusing. 
Additionally, active targets provide more robust detection of features, as the patterns are designed to be highly distinguishable and less affected by environmental factors.
Overall, active calibration with the four-phase shifting method and active targets enhances the accuracy and reliability of the calibration process, particularly in scenarios where traditional methods may struggle.

# Main features

All the preceding sections aimed to describe the method of stereo calibration with a conventional or active target. 
To achieve this, the camera model, the effect of distortion, and the calibration procedure were explained. 
A whole section was dedicated to active calibration and its formulation to understand its operation for the subsequent steps. 
The goal of this project is to develop a comprehensive Python package facilitating active calibration of a stereo system consisting of two cameras and obtaining a 3D reconstruction of the captured scene.
The current features of this toolkit are:

- [x] Create active targets composed of sinusoidal circular fringes of phase-shifts $[0, \pi/2, \pi, 3\pi/2]$, 
- [x] Perform the four-phase shifting method,
- [x] Perform the stereo-calibration,
- [x] Export the results in an XML file,
- [ ] Visualisation of the results.


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

## How it works...

The first feature enables the generation of images of the circular fringe patterns for different phase shifts by specifying the pattern's geometry. 
For example, entering `grid_length: 6` and `grid_width: 3` would yield four images of a 3x6 circular fringe pattern shifted at $[0, \pi/2, \pi, 3\pi/2]$, ready for display on a screen of resolution `resolution_length: 2388`, `resolution_width: 1668`.
To perform the four-phase shifting method and the stereo-calibration of two cameras, the user will provide images from both cameras of the previously generated active targets from various positions and orientations. The images should be named as the following:

Example: *00_270_0.tif* and *00_270_1.tif*

- *00*: set of two images corresponding to one orientation of the active target,
- *270*: the phase shift of the target in degrees,
- *0* or *1*: the camera number. *0* is the left camera and *1* is the right one,
- *tif*: is the image format. This one need to match the one provided in the `deck.yaml` file `extension: .tif`.

The script will organize these images into sets of four images with different phase shifts $[0, \pi/2, \pi, 3\pi/2]$. 
This facilitates the generation of phase maps for each position and orientation of the active target using the four-phase shifting algorithm.
Subsequently, the script will deduce the intrinsic/extrinsic parameters of each camera, distortion coefficients, and the relationship of the cameras using the phase maps obtained and saved in the folder "Four_phase_images".
A module `Export` will then export the results in an XML file for further uses.

## Contributes?

This package doesn't provide a visualization tool of the 3D reconstructed scene. If you need this feature, here are some guidelines to do so:

- With extrinsic parameters, rectify the orientation of one camera so corresponding points lie on the same scanlines,
- Find corresponding points using a stereo matching algorithm,
- Compute the 3D coordinates of matching points with the intrinsic parameters,
- Create a scatter plot of the 3D coordinates.

If you would like to contribute, modify, improve the script, give feedbacks, I'll be happy to hearing from you. Please leave an Issue or a pull request.
