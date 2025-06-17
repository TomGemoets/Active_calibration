import glob
import os

class Read():
    def __init__(self, path_file, camera_name, extension):
        self.path_file = path_file
        self.camera_name = camera_name
        self.extension = extension
    
    def grab_image_files(self):
        """Grab all the images from in camera in a folder

        Keyword arguments:
        path_file -- path of where the images are located
        camera_name -- name of the camera i.e. '_0' is the left camera, '_1' is the right camera
        extension -- extension of the images i.e. '.tif', '.png' etc...

        Returns a list of all the image names from one camera.
        """
        if os.path.exists('./' + self.path_file):
            path = self.path_file + '/*' + self.camera_name + self.extension
            image = glob.glob(path)
            image.sort()

            if not image:
                print('Please load the calibration images in the folder "Pre_Phase_Mapping_images" to perform the active calibration.\n')
                exit()
            else:
                return image
        else:
            os.mkdir('./' + self.path_file)
            print('A folder "Pre_Phase_Mapping_images" has been created to load the images of the active target for the calibration.')
            print('Please load the calibration images in this folder to perform the active calibration.\n')
            exit()





