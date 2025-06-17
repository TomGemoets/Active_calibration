from Module import *

# Load yamlfile
deck = Deck('./deck.yaml')
print(deck)

# Get values from the yaml
length_single_fringe = np.minimum(deck.resolution_length / deck.grid_length, deck.resolution_width / deck.grid_width)
mean_pixel_value = deck.mean_pixel_value
amplitude = deck.sinusoidal_amplitude
phase_shift = deck.phase_shift
phase_number = deck.phase_number
grid_length = deck.grid_length
grid_width = deck.grid_width
dot_grid_size = (deck.grid_length, deck.grid_width)
dot_grid_spacing = deck.grid_spacing

def calculate_four_phase_camera(list_image, phase_number):
    count = 0
    while count < len(list_image)/phase_number:
        group_four_images = list_image[count * phase_number : (count+1) * phase_number]
        four_phase_image = FourPhase(group_four_images).calculate_four_phase_shifting()
        count += 1


if __name__ == '__main__':
    # Create circular grid target
    for each_phase_number in np.arange(phase_number):
        phase = phase_shift * each_phase_number
        target_grid = TargetGrid(length_single_fringe, mean_pixel_value, amplitude, phase, grid_length, grid_width, 'target').generate_grid_target()
    print('Grid targets are saved in the folder "Target_images".\n')

    # Load active target images from the camera left and right
    image_left = Read(deck.path_target_image, deck.name_image_left, deck.extension).grab_image_files()
    image_right = Read(deck.path_target_image, deck.name_image_right, deck.extension).grab_image_files()

    # Perform the four phase shift for all images
    calculate_four_phase_camera(image_left, phase_number)
    print('Four-phase shifting for the images from the left camera: done!')
    calculate_four_phase_camera(image_right, phase_number)
    print('Four-phase shifting for the images from the right camera: done!\n')

    # Load calibration image
    calibration_image_left = Read(deck.path_calibration_image, deck.name_image_left, deck.extension).grab_image_files()
    calibration_image_right = Read(deck.path_calibration_image, deck.name_image_right, deck.extension).grab_image_files()
    print('Performing the stereo-calibration...\n')
    # Calibrate camera left
    camera_left = Camera(dot_grid_size, dot_grid_spacing, calibration_image_left)
    calibration_left = camera_left.calibrate()

    # Calibrate camera right
    camera_right = Camera(dot_grid_size, dot_grid_spacing, calibration_image_right)
    calibration_right = camera_right.calibrate()

    # Perform stereo calibration
    stereo_setup = StereoCameras(calibration_left, calibration_right)
    stereo_parameters = stereo_setup.stereo_calibrate()

    # Export to XML file
    ExportToXML(stereo_parameters[0], stereo_parameters[1], stereo_parameters[2], stereo_parameters[3], stereo_parameters[6], stereo_parameters[5]).write_XML()
    ExportToXML(stereo_parameters[0], stereo_parameters[1], stereo_parameters[2], stereo_parameters[3], stereo_parameters[6], stereo_parameters[5]).write_XML_VIC([[0,0,0],[0,0,0]])
