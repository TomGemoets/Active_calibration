from Module import *
import subprocess
from PIL import Image
import pillow_heif
import cv2 as cv

def calculate_four_phase_camera(list_image, phase_number):
    count = 0
    while count < len(list_image)/phase_number:
        group_four_images = list_image[count * phase_number : (count+1) * phase_number]
        four_phase_image = FourPhase(group_four_images).calculate_four_phase_shifting()
        count += 1

def choix_calibration():
    choix_valide = ['p', 'passive', 'a', 'active']
    while True:
        passive_ou_active = input("Souhaitez-vous réaliser de la calibration passive ou active ?(p/a) : ")
        if passive_ou_active in choix_valide:
            return passive_ou_active
        else :
            print("Vous avez encoder une mauvaise valeur, veuillez réessayer.")
def dimensions_chessboard():
    while True :
        try:
            col = 6
            ligne = 7
            return col, ligne
        except ValueError:
            print("Erreur : valeur non valide. Veuillez réessayer.")

if __name__ == '__main__':
    #Demande à l'utilisateur s'il veut faire de la calibration Passive ou Active
    methode_de_calibration = choix_calibration()
    #methode_de_calibration = 'a'

    # -----------------Calibration active uniquement----------------------------------
    # Create circular grid target
    if methode_de_calibration == 'a' or methode_de_calibration == 'active':
        print("Début de la calibration active")
        print("methode active")
        # Load yamlfile
        deck = Deck('./deck.yaml',methode_de_calibration)
        print(deck)
        # Get values from the yaml
        length_single_fringe = np.minimum(deck.resolution_length / deck.grid_length,
                                          deck.resolution_width / deck.grid_width)
        mean_pixel_value = deck.mean_pixel_value
        amplitude = deck.sinusoidal_amplitude
        phase_shift = deck.phase_shift
        phase_number = deck.phase_number
        grid_length = deck.grid_length
        grid_width = deck.grid_width
        dot_grid_size = (deck.grid_length, deck.grid_width)
        dot_grid_spacing = deck.grid_spacing

        for each_phase_number in np.arange(phase_number):
            phase = phase_shift * each_phase_number
            target_grid = TargetGrid(length_single_fringe, mean_pixel_value, amplitude, phase, grid_length, grid_width,
                                     'target').generate_grid_target()
        print('Grid targets are saved in the folder "Target_images".\n')

        # Create circular grid target
        for each_phase_number in np.arange(phase_number):
            phase = phase_shift * each_phase_number
            target_grid = TargetGrid(length_single_fringe, mean_pixel_value, amplitude, phase, grid_length, grid_width,
                                     'target').generate_grid_target()
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
        calibration_image_left = Read(deck.path_active_calibration_image, deck.name_image_left,
                                      deck.extension).grab_image_files()
        calibration_image_right = Read(deck.path_active_calibration_image, deck.name_image_right,
                                       deck.extension).grab_image_files()
        print('Performing the stereo-calibration...\n')
        # Calibrate camera left
        camera_left = CameraActive(calibration_image_left,dot_grid_size, dot_grid_spacing)
        list_object_points, list_image_points, image_gray, stock_image = camera_left.detect_centers()
        #calibration_left = camera_left.calibrate(list_object_points, list_image_points, image_gray, stock_image)

        # Calibrate camera right
        camera_right = CameraActive(calibration_image_right, dot_grid_size, dot_grid_spacing) #problème ici
        list_object_points, list_image_points, image_gray, stock_image = camera_right.detect_centers()
        #calibration_right = camera_right.calibrate(list_object_points, list_image_points, image_gray, stock_image)
    # -----------------Calibration active uniquement----------------------------------

    # ------------------Calibration passive uniquement----------------------------------
    else: #faire la calib passive
        print("Début de la calibration passive")
        # Load yamlfile
        deck = Deck('./deck_passive.yaml',methode_de_calibration)
        print(deck)

        chess_columns = deck.chess_columns
        chess_lines = deck.chess_lines

        # Génération du chessboard
        #col_chessboard, ligne_chessboard = dimensions_chessboard()
        chessboard = ChessboardGrid('chessboard',chess_columns,chess_lines)
        chessboard.define_chessboard_target()

        # renommer (et reformater) les images par téléphone (IPhone) pour la calib passive    JE NE PARVIENS PAS A CHANGER LE FORMAT, JUSTE LE NOM
        list_chemin_photos = []
        chemin_photos_gauche = r"C:\Users\patri\PycharmProjects\Active_calibrationV2\Images_calib_passive_gauche"
        list_chemin_photos.append(chemin_photos_gauche)
        chemin_photos_droite = r"C:\Users\patri\PycharmProjects\Active_calibrationV2\Images_calib_passive_droite"
        list_chemin_photos.append(chemin_photos_droite)
        extensions = ['.jpg', '.jpeg', '.png', '.heic']

        camera = -1
        for chemin in list_chemin_photos:
            # compteur = 0
            position = 0
            camera += 1 #caméra gauche
            for nom_fichier in os.listdir(chemin):
                nom_chemin_complet = os.path.join(chemin, nom_fichier)
                if os.path.isfile(nom_chemin_complet):
                    _, ext = os.path.splitext(nom_fichier)
                    if ext.lower() in extensions:
                        ext = '.jpg'
                        nouveau_nom_fichier = f"{position:03d}_{camera}{ext}"
                        nouveau_chemin_complet = os.path.join(chemin, nouveau_nom_fichier)
                        os.rename(nom_chemin_complet, nouveau_chemin_complet)
                        print(f"{nom_fichier} → {nouveau_nom_fichier}")
                        position += 1

        image_p_left = Read(deck.path_left_calibration_image, deck.name_image_left,
                                      deck.extension).grab_image_files()
        image_p_right = Read(deck.path_right_calibration_image, deck.name_image_right,
                        deck.extension).grab_image_files()
        camera_left = CameraPassive(image_p_left)
        list_object_points, list_image_points, image_gray, stock_image = camera_left.find_corners(chess_columns, chess_lines)
        camera_right = CameraPassive(image_p_right)
        list_object_points, list_image_points, image_gray, stock_image = camera_right.find_corners(chess_columns, chess_lines)

    #-------------------Calibration passive uniquement----------------------------------

    calibration_left = camera_left.calibrate(list_object_points, list_image_points, image_gray, stock_image)
    calibration_right = camera_right.calibrate(list_object_points, list_image_points, image_gray, stock_image)

    # Perform stereo calibration
    stereo_setup = StereoCameras(calibration_left, calibration_right)
    stereo_parameters = stereo_setup.stereo_calibrate()

    # Export to XML file
    ExportToXML(stereo_parameters[0], stereo_parameters[1], stereo_parameters[2], stereo_parameters[3], stereo_parameters[6], stereo_parameters[5]).write_XML()
    ExportToXML(stereo_parameters[0], stereo_parameters[1], stereo_parameters[2], stereo_parameters[3], stereo_parameters[6], stereo_parameters[5]).write_XML_VIC([[0,0,0],[0,0,0]])
