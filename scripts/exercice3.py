#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 3 ##########
## Ventes de chaque employé

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# pour chaque employé, on va avoir besoin de :
# nom, prenom, matricule dans Employes
# nombre d'entrées dans Ventes
# prix dans Carte
# => jointure sur les 3 tables

# nombre total de ventes par employé = nombre de lignes dans Ventes contenant le matricule de l'employé

curseur.execute(f"SELECT DISTINCT nomEmploye, prenomEmploye, COUNT(idEmploye), SUM(prix) FROM Employes AS E, Ventes AS V, Carte AS C WHERE E.matricule = V.idEmploye AND V.idBoisson = C.idBoisson GROUP BY idEmploye")
result = curseur.fetchall()
for nom, prenom, vente, chiffre in result:
    print(nom + " " +  prenom + " : " + str(vente) + " ventes pour un chiffre de " + str(round(chiffre, 2)) + "€.")

BDD.close()
