import os
from itertools import product

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

    def rename_images_active(self):
        # Paramètres
        positions = [f"{i:02}" for i in range(13)]  # max 100 positions (00, 01, ..., 99)
        phases = ['000', '090', '180', '270']
        cameras = ['0', '1']

        # Liste tous les fichiers du dossier (fichiers seulement)
        files = [f for f in os.listdir(self.list_chemin_dossier[0]) if os.path.isfile(os.path.join(self.list_chemin_dossier[0], f))]

        # Trie les fichiers : d’abord par nom, puis par date de modification
        #sorted_files = sorted(files, key=lambda f: (f.lower(), os.path.getmtime(os.path.join(self.list_chemin_dossier[0], f))))
        sorted_files = sorted(files,key=lambda f: os.path.getmtime(os.path.join(self.list_chemin_dossier[0], f)), reverse = False)
        #sorted_files = files
        # Crée les nouveaux noms possibles (ordre défini)
        new_names = [f"{pos}_{ph}_{cam}" for pos, ph, cam in product(positions, phases, cameras)]
        print(new_names)

        # Vérifie qu’on ne dépasse pas le nombre de noms disponibles
        if len(sorted_files) > len(new_names):
            print(
                f"Erreur : trop de fichiers ({len(sorted_files)}) par rapport au nombre de noms possibles ({len(new_names)}).")
            return

        # Renommage
        for i, old_name in enumerate(sorted_files):
            ext = os.path.splitext(old_name)[1]  # Garde l'extension (.jpg, .png, etc.)
            new_name = new_names[i] + ext
            old_path = os.path.join(self.list_chemin_dossier[0], old_name)
            new_path = os.path.join(self.list_chemin_dossier[0], new_name)
            os.rename(old_path, new_path)

        print(f"{len(sorted_files)} fichiers renommés avec succès.")





