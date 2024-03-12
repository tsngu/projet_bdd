# on reprend l'exercice 6
########## EXERCICE 7 #########

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Identification du Manager
infosManager = dict()
curseur.execute("SELECT idManager, nomEtablissement FROM Etablissements")
for matricule, nom in curseur.fetchall():
    infosManager[matricule] = nom
    
# On demande à l'utilisateur d'entrer son id.
idOk = False
idEmploye = input("Entrez votre ID Manager : ")

# Si son id ne correspond pas à un idManager, le programme s'arrête.
if idEmploye not in infosManager.keys():
    print("Vous n'avez pas accès aux informations sur les ventes.")
else:
    # Sinon non récupère l'établissement dont l'utilisateur est le manager
    etablissement = infosManager[idEmploye]
        
    # on demande la saisie de la date
    date = input("Entrez une date : ")
    # on convertir au format de la BDD : JJ/MM/A
    (jour, mois, annee) = date.split()
    # on convertir le mois en nombre
    tableMois = {
        "janvier": "01",
        "février": "02", 
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12"
    }
    date = "/".join([jour, tableMois[mois], annee])
    
    curseur.execute("SELECT COUNT(idVente), SUM(prix), bar FROM Ventes AS V, Carte AS C, Employes AS E WHERE E.matricule = V.idEmploye AND V.idBoisson = C.idBoisson AND E.bar = ? AND V.date = ?", (etablissement, date))
    resultventes = curseur.fetchall()
    for (ventes, montant, bar) in resultventes:
        print(f"Le bar {bar} a fait {ventes} ventes pour un chiffre de {round(montant, 2)}€.")
    print("Résultat par employé·e : ")
    
    curseur.execute("SELECT prenomEmploye, nomEmploye, SUM(prix) FROM Ventes AS V, Carte AS C, Employes AS E WHERE V.idBoisson = C.idBoisson AND E.matricule = V.idEmploye AND E.bar = ? AND V.date = ? GROUP BY idEmploye", (etablissement, date))
    resultbenef = curseur.fetchall()
    for (prenom, nom, montant) in resultbenef:
        print(f"{prenom} {nom} a généré un chiffre de {round(montant, 2)}€.")

BDD.close()