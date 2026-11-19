import pandas as pd
import numpy as np
import Session

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
        ecoutes = []

        for ecoute in self.collection.ecoutes:
            utilisateurs.append(ecoute.utilisateur.nom)   # le nom, pas l'objet
            dates.append(ecoute.date_heure)               # en utc, si le temps me permet dautre fuseau
            jours.append(ecoute.jour_semaine())
            heures.append(ecoute.heure())
            ecoutes.append(ecoute)


        return pd.DataFrame({
            "utilisateur": utilisateurs,
            "date": dates,
            "jour": jours,
            "heure": heures,
            "ecoutes": ecoutes
        })

    def matrice_jour_heure(self, utilisateur):     #matrice 7x24 nombre decoute
        masque = self.df_ecoutes["utilisateur"] == utilisateur
        df_utilisateur = self.df_ecoutes[masque]
        
        # Aucun écoute pour cet utilisateur alors matrice vide
        if len(df_utilisateur) == 0:
            return np.zeros((7, 24))

        #Créer une serie jour-heure-nb_ecoute
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

    def decouper_sessions(self, utilisateur):
        masque = self.df_ecoutes["utilisateur"] == utilisateur
        df_utilisateur = self.df_ecoutes[masque].sort_values("date")   # du plus ancien au plus récent

        sessions = []              
        ecoutes = []               # écoutes de la session en cours
        date_precedente = None     # aucune date précedente avec la première

        for i in range(len(df_utilisateur)):
            ligne = df_utilisateur.iloc[i]
            date = ligne["date"]

            if date_precedente is not None:
                ecart = (date - date_precedente).total_seconds() / 60   # écart en minutes
                if ecart > self.seuil_minutes:
                    # Trop de temps depuis la dernière écoute alors fin de cette sesion
                    sessions.append(Session(ecoutes))
                    ecoutes = []

            ecoutes.append(ligne["ecoute"])
            date_precedente = date

        # Fermer la dernière session
        if len(ecoutes) > 0:
            sessions.append(Session(ecoutes))

        return sessions


    def statistiques(self, utilisateur):
        sessions = self.decouper_sessions(utilisateur)

        # Aucune session : pas de statistiques possibles
        if len(sessions) == 0:
            return None

        matrice = self.matrice_jour_heure(utilisateur)
        stats = {}
        stats["nb_sessions"] = len(sessions)

        durees_sessions = [session.duree() for session in sessions]
        stats["duree_moy"] = np.mean(durees_sessions)
        stats["duree_max"] = np.max(durees_sessions)

        chansons_sessions = [session.nombre_chansons() for session in sessions]
        stats["chansons_par_session"] = np.mean(chansons_sessions)

        # Somme des 7 jours pour chaque heure puis l'heure avec le plus d'écoutes
        stats["heure_pointe"] = np.argmax(matrice.sum(axis=0))
        # Somme des 24 heures pour chaque jour puis le jour avec le plus d'écoutes
        stats["jour_favori"] = np.argmax(matrice.sum(axis=1))

        return stats

    def comparer(self, utilisateur_a, utilisateur_b):
        return self.statistiques(utilisateur_a), self.statistiques(utilisateur_b)