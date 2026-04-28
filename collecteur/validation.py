import re

class ValidationDonnees:
    """Validation des données entrées par les étudiants"""
    
    @staticmethod
    def valider_email(email):
        """Valide le format d'un email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def valider_telephone(telephone):
        """Valide le numéro de téléphone (Cameroun)"""
        # Formats acceptés : 6XXXXXXXX, 6X XXX XXX, +237 6XXXXXXXX
        telephone_propre = re.sub(r'[\s\+]', '', telephone)
        pattern = r'^[67]\d{8}$'
        return bool(re.match(pattern, telephone_propre))
    
    @staticmethod
    def valider_age(age):
        """Valide l'âge (entre 16 et 99 ans)"""
        try:
            age_int = int(age)
            return 16 <= age_int <= 99
        except:
            return False
    
    @staticmethod
    def valider_moyenne(moyenne):
        """Valide la moyenne (entre 0 et 20)"""
        try:
            moy_float = float(moyenne)
            return 0 <= moy_float <= 20
        except:
            return False
    
    @staticmethod
    def valider_absences(absences):
        """Valide le nombre d'absences (entre 0 et 100)"""
        try:
            abs_int = int(absences)
            return 0 <= abs_int <= 100
        except:
            return False
    
    @staticmethod
    def nettoyer_telephone(telephone):
        """Nettoie le numéro de téléphone"""
        return re.sub(r'[\s\+]', '', telephone)