import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Configuration des paramètres
n_journal_entries = 5105
total_transactions = 32100
anomaly_counts = {'1': 22, '2': 14, '3': 18, '4': 18, '5': 18, '6': 18, '7': 20, '8': 20}

# 2. Génération des comptes (Classe 1 à 9)
classes = {
    '1': [f"1{str(i).zfill(3)}" for i in range(100, 199)],
    '2': [f"2{str(i).zfill(3)}" for i in range(100, 299)],
    '3': [f"3{str(i).zfill(3)}" for i in range(100, 399)],
    '4': [f"4{str(i).zfill(3)}" for i in range(100, 499)],
    '5': [f"5{str(i).zfill(3)}" for i in range(100, 599)],
    '6': [f"6{str(i).zfill(3)}" for i in range(100, 699)],
    '7': [f"7{str(i).zfill(3)}" for i in range(100, 799)],
    '8': [f"8{str(i).zfill(3)}" for i in range(100, 899)],
    '9': [f"9{str(i).zfill(3)}" for i in range(100, 999)]
}
accounts = [acc for sublist in classes.values() for acc in sublist][:426]

# 3. Génération des données de base
data = {
    'JE_NO': [],
    'EFF_DATE': [],
    'ACCOUNT': [],
    'AMOUNT': [],
    'SOURCE': [],
    'COMPANY': [],
    'FY': [],
    'Fabricated_JE': [],
    'TYPE': []
}

# 4. Génération des écritures normales équilibrées
for je_id in range(1, n_journal_entries - len(anomaly_counts) + 1):
    n_trans = np.random.choice([2, 4, 6])  # nombre pair pour équilibrer débit/crédit
    eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
    fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
    source = f"{np.random.randint(1, 8)}"
    company = f"{np.random.randint(1, 10)}"
    
    # Générer n_trans/2 montants positifs
    debit_amounts = np.round(np.random.uniform(1000, 50000, n_trans // 2), 2)
    credit_amounts = -debit_amounts  # exact opposé
    
    # Fusionner, mélanger et créer les transactions
    all_amounts = np.concatenate([debit_amounts, credit_amounts])
    np.random.shuffle(all_amounts)

    for amount in all_amounts:
        data['JE_NO'].append(f"JE-{je_id}")
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(np.random.choice(accounts))
        data['AMOUNT'].append(amount)
        data['SOURCE'].append(source)
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('0')
        data['TYPE'].append('0')


# 5. Génération des anomalies (0.46%)
anomaly_accounts = {
    '1': ['4455', '6121'],  # TVA + Compte de charges
    '2': ['5161', '4556'],  # Caisse + TVA récupérable
    '3': ['4455', '6134'],  # TVA + Assurances
    '4': ['4456', '6121'],  # TVA récupérable + Achats
    '5': ['7121', '4456'],  # Ventes + TVA récupérable
    '6': ['3421', '7121'],  # Clients + Ventes
    '7': ['4010', '3421'],  # Fournisseurs + Clients
    '8': ['4010', '7121']   # Fournisseurs + Ventes
}

for anomaly_type, count in anomaly_counts.items():
    for i in range(count):
        je_id = f"ANOM-{anomaly_type}-{i+1}"
        eff_date = datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 365))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{eff_date.month-1:02d}-28"
        
        # Transaction 1 (Débit)
        data['JE_NO'].append(je_id)
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(anomaly_accounts[anomaly_type][0])
        data['AMOUNT'].append(round(np.random.uniform(5000, 30000), 2))
        data['SOURCE'].append(f"{np.random.randint(1, 8)}")
        data['COMPANY'].append(f"{np.random.randint(1, 10)}")
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append(anomaly_type)
        
        # Transaction 2 (Crédit)
        data['JE_NO'].append(je_id)
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(anomaly_accounts[anomaly_type][1])
        data['AMOUNT'].append(-data['AMOUNT'][-1])  # Balance exacte
        data['SOURCE'].append(data['SOURCE'][-1])
        data['COMPANY'].append(data['COMPANY'][-1])
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append(anomaly_type)

# 6. Création du DataFrame
df = pd.DataFrame(data)
df['ACCOUNT_DC'] = df.apply(lambda row: f"{row['ACCOUNT']}_D" if float(row['AMOUNT']) >= 0 else f"{row['ACCOUNT']}_C", axis=1)

# 7. Vérification des caractéristiques
print(f"Total transactions: {len(df)}")
print(f"Normal transactions: {len(df[df['Fabricated_JE'] == '0'])}")
print(f"Anomaly transactions: {len(df[df['Fabricated_JE'] == '1'])}")
print(f"Unique accounts: {df['ACCOUNT'].nunique()}")
print(f"Journal entries: {df['JE_NO'].nunique()}")

# 8. Export vers CSV
df.to_csv('dataset_comptable_marocain.csv', index=False)