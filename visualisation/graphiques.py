import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

class VisualisationEtudiants:
    """Génération de graphiques interactifs"""
    
    @staticmethod
    def barplot_filieres(df):
        """Graphique des effectifs par filière"""
        if len(df) == 0:
            return None
        
        counts = df['filiere'].value_counts().reset_index()
        counts.columns = ['Filière', 'Nombre']
        
        fig = px.bar(
            counts, 
            x='Filière', 
            y='Nombre',
            title="Effectifs par filière",
            color='Nombre',
            color_continuous_scale='Viridis',
            text='Nombre'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def pie_genre(df):
        """Camembert de répartition par genre"""
        if len(df) == 0:
            return None
        
        counts = df['genre'].value_counts()
        
        fig = px.pie(
            values=counts.values,
            names=counts.index,
            title="Répartition par genre",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def histogramme_moyennes(df):
        """Histogramme des moyennes"""
        if len(df) == 0:
            return None
        
        fig = px.histogram(
            df,
            x='moyenne_actuelle',
            nbins=20,
            title="Distribution des moyennes",
            labels={'moyenne_actuelle': 'Moyenne /20', 'count': 'Nombre d\'étudiants'},
            color_discrete_sequence=['#1E88E5']
        )
        fig.add_vline(x=10, line_dash="dash", line_color="red", 
                      annotation_text="Seuil alerte")
        fig.add_vline(x=12, line_dash="dash", line_color="green",
                      annotation_text="Moyenne passable")
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def barplot_niveaux(df):
        """Graphique des effectifs par niveau"""
        if len(df) == 0:
            return None
        
        ordre = ["L1", "L2", "L3", "M1", "M2"]
        counts = df['niveau'].value_counts()
        counts = counts.reindex(ordre, fill_value=0).reset_index()
        counts.columns = ['Niveau', 'Nombre']
        
        fig = px.bar(
            counts,
            x='Niveau',
            y='Nombre',
            title="Effectifs par niveau d'étude",
            color='Nombre',
            text='Nombre'
        )
        fig.update_layout(height=450)
        return fig
    
    @staticmethod
    def scatter_moyenne_absences(df):
        """Nuage de points moyenne vs absences"""
        if len(df) == 0:
            return None
        
        fig = px.scatter(
            df,
            x='nombre_absences',
            y='moyenne_actuelle',
            title="Corrélation : Absences vs Moyenne",
            labels={'nombre_absences': "Nombre d'absences", 'moyenne_actuelle': "Moyenne /20"},
            color='filiere',
            size='age',
            hover_data=['nom', 'prenom'],
            trendline="ols"
        )
        fig.update_layout(height=550)
        return fig
    
    @staticmethod
    def barplot_hebergement(df):
        """Graphique des types d'hébergement"""
        if len(df) == 0:
            return None
        
        counts = df['hebergement'].value_counts().reset_index()
        counts.columns = ["Type d'hébergement", "Nombre"]
        
        fig = px.bar(
            counts,
            x="Type d'hébergement",
            y="Nombre",
            title="Répartition par type d'hébergement",
            color="Nombre",
            text="Nombre"
        )
        fig.update_layout(height=450)
        return fig
    
    @staticmethod
    def gauge_moyenne_generale(moyenne):
        """Jauge de la moyenne générale"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=moyenne,
            title={"text": "Moyenne Générale (/20)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 20], 'tickwidth': 1},
                'bar': {'color': "#1E88E5"},
                'steps': [
                    {'range': [0, 10], 'color': "#FF6B6B"},
                    {'range': [10, 15], 'color': "#FFE082"},
                    {'range': [15, 20], 'color': "#81C784"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        fig.update_layout(height=300)
        return fig
    
    @staticmethod
    def sunburst_filiere_niveau(df):
        """Graphique en sunburst (filière → niveau)"""
        if len(df) == 0:
            return None
        
        # Préparation des données
        sunburst_data = df.groupby(['filiere', 'niveau']).size().reset_index(name='count')
        
        fig = px.sunburst(
            sunburst_data,
            path=['filiere', 'niveau'],
            values='count',
            title="Hiérarchie : Filière → Niveau",
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=550)
        return fig
    
    @staticmethod
    def barplot_ville(df):
        """Graphique des villes d'origine"""
        if len(df) == 0:
            return None
        
        counts = df['ville'].value_counts().head(10).reset_index()
        counts.columns = ["Ville", "Nombre"]
        
        fig = px.bar(
            counts,
            x="Ville",
            y="Nombre",
            title="Top 10 des villes d'origine",
            color="Nombre",
            text="Nombre"
        )
        fig.update_layout(height=450)
        return fig