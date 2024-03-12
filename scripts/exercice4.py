#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 4 ##########

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Pour récupérer la date à laquelle il y a eu le moins de ventes :
# Besoin de : date et idVente de la table Ventes.
# On compte d'abord le nombre de Ventes par date qu'on sauvegarde dans V.
# Puis on prend la valeur la plus petite avec MIN et la date.

curseur.execute("SELECT date, MIN(V) FROM (SELECT COUNT(idVente) AS V, date FROM Ventes GROUP BY date)")
resultnbv = curseur.fetchall()
for date, chiffre in resultnbv:
    print("Le " + str(date) + " a enregistré le moins de ventes avec " + str(chiffre) + " ventes.")

print()
# Pour récupérer la date à laquelle les bénéfices ont été les moins importants :
# Besoin de : date et prix des tables Carte et Ventes.
# On fait la somme des prix des ventes par date qu'on enregistre dans B.
# Jointure par idBoisson sur les deux tables.
# On prend la somme la plus petite avec MIN(B) et la date.

curseur.execute("SELECT MIN(B), date FROM (SELECT SUM(prix) AS B, date FROM Carte AS C, Ventes AS V WHERE C.idBoisson = V.idBoisson GROUP BY date)")
resultnbb = curseur.fetchall()
for chiffre, date in resultnbb:
    print("Le bénéfice le moins important était de " + str(round(chiffre, 2)) + "€ le " + str(date) + ".")

BDD.close()