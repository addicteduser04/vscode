import pandas as pd
import random
from datetime import datetime, timedelta
import copy

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
def random_date():
    return (fy_start + timedelta(days=random.randint(0, (fy_end - fy_start).days))).strftime('%Y-%m-%d')

# === Génération des écritures normales ===
entries = []
clean_entries = []

for i in range(1, n_je + 1):
    je_no = f"JE-{i}"
    eff_date = random_date()
    src = random.choice(sources)
    comp = random.choice(companies)
    montant = round(random.uniform(1000, 10000), 2)
    debit_account = random.choice(accounts)
    credit_account = random.choice(accounts)

    entry_debit = {
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': debit_account,
        'AMOUNT': montant,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy_label,
        'Fabricated_JE': 0,
        'TYPE': 0
    }
    entry_credit = {
        'JE_NO': je_no,
        'EFF_DATE': eff_date,
        'ACCOUNT': credit_account,
        'AMOUNT': -montant,
        'SOURCE': src,
        'COMPANY': comp,
        'FY': fy_label,
        'Fabricated_JE': 0,
        'TYPE': 0
    }

    entries.append(entry_debit)
    entries.append(entry_credit)
    clean_entries.append((entry_debit, entry_credit))

# === Création des doublons ===
n_anomalies = int(n_je * anomaly_ratio)
for j in range(n_anomalies):
    original = random.choice(clean_entries)
    je_no_dup = f"JE-DUP-{j+1}"

    for line in original:
        dup_line = copy.deepcopy(line)
        dup_line['JE_NO'] = je_no_dup
        dup_line['Fabricated_JE'] = 1
        dup_line['TYPE'] = 4
        entries.append(dup_line)

# === Export ===
df = pd.DataFrame(entries)
df.to_csv("journal_avec_anomalie_type4.csv", index=False)
print(f"Fichier généré avec {n_anomalies} doublons ajoutés.")
