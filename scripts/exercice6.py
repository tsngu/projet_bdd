#!/usr/bin/env python
# -*- coding:utf-8 -*

########## EXERCICE 6 #########

import sqlite3 as sql
import csv

BDD = sql.connect("BARS.db")
curseur = BDD.cursor()

# Je reprends l'identification de l'exo 5.

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

        # On demande le mois à l'utilisateur. Si l'utilisateur entre 11 alors on lui donne les informations, sinon le système s'arrête.
        mois = input("De quel mois voulez-vous les informations ? (nombre entre 1 et 12) : ")
        if (mois == "11"):
            print("Voici les informations demandées : ")
            print()

            # Pour le nombre de ventes et le montant des ventes.
            # Besoin de idVente, prix, bar dans les tables Ventes, Carte et Employes.
            # Jointure sur les trois tables.
            # On compte les ventes, on fait la somme de ces ventes en imposant la condition que bar = l'établissement du manager.

            curseur.execute("SELECT COUNT(idVente), SUM(prix), bar FROM Ventes AS V, Carte AS C, Employes AS E\
                WHERE E.matricule = V.idEmploye AND V.idBoisson = C.idBoisson AND E.bar = ?", (etablissement,))
            resultventes = curseur.fetchall()
            for nb, prix, bar in resultventes:
                print("Ce mois-ci, au bar " + bar + " il y a eu " + str(nb) + " ventes, pour un montant de " + str(round(prix, 2)) + "€.")
            
            print()
            # Pour le bénéfice généré pour chaque employé du bar.
            # Besoin de idBoisson dans la table Ventes.
            # Besoin du prénom et du nom de l'employé dans la table Employes.
            # Besoin de prix dans la table Carte.
            # Jointure des 3 tables.
            # Somme des prix qu'on trie par les employés de l'établissement.

            curseur.execute("SELECT prenomEmploye, nomEmploye, SUM(prix) FROM Ventes AS V, Carte AS C, Employes AS E\
                WHERE V.idBoisson = C.idBoisson AND E.matricule = V.idEmploye AND E.bar = ? GROUP BY idEmploye", (etablissement,))

            resultbenef = curseur.fetchall()
            for prenom, nom, benef in resultbenef:
                print(nom + " " + prenom + " a généré un bénéfice de " + str(round(benef, 2)) + "€.")


        elif (mois == "1") or (mois == "2") or (mois == "3") or (mois == "4") or (mois == "5") or (mois == "6") or (mois == "7") or (mois == "8") or (mois == "9") or (mois == "10") or (mois == "12"):
            print("Il n'y a pas d'informations sur ce mois.")
        else:
            print("Ce n'est pas compris entre 1 et 12.")
    else:
        print("Ce n'est pas une réponse acceptée, le système va s'éteindre.")

BDD.close()