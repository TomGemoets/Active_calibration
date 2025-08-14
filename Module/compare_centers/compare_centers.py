import pandas as pd
import numpy as np

# === 1. Lire les fichiers CSV ===
"""csv_path_p = "centres_detectes_passive_superposée.csv"
csv_path_a = "centres_detectes_active_classique.csv"""
csv_path_p = "centres_detectes_p.csv"
csv_path_a = "centres_detectes_a.csv"

csv_path = "comparaison_centres.csv"
empty_df = pd.DataFrame(columns=["x_ref", "y_ref", "dx","dy", "distance", ])
empty_df.to_csv(csv_path, index=False)
print(f"Fichier '{csv_path}' réinitialisé.")

df_p = pd.read_csv(csv_path_p)
df_a = pd.read_csv(csv_path_a)

# === 2. Vérifier la compatibilité ===
if df_p.shape != df_a.shape:
    raise ValueError("Les deux fichiers n'ont pas la même taille.")

if not (df_p.columns == df_a.columns).all():
    raise ValueError("Les deux fichiers n'ont pas les mêmes colonnes.")

# === 3. Comparer les positions ===
diff_x = df_p["x"] - df_a["x"]
diff_y = df_p["y"] - df_a["y"]
distances = np.sqrt(diff_x**2 + diff_y**2)

# === 4. Ajouter les différences dans un DataFrame ===
comparison = df_p.copy()
comparison["x_ref"] = df_a["x"]
comparison["y_ref"] = df_a["y"]
comparison["dx"] = diff_x
comparison["dy"] = diff_y
comparison["distance"] = distances

# === 5. Statistiques ===
print("Comparaison terminée.")
print(f"Nombre de points : {len(distances)}")
print(f"Erreur moyenne (pixels) : {distances.mean():.2f}")
print(f"Erreur maximale (pixels) : {distances.max():.2f}")
print(f"Erreur minimale (pixels) : {distances.min():.2f}")

# === 6. Exporter le résultat ===
comparison.to_csv("comparaison_centres.csv", index=False)
print("Fichier de comparaison sauvegardé sous 'comparaison_centres.csv'.")