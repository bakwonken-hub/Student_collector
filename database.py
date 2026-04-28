import pandas as pd
import os
from datetime import datetime

class BaseDonnees:
    """Gestionnaire de base de données pour les étudiants"""
    
    def __init__(self, fichier="data/etudiants.csv"):
        self.fichier = fichier
        self.creer_dossier()
        self.initialiser_fichier()
    
    def creer_dossier(self):
        """Crée le dossier data s'il n'existe pas"""
        os.makedirs("data", exist_ok=True)
    
    def initialiser_fichier(self):
        """Crée le fichier CSV avec en-têtes s'il n'existe pas"""
        if not os.path.exists(self.fichier):
            df_vide = pd.DataFrame(columns=[
                'id', 'nom', 'prenom', 'email', 'telephone', 'genre',
                'filiere', 'niveau', 'ville', 'age', 'moyenne_actuelle',
                'nombre_absences', 'boursier', 'hebergement',
                'date_inscription', 'dernier_connexion'
            ])
            df_vide.to_csv(self.fichier, index=False, encoding='utf-8')
    
    def ajouter_etudiant(self, donnees):
        """Ajoute un nouvel étudiant"""
        df = pd.read_csv(self.fichier, encoding='utf-8')
        
        # Générer un ID unique
        if len(df) == 0:
            nouvel_id = 1
        else:
            nouvel_id = df['id'].max() + 1
        
        nouvelle_ligne = {
            'id': nouvel_id,
            **donnees,
            'date_inscription': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'dernier_connexion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        df.loc[len(df)] = nouvelle_ligne
        df.to_csv(self.fichier, index=False, encoding='utf-8')
        return nouvel_id
    
    def obtenir_tous(self):
        """Récupère tous les étudiants"""
        return pd.read_csv(self.fichier, encoding='utf-8')
    
    def obtenir_par_id(self, etudiant_id):
        """Récupère un étudiant par son ID"""
        df = self.obtenir_tous()
        return df[df['id'] == etudiant_id]
    
    def mettre_a_jour(self, etudiant_id, champ, valeur):
        """Met à jour un champ spécifique"""
        df = self.obtenir_tous()
        df.loc[df['id'] == etudiant_id, champ] = valeur
        df.to_csv(self.fichier, index=False, encoding='utf-8')
    
    def supprimer(self, etudiant_id):
        """Supprime un étudiant"""
        df = self.obtenir_tous()
        df = df[df['id'] != etudiant_id]
        df.to_csv(self.fichier, index=False, encoding='utf-8')
    
    def stats_globales(self):
        """Statistiques descriptives de base"""
        df = self.obtenir_tous()
        
        if len(df) == 0:
            return {
                "total": 0,
                "moyenne_age": 0,
                "moyenne_notes": 0,
                "taux_remplissage": 0
            }
        
        return {
            "total": len(df),
            "moyenne_age": round(df['age'].mean(), 1) if 'age' in df else 0,
            "moyenne_notes": round(df['moyenne_actuelle'].mean(), 1) if 'moyenne_actuelle' in df else 0,
            "taux_boursiers": round((df['boursier'] == "Oui").mean() * 100, 1) if 'boursier' in df else 0
        }