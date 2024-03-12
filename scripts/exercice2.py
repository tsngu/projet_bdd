#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 2 ##########

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Nombre total de bars : Besoin de la table Etablissement et compter chaque id présent.

curseur.execute("SELECT COUNT(idEtablissement) FROM Etablissements")
resultbar = curseur.fetchall()
for chiffre in resultbar:
    chiffre = resultbar[0][0]
    print("Il y a " + str(chiffre) + " bars.")

print()

# Nombre total d'employés : Besoin de la table Employés et compter chaque matricule.

curseur.execute("SELECT COUNT(matricule) FROM Employes")
resultemp = curseur.fetchall()
for chiffre in resultemp:
    chiffre = resultemp[0][0]
    print("Il y a " + str(chiffre) + " employés.")

print()
# Les managers de bars : Besoin de la table Employes, du nom, prénom, et du bar dans lequel ils travaillent avec la condition que profession = Manager.

curseur.execute("SELECT nomEmploye, prenomEmploye, bar FROM Employes WHERE profession='Manager'")
resultman = curseur.fetchall()
for nom, prenom, bar in resultman:
    print(nom + " " + prenom + " " + "dirige " + bar + ".")

print()
# Le nombre d'employés pour chaque profession : Besoin de la table Employes, compter le matricule de chaque employé et grouper par profession.

curseur.execute("SELECT COUNT(matricule), profession FROM Employes GROUP BY profession")
resultnbem = curseur.fetchall()
for chiffre, profession in resultnbem:
    print("Il y a" + " " + str(chiffre) + " " + profession + ".")

print()
# Le revenu total du groupe : Besoin de la table Ventes et de la table Carte.
# Dans la table Ventes, besoin de idBoisson.
# Dans la table Carte, besoin de prix.
# Jointure avec idBoisson sur les deux tables.

curseur.execute("SELECT SUM(prix), V.idBoisson FROM Carte AS C, Ventes AS V WHERE C.idBoisson = V.idBoisson")
resultrev = curseur.fetchall()
for chiffre, id in resultrev:
    print("Le revenu total du groupe est de " + str(round(chiffre, 2)) + "€")

BDD.close()