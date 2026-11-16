import pandas as pd
import numpy as np
class AnalyseurHabitudes:
    def __init__(self, collection, seuil_minutes=30):
        self.collection = collection          
        self.seuil_minutes = seuil_minutes    # trou de temps maximal entre deux sessions decoutes
        self.df_ecoutes = self.preparer_donnees()

    def preparer_donnees(self):
        utilisateurs = []
        dates = []
        jours = []
        heures = []

        for ecoute in self.collection.ecoutes:
            utilisateurs.append(ecoute.utilisateur.nom)   # le nom, pas l'objet
            dates.append(ecoute.date_heure)               # en utc, si le temps me permet dautre fuseau
            jours.append(ecoute.jour_semaine())
            heures.append(ecoute.heure())

        return pd.DataFrame({
            "utilisateur": utilisateurs,
            "date": dates,
            "jour": jours,
            "heure": heures
        })

    def matrice_jour_heure(self, utilisateur):     #matrice 7x24 nombre decoute
        masque = self.df_ecoutes["utilisateur"] == utilisateur
        df_utilisateur = self.df_ecoutes[masque]
        
        # Aucun écoute pour cet utilisateur : matrice vide
        if len(df_utilisateur) == 0:
            return np.zeros((7, 24))

        #Créer une serie jour-heure-nb ecoute
        compte = df_utilisateur.groupby["jour","heure"].size()  
        
        matrice = np.zero((7,24))

        compte = compte.reset_index()
        for i in range(len(compte)):
            ligne = compte.iloc[i]
            jour = int(ligne["jour"])
            heure = int(ligne["heure"])
            matrice[jour, heure] += ligne[0]

        # Nombre de semaines couvertes par les écoutes de l'utilisateur
        nb_jours = (df_utilisateur["date"].max() - df_utilisateur["date"].min()).days + 1
        nb_semaines = max(1, nb_jours / 7)

        # Moyenne d'écoutes par semaine pour chaque jour et chaque heure
        matrice = matrice / nb_semaines
        
        return matrice

        


        