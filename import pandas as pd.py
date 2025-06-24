import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#  Remplace par le chemin de ton fichier CSV
df = pd.read_csv("DROP_FREATURES.csv")

#  Calcul de la matrice de corrélation
correlation_matrix = df.corr(numeric_only=True)

#  Affichage avec seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Matrice de corrélation")
plt.tight_layout()
plt.show()
