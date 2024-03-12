########## EXERCICE 11 #########

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
    
    curseur.execute("SELECT AVG(degre) FROM Ventes AS V, Carte AS C WHERE V.idBoisson = C.idBoisson")
    resultat = curseur.fetchall()
    degre_moyen = resultat[0][0]
    print(f"Le bar {etablissement} a vendu des boissons à {round(degre_moyen, 2)}% d'alcool en moyenne.")
    
    # quantité d'alcool = degré/100 (pour avoir un pourcentage) * quantité de boisson
    curseur.execute("SELECT SUM(degre/100 * quantite) FROM Ventes AS V, Carte AS C WHERE V.idBoisson = C.idBoisson")
    resultat = curseur.fetchall()
    quantite_alcool = resultat[0][0]
    print(f"Le bar {etablissement} a vendu une quantité totale d'alcool de {round(quantite_alcool, 2)} cL.")

BDD.close()