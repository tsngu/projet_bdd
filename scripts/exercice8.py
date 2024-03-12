#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 8 #########

import sqlite3 as sql
import csv

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

    # On demande au manager s'il veut afficher les information du mois. 

    infoVentes = input("Voulez-vous afficher les informations sur les ventes de ce mois ? (O / N) : ")

    # Si O alors on lui donne les informations par rapport à son bar. Sinon on arrête le programme.
    
    if (infoVentes == "N"):
        print("Le système va s'éteindre.")
    elif (infoVentes == "O"):

        # Afficher les boissons les moins vendues dans l'établissement ce mois-ci
        print(f"Les boissons qui sont les moins vendues à {etablissement} sont :")

        nb_boissons = 5 # On va afficher 5 boissons.

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
        # Afficher les employés qui ont le moins vendu
        print(f"Les cinq employés qui ont le moins vendu de boissons au bar {etablissement} sont :")

        nb_employes = 5

        # Besoin des tables Ventes et Employes
        # Jointure entre les 2 tables
        # Comme dans la requête au dessus, compter les boissons vendues par leur id et nommer la valeur B.
        # Selectionner le nom et prénom des employés.
        # Grouper par les id des employés et par odre ascendant de B.

        curseur.execute("SELECT COUNT(V.idBoisson) AS B, nomEmploye, prenomEmploye FROM Ventes AS V, Employes AS E\
            WHERE V.idEmploye = E.matricule AND E.bar = ?\
                GROUP BY idEmploye ORDER BY B ASC LIMIT ?", (etablissement, nb_employes))
        resultemp = curseur.fetchall()
        for min, nom, prenom in resultemp:
            print(nom + " " + prenom + ".")

BDD.close()