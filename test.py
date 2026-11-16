import pandas as pd
from Artiste import Artiste
from Chanson import Chanson
from Utilisateur import Utilisateur
from Ecoute import Ecoute
from Collection import CollectionMusicale
from AnalyseurStatistique import AnalyseurStatistique
from GestionnaireGraphique import GestionnaireGraphiques
import matplotlib.pyplot as plt
import customtkinter as ctk
from PagePrevision import PagePrevision
from AnalyseurHabitudes import AnalyseurHabitudes
from GestionnaireCSV import GestionnaireCSV

collection = GestionnaireCSV().lire_fichier("ecoutes.csv")
analyseur = AnalyseurHabitudes(collection)
m = analyseur.matrice_jour_heure("Jazza")
print(m.shape)                 # (7, 24)
print(m[1, 9])                 # Tuesday 9h: should be > 0 (unless averaged)

#test