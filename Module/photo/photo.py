import os

class DossierPhoto:
    def __init__(self, list_chemin_dossier, list_extension):
        self.list_chemin_dossier = list_chemin_dossier
        self.list_extension = list_extension

    '''
    Cette méthode permet de renommer chaque image stockée dans le dossier de photos de la caméra gauche et droite
    
    Chaque image dans l'ordre seront identifiées par un numéro correspondant à la variable "position"
    
    Les images de gauche prendrons le suffixe _0 
    Les images de droite prendrons le suffixe _1 
    
    Ce code change le format de l'image dans l'explorateur de fichier mais pour le bon fonctionnement de l'exécution il est
    conseillé de modifier le format de l'image à l'origine par un format qui est lisible par PyCharm
    
    retourn 
    '''
    def renommer_images(self):
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



