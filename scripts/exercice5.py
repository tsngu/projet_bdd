#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 5 ##########
## Ventes de chaque employé avec droits utilisateurs

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Authentification du manager

# on récupère les ID Manager
infosManager = dict()
curseur.execute("SELECT idManager, nomEtablissement FROM Etablissements")
for matricule, nom in curseur.fetchall():
    infosManager[matricule] = nom
    
idOk = False
idEmploye = input("Entrez votre ID Manager : ")
if idEmploye not in infosManager.keys():
    print("Vous n'avez pas accès aux informations sur les ventes.")
else:
    # on récupère l'établissement dont l'utilisateur est le manager
    etablissement = infosManager[idEmploye]
    
    print(f"Authentification réussie. Information sur les ventes du bar \"{etablissement}\" :\n")
    # Authentification réussie, on passe à la recherche
    # pour tester : T80612
    
    curseur.execute(f"SELECT DISTINCT nomEmploye, prenomEmploye, COUNT(matricule), SUM(prix) FROM Employes AS E, Ventes AS V, Carte AS C WHERE E.matricule = V.idEmploye AND V.idBoisson = C.idBoisson AND E.bar = ? GROUP BY matricule", (etablissement,))
    for nom, prenom, vente, chiffre in curseur.fetchall():
        print(nom + " " +  prenom + " : " + str(vente) + " ventes pour un chiffre de " + str(round(chiffre, 2)) + "€.")


BDD.close()