from Module import *
import subprocess
from PIL import Image
import pillow_heif
import cv2 as cv

# Load yamlfile
deck = Deck('./deck.yaml')
deck_passive_gauche = Deck('./Passive_deck_gauche.yaml')
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

def choix_calibration():
    choix_valide = ['p', 'passive', 'a', 'active']
    while True:
        passive_ou_active = input("Souhaitez-vous réaliser de la calibration passive ou active ?(p/a) : ")
        if passive_ou_active in choix_valide:
            return choix_valide
        else :
            print("Vous avez encoder une mauvaise valeur, veuillez réessayer.")
def dimensions_chessboard():
    while True :
        try:
            """col = int(input("combien de colonne voulez-vous ? : "))
            ligne = int(input("combien de lignes voulez-vous ? : "))"""
            col = 6
            ligne = 7
            return col, ligne
        except ValueError:
            print("Erreur : valeur non valide. Veuillez réessayer.")

if __name__ == '__main__':
    #Demande à l'utilisateur s'il veut faire de la calibration Passive ou Active
    #methode_de_calibration = choix_calibration()
    methode_de_calibration = 'p'

    # -----------------Calibration active uniquement----------------------------------
    # Create circular grid target
    if methode_de_calibration == 'a' or methode_de_calibration == 'active':
        print("methode active")
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
    # -----------------Calibration active uniquement----------------------------------

    # ------------------Calibration passive uniquement----------------------------------
    else: #faire la calib passive
        # Génération du chessboard
        col_chessboard, ligne_chessboard = dimensions_chessboard()
        cmd = [
            "python",
            "Module/chessboard generation/gen_pattern.py",
            "-o", "chessboard.svg",
            "-r", str(ligne_chessboard),
            "-c", str(col_chessboard),
            "--type", "checkerboard",
            "-s", str(20)
        ]
        subprocess.run(cmd)

        # renommer (et reformater) les images par téléphone (IPhone) pour la calib passive    JE NE PARVIENS PAS A CHANGER LE FORMAT, JUSTE LE NOM
        chemin_photos_gauche = r"C:\Users\patri\PycharmProjects\Active_calibrationV2\Images_calib_passive_gauche"
        extensions = ['.jpg', '.jpeg', '.png', '.heic']
        # compteur = 0
        position = 0
        for nom_fichier in os.listdir(chemin_photos_gauche):
            nom_complet = os.path.join(chemin_photos_gauche, nom_fichier)

            if os.path.isfile(nom_complet):
                _, ext = os.path.splitext(nom_fichier)
                if ext.lower() in extensions:
                    ext = '.jpg'
                    nouveau_nom_fichier = f"{position:03d}_0{ext}"
                    nouveau_chemin = os.path.join(chemin_photos_gauche, nouveau_nom_fichier)
                    os.rename(nom_complet, nouveau_chemin)
                    print(f"{nom_fichier} → {nouveau_nom_fichier}")
                    position += 1

        image_p_left = Read(deck_passive_gauche.path_target_image, deck_passive_gauche.name_image_left,
                        deck_passive_gauche.extension).grab_image_files()

        # Cherche les coins pour chaque sample image left
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros(((col_chessboard - 1) * (ligne_chessboard - 1), 3), np.float32)
        objp[:, :2] = np.mgrid[0:col_chessboard - 1, 0:ligne_chessboard - 1].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        for fname in image_p_left:
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, (col_chessboard - 1, ligne_chessboard - 1), None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
            elif ret == False:
                print("rien trouvé")

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (col_chessboard - 1, ligne_chessboard - 1), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
        cv.destroyAllWindows()

    # ------------------Calibration passive uniquement----------------------------------

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

