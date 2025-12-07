
from typing import Dict, Any
import json
from datetime import datetime


class BackendManager:
    """Orchestrateur principal du backend"""
    
    def __init__(self):
        """Initialise le gestionnaire backend"""
        self.llm_engine = None  # Person A le remplira
        self.planner_logic = None  # Person B le remplira
        print("✅ BackendManager initialisé")
    
    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fonction principale - Point d'entrée du backend
        
        Args:
            user_input: Données de l'utilisateur
        
        Returns:
            Résultat combiné (AI + Planning)
        """
        try:
            # Étape 1 : Valider
            validated_data = self._validate_input(user_input)
            print("✓ Validation OK")
            
            # Étape 2 : IA
            ai_analysis = self._get_ai_analysis(validated_data)
            print("✓ Analyse IA OK")
            
            # Étape 3 : Planning
            study_plan = self._generate_study_plan(validated_data)
            print("✓ Planning OK")
            
            # Étape 4 : Combiner
            final_response = self._combine_results(ai_analysis, study_plan)
            print("✓ Résultats combinés OK")
            
            return final_response
            
        except Exception as e:
            return self._handle_error(e)
    
    def _validate_input(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Valide les données utilisateur"""
        required = ['subjects', 'deadlines', 'available_time']
        
        for field in required:
            if field not in user_input:
                raise ValueError(f"Champ manquant : {field}")
        
        return user_input
    
    def _get_ai_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Appelle l'IA (simulation pour l'instant)"""
        # SIMULATION - Person A remplacera ceci
        return {
            "analysis": f"Vous avez {len(data['subjects'])} matières à gérer",
            "recommendations": ["Prioriser les deadlines proches"],
            "difficulty": "medium"
        }
    
    def _generate_study_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère le planning (simulation pour l'instant)"""
        # SIMULATION - Person B remplacera ceci
        return {
            "weekly_schedule": [{"day": "Lundi", "subject": data['subjects'][0]}],
            "total_hours": 24
        }
    
    def _combine_results(self, ai_analysis: Dict, study_plan: Dict) -> Dict[str, Any]:
        """Combine AI + Planning"""
        return {
            "success": True,
            "ai_insights": ai_analysis,
            "study_plan": study_plan,
            "timestamp": datetime.now().isoformat()
        }
    
    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Gestion des erreurs"""
        return {
            "success": False,
            "error": str(error)
        }


def create_backend_manager():
    """Crée une instance du manager"""
    return BackendManager()


# TEST
if __name__ == "__main__":
    print("🧪 TEST DU BACKEND\n")
    
    manager = create_backend_manager()
    
    # Données de test
    test_input = {
        "subjects": ["Math", "Physique"],
        "deadlines": {"Math": "2024-12-20"},
        "available_time": {"daily_hours": 4, "days_per_week": 5}
    }
    
    result = manager.process_request(test_input)
    
    print("\n📊 Résultat :")
    print(json.dumps(result, indent=2, ensure_ascii=False))