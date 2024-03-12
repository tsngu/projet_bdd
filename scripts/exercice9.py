########## EXERCICE 9 #########

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
    
    NB_BOISSONS = 5
    
    # 1. les boissons les plus rentables, disons 5 (LIMIT 5)
    # Ventes
    # Carte pour le nom de la boisson et son prix
    
    print(f"Boissons les plus rentables pour le bar {etablissement} :")
    
    curseur.execute("SELECT nomBoisson, COUNT(V.idBoisson), prix FROM Ventes AS V, Carte AS C, Employes AS E WHERE V.idBoisson = C.idBoisson AND E.matricule = V.idEmploye AND E.bar = ? GROUP BY V.idBoisson", (etablissement,))
    resultat = curseur.fetchall()
    # fonction de tri
    def tri_resultats(liste):
        return liste[1]*liste[2]
    resultat = sorted(resultat, key=tri_resultats, reverse=True)
    # on affiche les 5 premières
    for nomBoisson, nombre_ventes, prix in resultat[:NB_BOISSONS]:
        print(f"{nomBoisson} a rapporté {round(nombre_ventes*prix, 2)}€.")
        
    NB_EMPLOYES = 5
    
    # nom des employes => Employes
    # Ventes
    # carte pour avoir le chiffre de chaque employé
    
    print() # saut de ligne
    print(f"Employés les plus productifs du bar {etablissement} : ")
    
    curseur.execute("SELECT prenomEmploye, nomEmploye, SUM(prix) AS benefice FROM Ventes AS V, Carte AS C, Employes AS E WHERE V.idBoisson = C.idBoisson AND E.matricule = V.idEmploye AND E.bar = ? GROUP BY idEmploye ORDER BY benefice DESC LIMIT ?", (etablissement, NB_EMPLOYES))
    resultbenef = curseur.fetchall()
    for prenom, nom, benef in resultbenef:
        print(f"{prenom} {nom} a généré {round(benef, 2)}€.")

BDD.close()