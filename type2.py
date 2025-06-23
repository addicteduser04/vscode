import pandas as pd
import random
from datetime import datetime, timedelta

# === Paramètres ===
n_je = 100
anomaly_ratio = 0.1
valid_accounts = [1000, 1104, 1151, 1198, 2264, 3106, 4010, 5121, 6061]  # comptes valides
invalid_accounts = [9999, 123, 8888, 4321, 777, 1, 98765]  # comptes invalides ou douteux

sources = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
companies = ['C' + str(i) for i in range(1, 10)]
fy = '2024-01-01 – 2024-12-31'

# === Fonctions ===
def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

# === Génération des écritures ===
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
    anomaly_type = 2 if is_anomalous else 0

    # Choix des comptes
    if is_anomalous:
        debit_account = random.choice(invalid_accounts)
        credit_account = random.choice(valid_accounts)
    else:
        debit_account = random.choice(valid_accounts)
        credit_account = random.choice(valid_accounts)

    montant = round(random.uniform(1000, 10000), 2)

    # Écriture à 2 lignes (débit et crédit)
    entries.append({
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': debit_account,
        'AMOUNT': montant,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy,
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
        'FY': fy,
        'Fabricated_JE': fabricated_je,
        'TYPE': anomaly_type
    })

# === Export ===
df = pd.DataFrame(entries)
df.to_csv("journal_avec_anomalie_type2.csv", index=False)
print(f"Fichier généré avec succès : {df['Fabricated_JE'].sum()} écritures anormales sur {n_je}")
