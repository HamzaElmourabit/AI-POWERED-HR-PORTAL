import openai
import json
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # OpenAI client is already configured via environment variables
        self.client = openai.OpenAI()

    def analyze_resume(self, resume_text: str, job_description: str = None) -> Dict:
        """
        Analyse un CV avec l'IA pour extraire les compétences, l'expérience et calculer un score.
        """
        try:
            prompt = f"""
            Analysez ce CV et extrayez les informations suivantes au format JSON:
            
            CV:
            {resume_text}
            
            {"Description du poste:" + job_description if job_description else ""}
            
            Retournez un JSON avec:
            - skills: liste des compétences techniques et soft skills
            - experience_years: nombre d'années d'expérience estimé
            - education: formation et diplômes
            - summary: résumé professionnel en 2-3 phrases
            - score: score de 0 à 100 basé sur la qualité du profil
            {"- job_match_score: score de 0 à 100 pour l'adéquation au poste" if job_description else ""}
            - strengths: points forts du candidat
            - areas_for_improvement: axes d'amélioration
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert RH spécialisé dans l'analyse de CV. Répondez uniquement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du CV: {str(e)}")
            return {
                "skills": [],
                "experience_years": 0,
                "education": "",
                "summary": "Analyse non disponible",
                "score": 0,
                "job_match_score": 0 if job_description else None,
                "strengths": [],
                "areas_for_improvement": []
            }

    def generate_interview_questions(self, job_title: str, candidate_profile: Dict) -> List[str]:
        """
        Génère des questions d'entretien personnalisées basées sur le poste et le profil du candidat.
        """
        try:
            prompt = f"""
            Générez 8-10 questions d'entretien pertinentes pour:
            
            Poste: {job_title}
            Profil candidat: {json.dumps(candidate_profile, indent=2)}
            
            Incluez:
            - 2-3 questions techniques spécifiques au poste
            - 2-3 questions comportementales
            - 2-3 questions sur l'expérience passée
            - 1-2 questions sur la motivation et les objectifs
            
            Retournez une liste JSON de questions.
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert RH. Générez des questions d'entretien pertinentes et professionnelles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            questions = json.loads(response.choices[0].message.content)
            return questions if isinstance(questions, list) else []

        except Exception as e:
            logger.error(f"Erreur lors de la génération des questions: {str(e)}")
            return [
                "Pouvez-vous vous présenter en quelques minutes?",
                "Pourquoi ce poste vous intéresse-t-il?",
                "Quelles sont vos principales forces?",
                "Décrivez un défi professionnel que vous avez surmonté.",
                "Où vous voyez-vous dans 5 ans?"
            ]

    def analyze_performance_data(self, employee_data: Dict, performance_history: List[Dict]) -> Dict:
        """
        Analyse les données de performance d'un employé et génère des insights IA.
        """
        try:
            prompt = f"""
            Analysez les données de performance de cet employé:
            
            Données employé: {json.dumps(employee_data, indent=2)}
            Historique performance: {json.dumps(performance_history, indent=2)}
            
            Générez une analyse JSON avec:
            - performance_trend: tendance (amélioration/stable/déclin)
            - predicted_score: score prédit pour la prochaine évaluation (0-100)
            - strengths: forces identifiées
            - development_areas: axes de développement
            - recommendations: recommandations spécifiques
            - training_suggestions: formations suggérées
            - risk_factors: facteurs de risque (turnover, etc.)
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un analyste RH expert en performance. Fournissez des insights précis et actionnables."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de performance: {str(e)}")
            return {
                "performance_trend": "stable",
                "predicted_score": 75,
                "strengths": [],
                "development_areas": [],
                "recommendations": [],
                "training_suggestions": [],
                "risk_factors": []
            }

    def generate_job_description(self, job_title: str, department: str, requirements: List[str]) -> Dict:
        """
        Génère une description de poste optimisée avec l'IA.
        """
        try:
            prompt = f"""
            Créez une description de poste professionnelle pour:
            
            Titre: {job_title}
            Département: {department}
            Exigences: {', '.join(requirements)}
            
            Générez un JSON avec:
            - description: description détaillée du poste
            - responsibilities: liste des responsabilités principales
            - qualifications: qualifications requises
            - preferred_skills: compétences préférées
            - keywords: mots-clés pour le matching IA
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert en rédaction de descriptions de poste. Créez du contenu professionnel et attractif."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Erreur lors de la génération de description: {str(e)}")
            return {
                "description": f"Poste de {job_title} au sein du département {department}",
                "responsibilities": [],
                "qualifications": requirements,
                "preferred_skills": [],
                "keywords": []
            }

    def chatbot_response(self, user_message: str, context: Dict = None) -> str:
        """
        Génère une réponse de chatbot RH intelligent.
        """
        try:
            context_str = f"Contexte: {json.dumps(context, indent=2)}" if context else ""
            
            prompt = f"""
            Vous êtes un assistant RH virtuel. Répondez à cette question de manière professionnelle et utile:
            
            Question: {user_message}
            {context_str}
            
            Fournissez une réponse claire, précise et professionnelle.
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant RH professionnel, serviable et bienveillant. Répondez de manière claire et concise."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse chatbot: {str(e)}")
            return "Je suis désolé, je ne peux pas traiter votre demande pour le moment. Veuillez réessayer plus tard."

    def predict_turnover_risk(self, employee_data: Dict, team_data: List[Dict] = None) -> Dict:
        """
        Prédit le risque de turnover d'un employé.
        """
        try:
            team_context = f"Données équipe: {json.dumps(team_data, indent=2)}" if team_data else ""
            
            prompt = f"""
            Analysez le risque de turnover pour cet employé:
            
            Données employé: {json.dumps(employee_data, indent=2)}
            {team_context}
            
            Retournez un JSON avec:
            - risk_score: score de risque de 0 à 100
            - risk_level: niveau (faible/moyen/élevé)
            - risk_factors: facteurs de risque identifiés
            - retention_strategies: stratégies de rétention suggérées
            - timeline: horizon temporel estimé
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert en analytics RH spécialisé dans la prédiction de turnover."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Erreur lors de la prédiction de turnover: {str(e)}")
            return {
                "risk_score": 50,
                "risk_level": "moyen",
                "risk_factors": [],
                "retention_strategies": [],
                "timeline": "6-12 mois"
            }

