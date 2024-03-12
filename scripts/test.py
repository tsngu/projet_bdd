#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 8 #########

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Vérif exo 8 part 1;

#curseur.execute("SELECT COUNT(V.idBoisson), nomBoisson FROM Ventes AS V, CARTE AS C WHERE V.idBoisson = C.idBoisson GROUP BY nomBoisson")
#result = curseur.fetchall()
#for nb, nom in result:
    #print(nom + " a été vendu " + (str(nb) + " fois."))

print("Les cinq employés qui ont le plus vendu de Cocktail du moment et de Blonde pression sont :")
nb_employe = 5
curseur.execute("SELECT COUNT(idVente) AS Cnt, nomEmploye, prenomEmploye FROM Ventes AS V, Carte AS C, Employes AS E WHERE V.idBoisson = C.idBoisson AND V.idEmploye = E.matricule AND (nomBoisson = 'Cocktail du moment') OR (nomBoisson = 'Blonde pression') GROUP BY matricule ORDER BY Cnt ASC LIMIT ?", (nb_employe,))
resultem = curseur.fetchall()
for min, prenom, nom in resultem:
    print(nom + " " + prenom + ".")