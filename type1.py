import pandas as pd
import random
from datetime import datetime, timedelta

# === Paramètres ===
n_je = 100        # Nombre total d'écritures JE_NO
anomaly_ratio = 0.1  # 10% d'anomalies de type 1
accounts = [1000, 1104, 1151, 1198, 2264, 3106, 4010, 5121, 6061]
sources = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
companies = ['C' + str(i) for i in range(1, 10)]
fy = '2024-01-01 – 2024-12-31'

# === Fonctions utilitaires ===
def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

# === Génération ===
entries = []
date_start = datetime(2024, 1, 1)
date_end = datetime(2024, 12, 31)

for i in range(1, n_je + 1):
    je_no = f"JE-{i}"
    eff_date = random_date(date_start, date_end)
    src = random.choice(sources)
    comp = random.choice(companies)
    
    is_anomalous = random.random() < anomaly_ratio
    fabricated_je = 1 if is_anomalous else 0
    anomaly_type = 1 if is_anomalous else 0

    # Montants
    debit = round(random.uniform(1000, 10000), 2)
    credit = round(debit, 2)

    if is_anomalous:
        # On modifie le crédit pour créer un déséquilibre
        credit += random.choice([-1, 1]) * round(random.uniform(1, 500), 2)
    
    # Deux lignes : une pour le débit, une pour le crédit
    entries.append({
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': random.choice(accounts),
        'AMOUNT': debit,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy,
        'Fabricated_JE': fabricated_je,
        'TYPE': anomaly_type
    })
    entries.append({
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': random.choice(accounts),
        'AMOUNT': -credit,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy,
        'Fabricated_JE': fabricated_je,
        'TYPE': anomaly_type
    })

# === Export ===
df = pd.DataFrame(entries)
df.to_csv("journal_avec_anomalie_type1.csv", index=False)
print(f"Fichier généré avec succès : {df['Fabricated_JE'].sum()} écritures anormales sur {n_je}")
