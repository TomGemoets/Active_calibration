from Module import *
print("import réussi")
import subprocess
from PIL import Image
import pillow_heif
import cv2 as cv



def dimensions_chessboard():
    while True :
        try:
            col = int(input("combien de colonne voulez-vous ? : "))
            ligne = int(input("combien de lignes voulez-vous ? : "))
            return col, ligne
        except ValueError:
            print("Erreur : valeur non valide. Veuillez réessayer.")
if __name__ == "__main__":
    print("début de script")
    deck_passive_gauche = Deck('./Passive_deck_gauche.yaml')
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

    # Load passive samples images tooken from the left camera
    image_p_left = Read(deck_passive_gauche.path_target_image, deck_passive_gauche.name_image_left,deck_passive_gauche.extension).grab_image_files()

    # Cherche les coins pour chaque sample image left
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros(((col_chessboard-1) * (ligne_chessboard-1), 3), np.float32)
    objp[:, :2] = np.mgrid[0:col_chessboard-1, 0:ligne_chessboard-1].T.reshape(-1, 2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    
    for fname in image_p_left:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (col_chessboard-1, ligne_chessboard-1), None)
    
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
    
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)
    
            # Draw and display the corners
            cv.drawChessboardCorners(img, (7, 6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()