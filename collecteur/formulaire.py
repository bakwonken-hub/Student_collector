import streamlit as st
from datetime import datetime
from .validation import ValidationDonnees
from config import FILIERES, NIVEAUX, VILLES, OPTIONS_GENRE, OPTIONS_BOURSE, OPTIONS_HEBERGEMENT

class FormulaireCollecte:
    """Formulaire de collecte des données étudiants"""
    
    def __init__(self, db):
        self.db = db
        self.validation = ValidationDonnees()
    
    def afficher(self):
        """Affiche le formulaire de collecte"""
        st.subheader("📝 Nouvelle inscription étudiante")
        
        with st.form("formulaire_etudiant", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom *", placeholder="Ex: NDOUMBE")
                prenom = st.text_input("Prénom *", placeholder="Ex: Jean")
                email = st.text_input("Email *", placeholder="jean.ndoumbe@email.com")
                telephone = st.text_input("Téléphone *", placeholder="6XXXXXXXX")
                genre = st.selectbox("Genre *", OPTIONS_GENRE)
            
            with col2:
                filiere = st.selectbox("Filière *", FILIERES)
                niveau = st.selectbox("Niveau *", NIVEAUX)
                ville = st.selectbox("Ville d'origine *", VILLES)
                age = st.number_input("Âge *", min_value=16, max_value=99, step=1)
                boursier = st.selectbox("Boursier ?", OPTIONS_BOURSE)
            
            st.markdown("---")
            col3, col4 = st.columns(2)
            
            with col3:
                moyenne = st.number_input("Moyenne actuelle (/20)", min_value=0.0, max_value=20.0, step=0.5, value=12.0)
            
            with col4:
                absences = st.number_input("Nombre d'absences", min_value=0, max_value=100, step=1, value=0)
            
            hebergement = st.selectbox("Type d'hébergement", OPTIONS_HEBERGEMENT)
            
            st.caption("* : Champs obligatoires")
            
            submitted = st.form_submit_button("✅ Enregistrer l'étudiant", use_container_width=True)
            
            if submitted:
                # Validation
                erreurs = []
                
                if not nom:
                    erreurs.append("Le nom est obligatoire")
                if not prenom:
                    erreurs.append("Le prénom est obligatoire")
                if not email:
                    erreurs.append("L'email est obligatoire")
                elif not self.validation.valider_email(email):
                    erreurs.append("Format d'email invalide")
                
                if telephone and not self.validation.valider_telephone(telephone):
                    erreurs.append("Format de téléphone invalide (6XXXXXXXX)")
                
                if not self.validation.valider_age(age):
                    erreurs.append("Âge invalide (doit être entre 16 et 99 ans)")
                
                if not self.validation.valider_moyenne(moyenne):
                    erreurs.append("Moyenne invalide (doit être entre 0 et 20)")
                
                if erreurs:
                    for erreur in erreurs:
                        st.error(f"❌ {erreur}")
                else:
                    # Nettoyage du téléphone
                    telephone_clean = self.validation.nettoyer_telephone(telephone) if telephone else ""
                    
                    # Préparation des données
                    donnees = {
                        'nom': nom.upper(),
                        'prenom': prenom.capitalize(),
                        'email': email.lower(),
                        'telephone': telephone_clean,
                        'genre': genre,
                        'filiere': filiere,
                        'niveau': niveau,
                        'ville': ville,
                        'age': age,
                        'moyenne_actuelle': moyenne,
                        'nombre_absences': absences,
                        'boursier': boursier,
                        'hebergement': hebergement
                    }
                    
                    # Sauvegarde
                    etudiant_id = self.db.ajouter_etudiant(donnees)
                    st.success(f"✅ Étudiant inscrit avec succès ! ID: {etudiant_id}")
                    st.balloons()
                    
                    return True
        
        return False