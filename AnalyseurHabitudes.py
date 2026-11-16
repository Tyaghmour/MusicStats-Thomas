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

        nbecoute_jourheure = df_utilisateur.groupby["jour","heure"].size()    #size conte le nombre d'ecoute pour une 
        matrice = np.zero((7,24))
        


        