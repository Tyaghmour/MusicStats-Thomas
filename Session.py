class Session:
    def __init__(self, ecoutes):
        self.ecoutes = ecoutes

    def debut(self):
        return self.ecoutes[0].date_heure

    def fin(self):
        return self.ecoutes[-1].date_heure

    def duree(self):
        # durée en minutes entre la première et la dernière écoute
        return (self.fin() - self.debut()).total_seconds() / 60

    def nombre_chansons(self):
        return len(self.ecoutes)