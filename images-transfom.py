import os
from pillow_heif import register_heif_opener
from PIL import Image

# Enregistre HEIC comme format lisible par PIL
register_heif_opener()

# Dossiers source et destination
input_folder = "dossier_heic"
output_folder = "dossier_tif"

# Créer le dossier de sortie s’il n’existe pas
os.makedirs(output_folder, exist_ok=True)

# Conversion en lot
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".jpeg"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".tif"
        output_path = os.path.join(output_folder, output_filename)

        try:
            # Ouvre l'image HEIC
            img = Image.open(input_path)

            # Convertit en niveaux de gris (grayscale)
            gray_img = img.convert("L")  # "L" = 8-bit grayscale

            # Sauvegarde en TIFF
            gray_img.save(output_path, format="TIFF")
            print(f"✅ {filename} → {output_filename}")

            # Optionnel : supprimer le fichier HEIC original
            # os.remove(input_path)
        except Exception as e:
            print(f"❌ Erreur pour {filename} : {e}")
