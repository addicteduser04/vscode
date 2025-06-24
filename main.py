import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 1. Configuration des paramètres
n_journal_entries = 5105
total_transactions = 32100
anomaly_counts = {'1': 22, '2': 14, '3': 18, '4': 18, '5': 18, '6': 18, '7': 20, '8': 20}

# 2. Génération des comptes (Classe 1 à 9)
classes = {
    'facture': ['6121', '6161', '6181', '6231', '6251', '6261', '6271', '6311', '6581', '44111', '44112', '4413', '4415', '4417', '4418'],
    'salaire_frais': ['6211', '6231'],
    'tva': ['3455','4455','4456'],
    'banque': ['512'],
    'caisse': ['531'],
    'banque_frais': ['6681', '6711'],
    'tiers': ['467']
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
def get_source_code(account, amount):
    is_debit = amount > 0

    # Mapping logique des comptes à un code source numérique
    source_map = {
        'facture': ['6121', '6161', '6181', '6231', '6251', '6261', '6271', '6311', '6581', '44111', '44112', '4413', '4415', '4417', '4418'],
        'salaire_frais': ['6211', '6231'],
        'tva': ['3455','4455','4456'],
        'banque': ['512'],
        'caisse': ['531'],
        'banque_frais': ['6681', '6711'],
        'tiers': ['467']
    }

    if account in source_map['facture']:
        return 1
    elif account in source_map['banque']:
        return 2
    elif account in source_map['caisse']:
        return 3
    elif account in source_map['tva']:
        return 4
    elif account in source_map['salaire_frais']:
        return 5
    elif account in source_map['banque_frais']:
        return 6
    elif account in source_map['tiers']:
        return 7
    else:
        return 7  # valeur par défaut pour écriture manuelle ou inconnue



def add_anomalies8(data, n=5):

    comptes_charges = ['6061', '6111', '6151']       # comptes de charges fournisseurs
    comptes_fournisseurs = ['4011', '4012', '4015'] # comptes fournisseurs
    comptes_produits = ['701', '707']                # comptes de produits (revenus)

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        je_no = f'JE-{i+ n_journal_entries - len(anomaly_counts) + 131}'
        montant_total = round(random.uniform(8000, 15000), 2)

        montant_tva = round(montant_total * 0.2, 2)
        montant_ht = round(montant_total * 0.8, 2)

        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        eff_date_str = eff_date.strftime('%Y-%m-%d')

        compte_charge = random.choice(comptes_charges)
        compte_fournisseur = random.choice(comptes_fournisseurs)
        compte_produit = random.choice(comptes_produits)

        # 1) Double enregistrement facture fournisseur (charge + fournisseur)
        # Débit charge (facture)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_charge)
        data['AMOUNT'].append(montant_ht)  # débit
        data['SOURCE'].append(get_source_code(compte_charge,montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # Débit TVA déductible
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')  # compte TVA déductible (à ajuster selon PC Marocain)
        data['AMOUNT'].append(round(montant_tva,2))  # débit TVA
        data['SOURCE'].append(get_source_code('3455',montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # Débit charge (facture) - second enregistrement (double)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_charge)
        data['AMOUNT'].append(round(montant_ht,2))  # débit (doublon)
        data['SOURCE'].append(get_source_code(compte_charge,montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # Débit TVA déductible
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')  # compte TVA déductible (à ajuster selon PC Marocain)
        data['AMOUNT'].append(round(montant_tva,2))  # débit TVA
        data['SOURCE'].append(get_source_code('3455',montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # Crédit fournisseur (facture)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_fournisseur)
        data['AMOUNT'].append(round(-(montant_ht + montant_tva),2))  # crédit
        data['SOURCE'].append(get_source_code(compte_fournisseur,-(montant_ht+montant_tva)))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # 2) Enregistrement du "paiement" incorrect par création de revenu
        # Crédit produit (revenu)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_produit)
        data['AMOUNT'].append(round(-montant_ht,2))  # crédit (création de revenu)
        data['SOURCE'].append(get_source_code(compte_produit,-montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

        # Débit fournisseur (réduction dette) partiellement fausse
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_fournisseur)
        data['AMOUNT'].append(round(montant_ht,2))  # débit (réduction partielle dette)
        data['SOURCE'].append(get_source_code(compte_fournisseur,montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('8')

    return data

def add_anomalies7(data, n=5):

    comptes_produits = ['701', '707']     # comptes de ventes (produits)
    comptes_clients = ['4111', '4112']    # comptes clients
    compte_fournisseur_4010 = '4010'      # compte fournisseur utilisé pour apurement fictif

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        je_no = f'JE-{i+ n_journal_entries - len(anomaly_counts) + 111}'
        montant_total = round(random.uniform(8000, 15000), 2)

        montant_tva = round(montant_total * 0.2, 2)
        montant_ht = round(montant_total * 0.8, 2)

        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        eff_date_str = eff_date.strftime('%Y-%m-%d')

        compte_produit = random.choice(comptes_produits)
        compte_client = random.choice(comptes_clients)

        # 1) Enregistrement revenu fictif (vente)
        # Crédit produit (vente)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_produit)
        data['AMOUNT'].append(round(-montant_ht,2))  # crédit
        data['SOURCE'].append(get_source_code(compte_produit,-montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('7')

        # Crédit TVA collectée
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')
        data['AMOUNT'].append(round(-montant_tva,2))  # crédit
        data['SOURCE'].append(get_source_code('3455',-montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('7')

        # Débit client (total facture)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_client)
        data['AMOUNT'].append(round(montant_ht + montant_tva, 2))  # débit
        data['SOURCE'].append(get_source_code(compte_client,montant_ht+montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('7')

        # 2) Apurement fictif : on lettre la facture avec le compte fournisseur 4010
        # Crédit client (annulation facture)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_client)
        data['AMOUNT'].append(round(-(montant_ht + montant_tva),2))  # crédit
        data['SOURCE'].append(get_source_code(compte_client,-(montant_ht+montant_tva)))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('7')

        # Débit compte fournisseur 4010 (pour simuler paiement)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_fournisseur_4010)
        data['AMOUNT'].append(round(montant_ht + montant_tva,2))  # débit
        data['SOURCE'].append(get_source_code(compte_fournisseur_4010,montant_ht+montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('7')

    return data


def add_anomalies6(data, n=5):

    comptes_produits = ['701', '707']       # comptes de ventes (produits)
    comptes_charges = ['6061', '6111', '6151']  # comptes de charges
    comptes_clients = ['4111', '4112']      # comptes clients

    for i in range(n):
        je_no = f'JE-{i+ n_journal_entries - len(anomaly_counts) + 93}'
        montant_total_reel = round(random.uniform(8000, 15000), 2)
        company = f"{np.random.randint(1, 10)}"
        source = '1'
        # Gonflement du CA: on augmente le montant réel de 30 à 50%
        facteur_gonflement = random.uniform(1.3, 1.5)
        montant_total_gonfle = round(montant_total_reel * facteur_gonflement, 2)

        # Calcul TVA normale sur le montant gonflé
        montant_tva = round(montant_total_gonfle * 0.2, 2)
        montant_ht = round(montant_total_gonfle * 0.8, 2)

        # Date aléatoire dans l’année
        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        eff_date_str = eff_date.strftime('%Y-%m-%d')

        compte_produit = random.choice(comptes_produits)
        compte_charge = random.choice(comptes_charges)
        compte_client = random.choice(comptes_clients)

        # Crédit produit (CA gonflé) — manuel
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_produit)
        data['AMOUNT'].append(-montant_ht)  # crédit
        data['SOURCE'].append(get_source_code(compte_produit,-montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('6')

        # Crédit TVA collectée sur montant gonflé
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')
        data['AMOUNT'].append(-montant_tva)  # crédit
        data['SOURCE'].append(get_source_code('3455',montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('6')

        # Débit client (total gonflé)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_client)
        data['AMOUNT'].append(round(montant_ht + montant_tva,2))  # débit
        data['SOURCE'].append(get_source_code(compte_client,montant_ht+montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('6')

        # Enregistrement manuel d’un coût fictif (charge) pour équilibrer ou masquer
        montant_charge = round(random.uniform(2000, 5000), 2)

        # Débit charge (manuel)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_charge)
        data['AMOUNT'].append(montant_charge)  # débit
        data['SOURCE'].append(get_source_code(compte_charge,montant_charge))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('6')

        # Crédit divers (compte 512, banque par exemple) pour équilibrer le JE
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('512')
        data['AMOUNT'].append(-montant_charge)  # crédit
        data['SOURCE'].append(get_source_code('512',-montant_charge))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('6')

    return data

def add_anomalies5(data, n=5):

    comptes_produits = ['701', '707']  # comptes de ventes
    comptes_clients = ['4111', '4112']

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        je_no = f'FE-{i+ n_journal_entries - len(anomaly_counts) + 75}'
        montant_total = round(random.uniform(8000, 15000), 2)

        # TVA normale
        montant_tva = round(montant_total * 0.2, 2)
        # Surévaluation artificielle de la base HT (90% au lieu de 80%)
        montant_ht = round(montant_total * 0.9, 2)

        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        eff_date_str = eff_date.strftime('%Y-%m-%d')
        compte_produit = random.choice(comptes_produits)
        compte_client = random.choice(comptes_clients)

        # Crédit produit (surévalué, car c’est un produit)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_produit)
        data['AMOUNT'].append(-montant_ht)  # crédit -> montant négatif
        data['SOURCE'].append(get_source_code(compte_produit,-montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('5')

        # Crédit TVA collectée
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')
        data['AMOUNT'].append(-montant_tva)  # crédit -> montant négatif
        data['SOURCE'].append(get_source_code('3455',-montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('5')

        # Débit client (montant total surévalué)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_client)
        data['AMOUNT'].append(round(montant_ht + montant_tva,2))  # débit -> montant positif
        data['SOURCE'].append(get_source_code(compte_client,montant_ht + montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('5')

    return data



def add_anomalies4(data, n=5):


    charges_soumis_tva = ['6061', '6111', '6151', '6171', '6131'] 
    fournisseurs_441 = ['44111', '44112', '4415']

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        je_no = f'JE-{i+ n_journal_entries - len(anomaly_counts) + 57}'
        montant_total = round(random.uniform(8000, 15000), 2)

        # On garde la TVA normale
        montant_tva = round(montant_total * 0.2, 2)
        # On diminue artificiellement la base HT (par exemple 60% au lieu de 80%)
        montant_ht = round(montant_total * 0.6, 2)
        # Le total n’équilibre plus HT + TVA (surévaluée par rapport à HT)

        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        eff_date_str = eff_date.strftime('%Y-%m-%d')
        compte_charge = random.choice(charges_soumis_tva)
        compte_fournisseur = random.choice(fournisseurs_441)

        # Débit charge (diminuée)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_charge)
        data['AMOUNT'].append(montant_ht)
        data['SOURCE'].append(get_source_code(compte_charge,montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('4')

        # Débit TVA (normale ou exagérée)
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')
        data['AMOUNT'].append(montant_tva)
        data['SOURCE'].append(get_source_code('3455',montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('4')

        # Crédit fournisseur
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(compte_fournisseur)
        data['AMOUNT'].append(round(-(montant_ht + montant_tva),2))
        data['SOURCE'].append(get_source_code(compte_fournisseur,-(montant_ht+montant_tva)))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('4')

    return data



def add_anomalies3(data, n=5):

    comptes_tva = ['3455']
    fournisseurs_441 = ['44111', '44112', '4413', '4415', '4417', '4418','512', '531','467']

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"



        je_no = f'JE-{i + n_journal_entries - len(anomaly_counts) + 37}'
        montant_tva = round(random.uniform(1000, 5000), 2)
        eff_date_str = eff_date.strftime('%Y-%m-%d')

        # Ligne TVA récupérable sans base HT
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append('3455')  # TVA récupérable
        data['AMOUNT'].append(montant_tva)
        data['SOURCE'].append(get_source_code('3455',montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('3')
        account_fournissuer= random.choice(fournisseurs_441)
        # Crédit fournisseur
        data['JE_NO'].append(je_no)
        data['EFF_DATE'].append(eff_date_str)
        data['ACCOUNT'].append(account_fournissuer)
        data['AMOUNT'].append(-montant_tva)
        data['SOURCE'].append(get_source_code(account_fournissuer,-montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append('3')

    return data


def add_anomalies2(data, n=10):

    
    # Charges typiques utilisées dans les fraudes (souvent non taxables ou fictives)
    charges_fictives = [
        '6121', '6161', '6211', '6251', '6311', '6711'
    ]
    
    comptes_paiement = ['531', '512']  # Caisse ou banque
    compte_tva = '3455'  # TVA récupérable

    for i in range(n):
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"

        je_no = f'JE-{i+ n_journal_entries - len(anomaly_counts) + 23}'
        montant_total = round(random.uniform(3000, 15000), 2)
        montant_ht = round(montant_total * 0.8, 2)
        montant_tva = round(montant_total * 0.2, 2)

        eff_date = datetime.now() - timedelta(days=random.randint(0, 365))
        eff_date_str = eff_date.strftime('%Y-%m-%d')

        compte_charge = random.choice(charges_fictives)
        compte_credit = random.choice(comptes_paiement)

        for compte, montant in [
            (compte_charge, montant_ht),       # Débit charge fictive
            (compte_tva, montant_tva),         # Débit TVA récupérable
            (compte_credit, -montant_total)    # Crédit caisse ou banque
        ]:
            data['JE_NO'].append(je_no)
            data['EFF_DATE'].append(eff_date_str)
            data['ACCOUNT'].append(compte)
            data['AMOUNT'].append(montant)
            data['SOURCE'].append(get_source_code(compte,montant))
            data['COMPANY'].append(company)
            data['FY'].append(fy)
            data['Fabricated_JE'].append('1')
            data['TYPE'].append("2")

    return data


def add_anomalies1(data, n=10):
    charges_non_tva = [
    '6121', '6161', '6181', '6211', '6231',
    '6251', '6261', '6271', '6311', '6581',
    '6681', '6711'
    ]    
    tva_récupérable = '3455'
    fournisseurs_441 = ['44111', '44112', '4413', '4415', '4417', '4418','512', '531','467']


    for i in range(n):
        eff_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 730))
        fy = f"{eff_date.year}-{eff_date.month:02d}-01 – {eff_date.year+1}-{(eff_date.month - 1 or 12):02d}-28"
        source = f"{np.random.randint(1, 8)}"
        company = f"{np.random.randint(1, 10)}"
        montant_total = round(random.uniform(1000, 10000), 2)
        montant_ht = round(montant_total * 0.8, 2)
        montant_tva = round(montant_total * 0.2, 2)
        compte_fournisseur =random.choice(fournisseurs_441)
        compte_charge_non_tva = random.choice(charges_non_tva)
        # Ligne charge non taxable (débit)
        data['JE_NO'].append(f"JE-{i+ n_journal_entries - len(anomaly_counts) + 1}")
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(compte_charge_non_tva)
        data['AMOUNT'].append(montant_ht)
        data['SOURCE'].append(get_source_code(compte_charge_non_tva, montant_ht))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append(1)

        # Ligne TVA récupérable (débit) – à tort
        data['JE_NO'].append(f"JE-{i+ n_journal_entries - len(anomaly_counts) + 1}")
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(tva_récupérable)
        data['AMOUNT'].append(montant_tva)
        data['SOURCE'].append(get_source_code(tva_récupérable, montant_tva))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append(1)

        # Ligne fournisseur détaillé (crédit)
        data['JE_NO'].append(f"JE-{i+ n_journal_entries - len(anomaly_counts) + 1}")
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(compte_fournisseur)
        data['AMOUNT'].append(-montant_total)
        data['SOURCE'].append(get_source_code(compte_fournisseur, -montant_total))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('1')
        data['TYPE'].append(1)

    return data



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
    account = np.random.choice(accounts)
    for amount in all_amounts:
        data['JE_NO'].append(f"JE-{je_id}")
        data['EFF_DATE'].append(eff_date.strftime('%Y-%m-%d'))
        data['ACCOUNT'].append(account)
        data['AMOUNT'].append(amount)
        data['SOURCE'].append(get_source_code(account,amount))
        data['COMPANY'].append(company)
        data['FY'].append(fy)
        data['Fabricated_JE'].append('0')
        data['TYPE'].append('0')

add_anomalies1(data, n=22)
add_anomalies2(data, n=14)
add_anomalies3(data, n=20)
add_anomalies4(data, n=18)
add_anomalies5(data, n=18)
add_anomalies6(data, n=18)
add_anomalies7(data, n=20)
add_anomalies8(data, n=18)
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