import pandas as pd
import numpy as np

class AnalyseStatistique:
    """Analyse descriptive des données étudiants"""
    
    def __init__(self, df):
        self.df = df
        if len(df) > 0:
            self.df_clean = df.dropna(subset=['moyenne_actuelle', 'age'])
        else:
            self.df_clean = df
    
    def analyse_complete(self):
        """Rapport d'analyse complet"""
        if len(self.df) == 0:
            return {"erreur": "Aucune donnée disponible"}
        
        rapport = {
            "effectif_total": len(self.df),
            "repartition_genre": self.repartition_genre(),
            "repartition_filiere": self.repartition_filiere(),
            "repartition_niveau": self.repartition_niveau(),
            "statistiques_moyennes": self.statistiques_moyennes(),
            "statistiques_age": self.statistiques_age(),
            "statistiques_absences": self.statistiques_absences(),
            "top_etudiants": self.top_etudiants(),
            "alertes_academiques": self.alertes_academiques(),
            "taux_boursiers": self.taux_boursiers(),
            "repartition_hebergement": self.repartition_hebergement(),
            "repartition_ville": self.repartition_ville()
        }
        
        return rapport
    
    def repartition_genre(self):
        """Répartition par genre"""
        if 'genre' in self.df.columns:
            return self.df['genre'].value_counts().to_dict()
        return {}
    
    def repartition_filiere(self):
        """Répartition par filière"""
        if 'filiere' in self.df.columns:
            return self.df['filiere'].value_counts().to_dict()
        return {}
    
    def repartition_niveau(self):
        """Répartition par niveau"""
        if 'niveau' in self.df.columns:
            ordre = ["L1", "L2", "L3", "M1", "M2"]
            counts = self.df['niveau'].value_counts()
            return {niveau: counts.get(niveau, 0) for niveau in ordre}
        return {}
    
    def statistiques_moyennes(self):
        """Statistiques des moyennes"""
        if 'moyenne_actuelle' in self.df.columns:
            return {
                "moyenne_generale": round(self.df['moyenne_actuelle'].mean(), 2),
                "mediane": round(self.df['moyenne_actuelle'].median(), 2),
                "minimum": round(self.df['moyenne_actuelle'].min(), 2),
                "maximum": round(self.df['moyenne_actuelle'].max(), 2),
                "ecart_type": round(self.df['moyenne_actuelle'].std(), 2)
            }
        return {}
    
    def statistiques_age(self):
        """Statistiques des âges"""
        if 'age' in self.df.columns:
            return {
                "age_moyen": round(self.df['age'].mean(), 1),
                "age_min": int(self.df['age'].min()),
                "age_max": int(self.df['age'].max())
            }
        return {}
    
    def statistiques_absences(self):
        """Statistiques des absences"""
        if 'nombre_absences' in self.df.columns:
            return {
                "total_absences": int(self.df['nombre_absences'].sum()),
                "moyenne_absences": round(self.df['nombre_absences'].mean(), 1),
                "max_absences": int(self.df['nombre_absences'].max())
            }
        return {}
    
    def top_etudiants(self, n=5):
        """Top n étudiants avec meilleures moyennes"""
        if 'moyenne_actuelle' in self.df.columns:
            top = self.df.nlargest(n, 'moyenne_actuelle')[['nom', 'prenom', 'filiere', 'moyenne_actuelle']]
            return top.to_dict('records')
        return []
    
    def alertes_academiques(self, seuil=10):
        """Étudiants en dessous du seuil"""
        if 'moyenne_actuelle' in self.df.columns:
            alertes = self.df[self.df['moyenne_actuelle'] < seuil][['nom', 'prenom', 'filiere', 'moyenne_actuelle', 'nombre_absences']]
            return alertes.to_dict('records')
        return []
    
    def taux_boursiers(self):
        """Pourcentage de boursiers"""
        if 'boursier' in self.df.columns:
            total = len(self.df)
            boursiers = (self.df['boursier'] == "Oui").sum()
            return {
                "boursiers": int(boursiers),
                "non_boursiers": int(total - boursiers),
                "taux_boursiers": round(boursiers / total * 100, 1) if total > 0 else 0
            }
        return {}
    
    def repartition_hebergement(self):
        """Répartition par type d'hébergement"""
        if 'hebergement' in self.df.columns:
            return self.df['hebergement'].value_counts().to_dict()
        return {}
    
    def repartition_ville(self):
        """Répartition par ville d'origine"""
        if 'ville' in self.df.columns:
            return self.df['ville'].value_counts().to_dict()
        return {}
    
    def correlation_moyenne_absences(self):
        """Corrélation entre moyennes et absences"""
        if 'moyenne_actuelle' in self.df.columns and 'nombre_absences' in self.df.columns:
            return round(self.df['moyenne_actuelle'].corr(self.df['nombre_absences']), 3)
        return 0