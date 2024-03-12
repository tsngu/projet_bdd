#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 10 #############

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Donnez à chaque manager la possiblité d'afficher les employés qui ont vendu le plus de Cocktails du moment et de Blonde pression.

# Identification du manager

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

    infoVentes = input("Voulez-vous afficher les informations sur les employés ? (O / N) : ")

    # Si O alors on lui donne les informations par rapport à son bar. Sinon on arrête le programme.
    
    if (infoVentes == "N"):
        print("Le système va s'éteindre.")
    elif (infoVentes == "O"):
        
        # Les employés qui ont vendu le plus de "Cocktail du moment" et de "Blonde pression"
        print(f"Les cinq employés qui ont le plus vendu de Cocktail du moment et de Blonde pression au bar {etablissement} sont :")
        nb_employe = 5

        # Besoin des tables Ventes, Carte et Employes.
        # Jointure entre les 3 tables avec E.bar = l'établissement du manager et les Boissons sélectionnées = Cocktail du moment et Blonde pression.
        # On sélectionne le nombre de ventes de ces boissons, le nom et prénoms des employés.
        # On groupe par le matricule et on ordonne par le nombre de ventes des boissons en ordre croissant.
        curseur.execute("SELECT COUNT(idVente) AS Cnt, nomEmploye, prenomEmploye FROM Ventes AS V, Carte AS C, Employes AS E\
            WHERE V.idBoisson = C.idBoisson AND V.idEmploye = E.matricule AND (nomBoisson = 'Cocktail du moment') OR (nomBoisson = 'Blonde pression') AND E.bar = ?\
                GROUP BY matricule ORDER BY Cnt ASC LIMIT ?", (etablissement, nb_employe))
        resultem = curseur.fetchall()
        for min, prenom, nom in resultem:
            print(nom + " " + prenom + ".")

    else:
        print("Ce n'est pas une réponse acceptée, le système va s'éteindre.")

BDD.close()