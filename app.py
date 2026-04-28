# app.py - Application principale de collecte des données étudiants
import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Student Data Collector",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Import des modules personnalisés
from database import BaseDonnees
from collecteur.formulaire import FormulaireCollecte
from analyse.stats import AnalyseStatistique
from analyse.reporting import GenerateurRapport
from visualisation.graphiques import VisualisationEtudiants
from config import SEUIL_MOYENNE_ALERTE

# Initialisation de la base de données
@st.cache_resource
def init_db():
    return BaseDonnees()

db = init_db()

# Initialisation de l'état de session
if 'page' not in st.session_state:
    st.session_state['page'] = 'accueil'

# Sidebar - Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=80)
    st.markdown("## 🎓 Student Data Collector")
    st.markdown("---")
    
    pages = {
        "🏠 Accueil": "accueil",
        "📝 Nouvelle inscription": "inscription",
        "📊 Tableau de bord": "dashboard",
        "👥 Liste des étudiants": "liste",
        "📈 Analyses": "analyses",
        "📁 Export données": "export"
    }
    
    for label, page_key in pages.items():
        if st.button(label, use_container_width=True):
            st.session_state['page'] = page_key
            st.rerun()
    
    st.markdown("---")
    st.caption(f"Version 1.0\nTP INF232 EC2")

# Page d'accueil
if st.session_state['page'] == 'accueil':
    st.markdown('<div class="main-header">🎓 Student Data Collector</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    stats = db.stats_globales()
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div>📚 Total Étudiants</div>
            <div class="stat-number">{stats['total']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div>🎂 Âge moyen</div>
            <div class="stat-number">{stats['moyenne_age']} ans</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div>📊 Moyenne générale</div>
            <div class="stat-number">{stats['moyenne_notes']}/20</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Objectif de l'application")
        st.markdown("""
        Cette application permet de :
        - ✅ Collecter les informations des étudiants via un formulaire
        - ✅ Stocker et gérer les données
        - ✅ Analyser les performances académiques
        - ✅ Visualiser les tendances et statistiques
        - ✅ Générer des rapports automatisés
        """)
    
    with col2:
        st.subheader("📊 Indicateurs clés")
        
        df = db.obtenir_tous()
        if len(df) > 0:
            analyse = AnalyseStatistique(df)
            rapport = analyse.analyse_complete()
            
            st.metric("🏆 Meilleure moyenne", f"{rapport['statistiques_moyennes'].get('maximum', 'N/A')}/20")
            st.metric("⚠️ Étudiants en alerte", len(rapport.get('alertes_academiques', [])))
            st.metric("👥 Boursiers", f"{rapport.get('taux_boursiers', {}).get('taux_boursiers', 0)}%")
        else:
            st.info("Aucune donnée disponible. Commencez par inscrire des étudiants !")
    
    st.markdown("---")
    st.info("👈 Utilisez le menu latéral pour naviguer")

# Page d'inscription
elif st.session_state['page'] == 'inscription':
    formulaire = FormulaireCollecte(db)
    formulaire.afficher()

# Page tableau de bord
elif st.session_state['page'] == 'dashboard':
    st.subheader("📊 Tableau de bord")
    
    df = db.obtenir_tous()
    
    if len(df) == 0:
        st.warning("⚠️ Aucun étudiant inscrit. Utilisez le formulaire d'inscription.")
    else:
        analyse = AnalyseStatistique(df)
        rapport = analyse.analyse_complete()
        
        # Métriques rapides
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total étudiants", rapport['effectif_total'])
        with col2:
            st.metric("Filières représentées", len(rapport['repartition_filiere']))
        with col3:
            st.metric("Âge moyen", f"{rapport['statistiques_age'].get('age_moyen', 'N/A')} ans")
        with col4:
            st.metric("Moyenne générale", f"{rapport['statistiques_moyennes'].get('moyenne_generale', 'N/A')}/20")
        
        st.markdown("---")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            fig = VisualisationEtudiants.barplot_filieres(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = VisualisationEtudiants.pie_genre(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = VisualisationEtudiants.barplot_niveaux(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            fig = VisualisationEtudiants.scatter_moyenne_absences(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

# Page liste des étudiants
elif st.session_state['page'] == 'liste':
    st.subheader("👥 Liste des étudiants inscrits")
    
    df = db.obtenir_tous()
    
    if len(df) == 0:
        st.info("Aucun étudiant inscrit")
    else:
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            filtre_filiere = st.multiselect("Filtrer par filière", df['filiere'].unique())
        
        with col2:
            filtre_niveau = st.multiselect("Filtrer par niveau", df['niveau'].unique())
        
        # Application des filtres
        df_filtre = df.copy()
        if filtre_filiere:
            df_filtre = df_filtre[df_filtre['filiere'].isin(filtre_filiere)]
        if filtre_niveau:
            df_filtre = df_filtre[df_filtre['niveau'].isin(filtre_niveau)]
        
        st.dataframe(
            df_filtre[['id', 'nom', 'prenom', 'filiere', 'niveau', 'moyenne_actuelle', 'ville']],
            use_container_width=True
        )
        
        st.caption(f"Affichage de {len(df_filtre)} étudiant(s) sur {len(df)} total")

# Page analyses
elif st.session_state['page'] == 'analyses':
    st.subheader("📈 Analyses statistiques avancées")
    
    df = db.obtenir_tous()
    
    if len(df) == 0:
        st.warning("Aucune donnée à analyser")
    else:
        analyse = AnalyseStatistique(df)
        rapport = analyse.analyse_complete()
        
        # Moyenne générale
        moyenne_gen = rapport['statistiques_moyennes'].get('moyenne_generale', 0)
        fig = VisualisationEtudiants.gauge_moyenne_generale(moyenne_gen)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = VisualisationEtudiants.histogramme_moyennes(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = VisualisationEtudiants.sunburst_filiere_niveau(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Corrélation
        st.subheader("🔍 Corrélation moyenne / absences")
        correlation = analyse.correlation_moyenne_absences()
        
        if correlation < -0.3:
            st.warning(f"⚠️ Corrélation négative forte ({correlation}) : Plus d'absences = notes plus basses")
        elif correlation > 0.3:
            st.success(f"✅ Corrélation positive ({correlation})")
        else:
            st.info(f"ℹ️ Corrélation faible ({correlation})")
        
        # Top étudiants
        st.subheader("🏆 Top 5 des meilleurs étudiants")
        top = rapport.get('top_etudiants', [])
        if top:
            for i, etud in enumerate(top, 1):
                st.markdown(f"{i}. **{etud['prenom']} {etud['nom']}** - {etud['moyenne_actuelle']}/20 ({etud['filiere']})")
        
        # Alertes
        st.subheader(f"⚠️ Alertes académiques (moyenne < {SEUIL_MOYENNE_ALERTE}/20)")
        alertes = rapport.get('alertes_academiques', [])
        if alertes:
            for etud in alertes:
                st.error(f"**{etud['prenom']} {etud['nom']}** - Moyenne: {etud['moyenne_actuelle']}/20 | Absences: {etud['nombre_absences']}")
        else:
            st.success("✅ Aucun étudiant en alerte")

# Page export
elif st.session_state['page'] == 'export':
    st.subheader("📁 Export des données")
    
    df = db.obtenir_tous()
    
    if len(df) == 0:
        st.info("Aucune donnée à exporter")
    else:
        st.info(f"📊 {len(df)} étudiant(s) disponible(s) à l'export")
        
        # Génération rapport texte
        if st.button("📄 Générer rapport texte", use_container_width=True):
            analyse = AnalyseStatistique(df)
            rapport = analyse.analyse_complete()
            rapport_texte = GenerateurRapport.generer_rapport_texte(rapport)
            
            st.download_button(
                label="📥 Télécharger rapport",
                data=rapport_texte,
                file_name=f"rapport_etudiants_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Export CSV
        if st.button("📊 Exporter en CSV", use_container_width=True):
            fichier = GenerateurRapport.generer_csv(df)
            with open(fichier, 'rb') as f:
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=f,
                    file_name=f"export_etudiants_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # Aperçu des données
        st.subheader("Aperçu des données")
        st.dataframe(df.head(10), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    TP INF232 EC2 - Application de collecte des données étudiants<br>
    © 2026 - Tous droits réservés
</div>
""", unsafe_allow_html=True)