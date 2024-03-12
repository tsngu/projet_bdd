#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 12 #########

import sqlite3 as sql
import csv
import sys


BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Récupération des idManager
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

    nb_boissons = sys.argv[1] # Récupère la valeur notée dans le terminal
    print("Vous cherchez à supprimer " + nb_boissons + " boissons.")

    # Afficher les boissons les moins vendues dans l'établissement ce mois-ci
    print(f"Les {nb_boissons} boissons les moins consommées et donc à supprimer de la carte au bar {etablissement} sont :")
    print()

    # Besoin des tables Ventes, Carte et Employes
    # Besoin de COUNT le nombre de fois que les idBoissons qui apparaissent pour compter leur ventes, renommer la valeur à B.
    # Jointure entre les 3 tables et mettre la condition que l'employé doit être dans le bar du manager.
    # Grouper par le nom des boissons et trier par ordre ascendant.

    curseur.execute("SELECT COUNT(V.idBoisson) AS B, nomBoisson FROM Ventes AS V, Carte AS C, Employes AS E\
        WHERE V.idBoisson = C.idBoisson AND V.idEmploye = E.matricule AND E.bar = ?\
            GROUP BY nomBoisson ORDER BY B ASC LIMIT ?", (etablissement, nb_boissons))
    resultboiss = curseur.fetchall()
    for min, nom in resultboiss:
        print(nom + ".")

    print()
    print("ou")
    print()

    # Affichier les boissons les moins rentables
    print(f"Les {nb_boissons} boissons les moins rentables et donc à supprimer de la carte au bar {etablissement} sont :")
    print()

    # Besoin des tables Ventes, Carte et Employes
    # On sélectionne les idBoissons enregistrées dans la table Vente, le prix de ces boissons de la Carte et leur nom.
    # On joint les 3 tables avec E.bar = l'établissement en question.
    # On groupe par le nom des boissons et on trie par le bénéfice dans l'ordre croissant.
    curseur.execute("SELECT V.idBoisson, SUM(prix) AS benefice, nomBoisson FROM Ventes AS V, Carte AS C, Employes AS E\
        WHERE V.idBoisson = C.idBoisson AND V.idEmploye = E.matricule AND E.bar = ?\
            GROUP BY nomBoisson ORDER BY benefice ASC LIMIT ?", (etablissement, nb_boissons))
    resultrent = curseur.fetchall()
    for id, prix, nomBoisson in resultrent:
        print(nomBoisson + ".")

BDD.close()