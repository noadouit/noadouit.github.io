import mysql.connector
from mysql.connector import IntegrityError
from datetime import datetime


def convertir_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d 00:00:00")
    except ValueError:
        return date_str  

def est_date(valeur):
    try:
        datetime.strptime(valeur, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def traiter_csv(fichier, requete, colonnes, db, c):
    with open(fichier, "r", encoding="ISO-8859-1") as f:
        lignes = f.readlines()
    
    lignes = lignes[1:]  # Suppression de l'en-tête
    
    valeurs = []
    for ligne in lignes:
        ligne = ligne.strip().split(';')
        ligne = [ligne[i] for i in colonnes]  # Sélectionner uniquement les colonnes spécifiées
        valeurs.append(tuple(
            convertir_date(val) if est_date(val) else (int(val) if val.isdigit() else val)
            for val in ligne
        ))
    
    # Insertion des valeurs dans la base de données
    for valeur in valeurs:
        try:
            c.execute(requete, valeur)
            db.commit()
        except IntegrityError:
            print("Erreur d'intégrité pour la ligne " + str(valeur))
            db.rollback()
        else:
            print("Ligne " + str(valeur) + " ajoutée avec succès.")


if __name__ == "__main__":
    # Paramètres de connexion à la base de données
    params = {"host": "localhost", "user": "root", "password": "", "database": "selmarinnolannoa"}

    db = mysql.connector.connect(**params)
    c = db.cursor()
    # Définition des requêtes correctes
    requete_client = "INSERT INTO Client VALUES (%s, %s, %s, %s)"
    requete_entree = "INSERT INTO Entree VALUES (%s, %s, %s, %s, %s)"
    requete_saunier = "INSERT INTO Saunier VALUES (%s, %s, %s, %s)"
    requete_sortie = "INSERT INTO Sortie VALUES (%s, %s, %s)"
    requete_concerner = "INSERT INTO Concerner VALUES (%s, %s, %s)"

    # Traitement des fichiers CSV
    traiter_csv("csv/Client.csv", requete_client, [0, 1, 2, 3], db, c)
    traiter_csv("csv/Entree.csv", requete_entree, [0, 1, 2, 3, 4], db, c)
    traiter_csv("csv/Saunier.csv", requete_saunier, [0, 1, 2, 3], db, c)
    traiter_csv("csv/Sortie.csv", requete_sortie, [0, 1, 2], db, c)
    traiter_csv("csv/Sortie.csv", requete_concerner, [3, 0, 4], db, c)

    # Fermeture de la connexion
    c.close()
    db.close()
