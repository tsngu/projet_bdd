#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 1 ##########
## Création de la base de données

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# EMPLOYÉS
curseur.execute("CREATE TABLE Employes (matricule TEXT PRIMARY KEY, nomEmploye TEXT NOT NULL, prenomEmploye TEXT NOT NULL, profession TEXT NOT NULL, bar TEXT NOT NULL);")

# ÉTABLISSEMENTS
# ajout d'une clé primaire avec la propriété autoincrement
curseur.execute("CREATE TABLE Etablissements (idEtablissement INTEGER PRIMARY KEY AUTOINCREMENT, nomEtablissement TEXT NOT NULL, adresse TEXT NOT NULL, numTelephone TEXT NOT NULL, idManager TEXT NOT NULL, FOREIGN KEY (idManager) REFERENCES Employes(matricule));")

# CARTE
curseur.execute("CREATE TABLE Carte (idBoisson INTEGER PRIMARY KEY, nomBoisson TEXT NOT NULL, type TEXT NOT NULL, prix REAL NOT NULL, degre REAL, quantite REAL NOT NULL);")

# VENTES
# ajout d'une clé primaire avec la propriété autoincrement
curseur.execute("CREATE TABLE Ventes (idVente INTEGER PRIMARY KEY AUTOINCREMENT, idEmploye TEXT NOT NULL, idBoisson INTEGER NOT NULL, date TEXT NOT NULL, FOREIGN KEY (idEmploye) REFERENCES Employes(matricule), FOREIGN KEY (idBoisson) REFERENCES Carte(idBoisson));")

# Remplissage avec les données CSV
# On écrit les informations dans une liste de dictionnaires
# chaque dictionnaire : 'attribut' : valeur de l'attribut
PATH = "../data/"
with open(PATH+"employes.csv", "rt") as fichierEmployes:
    CSVEmploye = csv.DictReader(fichierEmployes, delimiter="\t")
    for ligne in CSVEmploye:
        curseur.execute("INSERT INTO Employes (matricule, nomEmploye, prenomEmploye, profession, bar) VALUES (:Matricule, :Nom, :Prenom, :Profession, :Nom_Bar)", ligne)

with open(PATH+"etablissements.csv", "rt") as fichierEtablissement:
    CSVEtablissement = csv.DictReader(fichierEtablissement, delimiter="\t")
    for ligne in CSVEtablissement:
        curseur.execute("INSERT INTO Etablissements (nomEtablissement, adresse, numTelephone, idManager) VALUES (:Name, :Adresse, :NumTel, :Manager_Id)", ligne)

with open(PATH+"carte.csv", "rt") as fichierCarte:
    CSVCarte = csv.DictReader(fichierCarte, delimiter="\t")
    for ligne in CSVCarte:
        curseur.execute("INSERT INTO Carte (idBoisson, nomBoisson, type, prix, degre, quantite) VALUES (:Id_Boisson, :Nom, :Type, :Prix, :Degre, :Quantite)", ligne)
        
with open(PATH+"ventes.csv", "rt") as fichierVente:
    CSVVente = csv.DictReader(fichierVente, delimiter="\t")
    for ligne in CSVVente:
        curseur.execute("INSERT INTO Ventes (idEmploye, idBoisson, date) VALUES (:Employe_Id, :Boisson_Id, :Date)", ligne)

BDD.commit()
BDD.close()
