import pandas as pd
import random
from datetime import datetime, timedelta

# === Paramètres ===
n_je = 100
anomaly_ratio = 0.1

accounts = [1000, 1104, 1151, 1198, 2264, 3106, 4010, 5121, 6061]
sources = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
companies = ['C' + str(i) for i in range(1, 10)]
fy_label = '2024-01-01 – 2024-12-31'
fy_start = datetime(2024, 1, 1)
fy_end = datetime(2024, 12, 31)

# === Fonctions ===
def random_valid_date():
    return (fy_start + timedelta(days=random.randint(0, (fy_end - fy_start).days))).strftime('%Y-%m-%d')

def random_invalid_date():
    # Date hors de l'année fiscale : avant ou après
    if random.random() < 0.5:
        return (fy_start - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d')
    else:
        return (fy_end + timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d')

# === Génération ===
entries = []

for i in range(1, n_je + 1):
    je_no = f"JE-{i}"
    is_anomalous = random.random() < anomaly_ratio
    fabricated_je = 1 if is_anomalous else 0
    anomaly_type = 3 if is_anomalous else 0
    eff_date = random_invalid_date() if is_anomalous else random_valid_date()

    src = random.choice(sources)
    comp = random.choice(companies)
    montant = round(random.uniform(1000, 10000), 2)

    debit_account = random.choice(accounts)
    credit_account = random.choice(accounts)

    # Écriture en deux lignes
    entries.append({
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': debit_account,
        'AMOUNT': montant,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy_label,
        'Fabricated_JE': fabricated_je,
        'TYPE': anomaly_type
    })
    entries.append({
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': credit_account,
        'AMOUNT': -montant,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy_label,
        'Fabricated_JE': fabricated_je,
        'TYPE': anomaly_type
    })

# === Export ===
df = pd.DataFrame(entries)
df.to_csv("journal_avec_anomalie_type3.csv", index=False)
print(f"Fichier généré avec succès : {df['Fabricated_JE'].sum()} écritures anormales sur {n_je}")
