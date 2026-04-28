import pandas as pd
from datetime import datetime

class GenerateurRapport:
    """Génération de rapports en différents formats"""
    
    @staticmethod
    def generer_rapport_texte(analyse):
        """Génère un rapport texte"""
        rapport = []
        rapport.append("="*60)
        rapport.append("RAPPORT DESCRIPTIF DES ÉTUDIANTS")
        rapport.append(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        rapport.append("="*60)
        rapport.append("")
        
        if "erreur" in analyse:
            rapport.append(analyse["erreur"])
            return "\n".join(rapport)
        
        rapport.append(f"📊 EFFECTIF TOTAL : {analyse['effectif_total']} étudiants")
        rapport.append("")
        
        rapport.append("👥 RÉPARTITION PAR GENRE :")
        for genre, count in analyse.get('repartition_genre', {}).items():
            pourc = count / analyse['effectif_total'] * 100
            rapport.append(f"   • {genre} : {count} ({pourc:.1f}%)")
        rapport.append("")
        
        rapport.append("🎓 RÉPARTITION PAR FILIÈRE :")
        for filiere, count in analyse.get('repartition_filiere', {}).items():
            pourc = count / analyse['effectif_total'] * 100
            rapport.append(f"   • {filiere} : {count} ({pourc:.1f}%)")
        rapport.append("")
        
        rapport.append("📚 STATISTIQUES ACADÉMIQUES :")
        stats_moy = analyse.get('statistiques_moyennes', {})
        rapport.append(f"   • Moyenne générale : {stats_moy.get('moyenne_generale', 'N/A')}/20")
        rapport.append(f"   • Médiane : {stats_moy.get('mediane', 'N/A')}/20")
        rapport.append(f"   • Meilleure moyenne : {stats_moy.get('maximum', 'N/A')}/20")
        rapport.append(f"   • Plus faible moyenne : {stats_moy.get('minimum', 'N/A')}/20")
        rapport.append("")
        
        rapport.append("🏆 TOP 5 ÉTUDIANTS :")
        for i, etudiant in enumerate(analyse.get('top_etudiants', [])[:5], 1):
            rapport.append(f"   {i}. {etudiant['prenom']} {etudiant['nom']} - {etudiant['moyenne_actuelle']}/20 ({etudiant['filiere']})")
        rapport.append("")
        
        rapport.append("⚠️ ALERTES ACADÉMIQUES :")
        alertes = analyse.get('alertes_academiques', [])
        if alertes:
            for etudiant in alertes:
                rapport.append(f"   • {etudiant['prenom']} {etudiant['nom']} : {etudiant['moyenne_actuelle']}/20 ({etudiant['nombre_absences']} absences)")
        else:
            rapport.append("   ✅ Aucune alerte détectée")
        
        rapport.append("")
        rapport.append("="*60)
        rapport.append("FIN DU RAPPORT")
        
        return "\n".join(rapport)
    
    @staticmethod
    def generer_csv(df, filename="export_etudiants.csv"):
        """Exporte les données en CSV"""
        df.to_csv(f"data/{filename}", index=False, encoding='utf-8-sig')
        return f"data/{filename}"