import os

class DossierPhoto:
    def __init__(self, list_chemin_dossier, list_extension):
        self.list_chemin_dossier = list_chemin_dossier
        self.list_extension = list_extension

    def renommer_images(self):
        """
        Rename each image from the left and right directory indicating the position and the camera left/right

        The images on the left will have the suffix _0
        The Images on the right will have the suffixed _1

        """
        camera = -1
        for chemin in self.list_chemin_dossier:
            # compteur = 0
            position = 0
            camera += 1  # caméra gauche
            for nom_fichier in os.listdir(chemin):
                nom_chemin_complet = os.path.join(chemin, nom_fichier)
                if os.path.isfile(nom_chemin_complet):
                    _, ext = os.path.splitext(nom_fichier)
                    if ext.lower() in self.list_extension:
                        ext = '.jpg'
                        nouveau_nom_fichier = f"{position:03d}_{camera}{ext}"
                        nouveau_chemin_complet = os.path.join(chemin, nouveau_nom_fichier)
                        os.rename(nom_chemin_complet, nouveau_chemin_complet)
                        print(f"{nom_fichier} → {nouveau_nom_fichier}")
                        position += 1



