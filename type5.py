import csv
import random
from datetime import datetime, timedelta

def generate_type_5_transactions(num_transactions, start_je_no, fiscal_year):
    sources = ['A','B','C','D','E','F','G']
    companies = [str(i) for i in range(1,10)]  # 1 à 9
    # Comptes "normaux"
    normal_accounts = [f"{random.randint(100000, 999999)}" for _ in range(90)]
    # Comptes "dormants" (inactifs) - peu utilisés
    dormant_accounts = [f"{random.randint(2000000, 2999999)}" for _ in range(10)]

    transactions = []
    current_je_no = start_je_no

    start_date = datetime(fiscal_year, 1, 1)

    # 1. Historique normal avec comptes normaux (pas d'anomalie)
    for _ in range(500):  # simuler activité normale passée
        je_no = current_je_no
        eff_date = start_date + timedelta(days=random.randint(0, 200))
        account = random.choice(normal_accounts)
        amount = round(random.uniform(-10000, 10000), 2)
        source = random.choice(sources)
        company = random.choice(companies)
        FY = fiscal_year
        fabricated_je = 0  # pas anomalie
        anomaly_type = 0  # pas anomalie

        transactions.append({
            "JE_NO": je_no,
            "eff_date": eff_date.strftime("%Y-%m-%d"),
            "account": account,
            "amount": amount,
            "source": source,
            "company": company,
            "FY": FY,
            "fabricated_je": fabricated_je,
            "type_anomalie": anomaly_type
        })
        current_je_no += 1

    # 2. Générer une activité soudaine sur comptes dormants (anomalie type 5)
    # Plusieurs transactions sur comptes dormants sur périodes rapprochées
    for _ in range(num_transactions):
        je_no = current_je_no
        # Dates concentrées sur fin d'année (exemple)
        eff_date = start_date + timedelta(days=random.randint(300, 364))
        account = random.choice(dormant_accounts)
        amount = round(random.uniform(-5000, 5000), 2)
        source = random.choice(sources)
        company = random.choice(companies)
        FY = fiscal_year
        fabricated_je = 1  # anomalie
        anomaly_type = 5

        transactions.append({
            "JE_NO": je_no,
            "eff_date": eff_date.strftime("%Y-%m-%d"),
            "account": account,
            "amount": amount,
            "source": source,
            "company": company,
            "FY": FY,
            "fabricated_je": fabricated_je,
            "type_anomalie": anomaly_type
        })
        current_je_no += 1

    return transactions

def save_to_csv(transactions, filename):
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ["JE_NO", "eff_date", "account", "amount", "source", "company", "FY", "fabricated_je", "type_anomalie"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for trans in transactions:
            writer.writerow(trans)

# Générer exemple
num_anomalies = 50
start_je_no = 1000
fiscal_year = 2025

transactions = generate_type_5_transactions(num_anomalies, start_je_no, fiscal_year)
save_to_csv(transactions, "transactions_anomalie_type_5.csv")

print("Fichier généré : transactions_anomalie_type_5.csv")
