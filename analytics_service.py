import openai
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func
from src.models.user import db
from src.models.employee import Employee, PerformanceEvaluation
from src.models.candidate import Application, Candidate, JobPosting
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.client = openai.OpenAI()

    def get_employee_analytics(self) -> Dict:
        """Récupère les analytics des employés."""
        try:
            # Statistiques de base
            total_employees = Employee.query.filter_by(status='active').count()
            
            # Répartition par département
            dept_stats = db.session.query(
                Employee.department,
                func.count(Employee.id).label('count')
            ).filter_by(status='active').group_by(Employee.department).all()
            
            # Performance moyenne par département
            perf_stats = db.session.query(
                Employee.department,
                func.avg(Employee.performance_score).label('avg_score')
            ).filter_by(status='active').group_by(Employee.department).all()
            
            # Évolution des embauches sur 12 mois
            twelve_months_ago = datetime.now() - timedelta(days=365)
            hiring_trend = db.session.query(
                func.date_trunc('month', Employee.hire_date).label('month'),
                func.count(Employee.id).label('hires')
            ).filter(
                Employee.hire_date >= twelve_months_ago,
                Employee.status == 'active'
            ).group_by('month').order_by('month').all()
            
            return {
                'total_employees': total_employees,
                'department_distribution': [
                    {'department': dept, 'count': count} 
                    for dept, count in dept_stats
                ],
                'performance_by_department': [
                    {'department': dept, 'avg_score': round(float(avg_score or 0), 2)} 
                    for dept, avg_score in perf_stats
                ],
                'hiring_trend': [
                    {'month': month.strftime('%Y-%m'), 'hires': hires}
                    for month, hires in hiring_trend
                ]
            }
        
        except Exception as e:
            logger.error(f"Erreur dans get_employee_analytics: {str(e)}")
            return {}

    def get_recruitment_analytics(self) -> Dict:
        """Récupère les analytics de recrutement."""
        try:
            # Statistiques générales
            total_jobs = JobPosting.query.filter_by(status='active').count()
            total_candidates = Candidate.query.count()
            total_applications = Application.query.count()
            
            # Applications par statut
            app_status_stats = db.session.query(
                Application.status,
                func.count(Application.id).label('count')
            ).group_by(Application.status).all()
            
            # Score moyen des candidats
            avg_candidate_score = db.session.query(
                func.avg(Candidate.ai_score)
            ).scalar() or 0
            
            # Taux de conversion par étape
            conversion_rates = self._calculate_conversion_rates()
            
            # Temps moyen de recrutement
            avg_recruitment_time = self._calculate_avg_recruitment_time()
            
            return {
                'total_active_jobs': total_jobs,
                'total_candidates': total_candidates,
                'total_applications': total_applications,
                'avg_candidate_score': round(float(avg_candidate_score), 2),
                'applications_by_status': [
                    {'status': status, 'count': count} 
                    for status, count in app_status_stats
                ],
                'conversion_rates': conversion_rates,
                'avg_recruitment_time_days': avg_recruitment_time
            }
        
        except Exception as e:
            logger.error(f"Erreur dans get_recruitment_analytics: {str(e)}")
            return {}

    def get_performance_analytics(self) -> Dict:
        """Récupère les analytics de performance."""
        try:
            # Performance moyenne globale
            avg_performance = db.session.query(
                func.avg(Employee.performance_score)
            ).filter_by(status='active').scalar() or 0
            
            # Évolution des performances sur 6 mois
            six_months_ago = datetime.now() - timedelta(days=180)
            performance_trend = db.session.query(
                func.date_trunc('month', PerformanceEvaluation.evaluation_date).label('month'),
                func.avg(PerformanceEvaluation.overall_score).label('avg_score')
            ).filter(
                PerformanceEvaluation.evaluation_date >= six_months_ago
            ).group_by('month').order_by('month').all()
            
            # Distribution des scores de performance
            performance_distribution = self._get_performance_distribution()
            
            # Top performers
            top_performers = Employee.query.filter_by(status='active').order_by(
                Employee.performance_score.desc()
            ).limit(5).all()
            
            return {
                'avg_performance': round(float(avg_performance), 2),
                'performance_trend': [
                    {'month': month.strftime('%Y-%m'), 'avg_score': round(float(avg_score), 2)}
                    for month, avg_score in performance_trend
                ],
                'performance_distribution': performance_distribution,
                'top_performers': [
                    {
                        'name': f"{emp.first_name} {emp.last_name}",
                        'department': emp.department,
                        'score': emp.performance_score
                    }
                    for emp in top_performers
                ]
            }
        
        except Exception as e:
            logger.error(f"Erreur dans get_performance_analytics: {str(e)}")
            return {}

    def predict_turnover_risks(self) -> Dict:
        """Prédit les risques de turnover avec l'IA."""
        try:
            employees = Employee.query.filter_by(status='active').all()
            risk_predictions = []
            
            for employee in employees:
                # Récupération des données de performance
                evaluations = PerformanceEvaluation.query.filter_by(
                    employee_id=employee.id
                ).order_by(PerformanceEvaluation.evaluation_date.desc()).limit(3).all()
                
                # Calcul du risque avec l'IA
                risk_data = self._calculate_employee_risk(employee, evaluations)
                
                if risk_data['risk_score'] > 6.0:  # Seuil de risque
                    risk_predictions.append({
                        'employee_id': employee.id,
                        'name': f"{employee.first_name} {employee.last_name}",
                        'department': employee.department,
                        'risk_score': risk_data['risk_score'],
                        'risk_level': risk_data['risk_level'],
                        'risk_factors': risk_data['risk_factors'],
                        'recommendations': risk_data['recommendations']
                    })
            
            # Tri par score de risque décroissant
            risk_predictions.sort(key=lambda x: x['risk_score'], reverse=True)
            
            return {
                'high_risk_employees': len([r for r in risk_predictions if r['risk_score'] >= 8.0]),
                'medium_risk_employees': len([r for r in risk_predictions if 6.0 <= r['risk_score'] < 8.0]),
                'risk_predictions': risk_predictions[:10],  # Top 10 des risques
                'total_at_risk': len(risk_predictions)
            }
        
        except Exception as e:
            logger.error(f"Erreur dans predict_turnover_risks: {str(e)}")
            return {}

    def generate_ai_insights(self, analytics_data: Dict) -> Dict:
        """Génère des insights IA basés sur les données d'analytics."""
        try:
            prompt = f"""
            Analysez ces données RH et générez des insights actionnables:
            
            {json.dumps(analytics_data, indent=2)}
            
            Générez un JSON avec:
            - key_insights: 3-5 insights principaux
            - recommendations: actions recommandées
            - trends: tendances identifiées
            - alerts: alertes importantes
            - opportunities: opportunités d'amélioration
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Vous êtes un expert en analytics RH. Fournissez des insights précis et actionnables."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            insights = json.loads(response.choices[0].message.content)
            return insights

        except Exception as e:
            logger.error(f"Erreur dans generate_ai_insights: {str(e)}")
            return {
                "key_insights": [],
                "recommendations": [],
                "trends": [],
                "alerts": [],
                "opportunities": []
            }

    def _calculate_conversion_rates(self) -> Dict:
        """Calcule les taux de conversion du processus de recrutement."""
        try:
            total_applications = Application.query.count()
            if total_applications == 0:
                return {}
            
            screening_count = Application.query.filter_by(status='screening').count()
            interview_count = Application.query.filter_by(status='interview').count()
            hired_count = Application.query.filter_by(status='hired').count()
            
            return {
                'application_to_screening': round((screening_count / total_applications) * 100, 1),
                'screening_to_interview': round((interview_count / screening_count) * 100, 1) if screening_count > 0 else 0,
                'interview_to_hire': round((hired_count / interview_count) * 100, 1) if interview_count > 0 else 0,
                'overall_success_rate': round((hired_count / total_applications) * 100, 1)
            }
        
        except Exception as e:
            logger.error(f"Erreur dans _calculate_conversion_rates: {str(e)}")
            return {}

    def _calculate_avg_recruitment_time(self) -> float:
        """Calcule le temps moyen de recrutement."""
        try:
            hired_applications = Application.query.filter_by(status='hired').all()
            
            if not hired_applications:
                return 0
            
            total_days = 0
            for app in hired_applications:
                days_diff = (app.updated_at.date() - app.application_date).days
                total_days += days_diff
            
            return round(total_days / len(hired_applications), 1)
        
        except Exception as e:
            logger.error(f"Erreur dans _calculate_avg_recruitment_time: {str(e)}")
            return 0

    def _get_performance_distribution(self) -> List[Dict]:
        """Récupère la distribution des scores de performance."""
        try:
            employees = Employee.query.filter_by(status='active').all()
            scores = [emp.performance_score for emp in employees if emp.performance_score]
            
            if not scores:
                return []
            
            # Création des buckets de performance
            buckets = [
                {'range': '0-5', 'count': len([s for s in scores if 0 <= s < 5])},
                {'range': '5-6', 'count': len([s for s in scores if 5 <= s < 6])},
                {'range': '6-7', 'count': len([s for s in scores if 6 <= s < 7])},
                {'range': '7-8', 'count': len([s for s in scores if 7 <= s < 8])},
                {'range': '8-9', 'count': len([s for s in scores if 8 <= s < 9])},
                {'range': '9-10', 'count': len([s for s in scores if 9 <= s <= 10])}
            ]
            
            return buckets
        
        except Exception as e:
            logger.error(f"Erreur dans _get_performance_distribution: {str(e)}")
            return []

    def _calculate_employee_risk(self, employee: Employee, evaluations: List[PerformanceEvaluation]) -> Dict:
        """Calcule le risque de turnover pour un employé."""
        try:
            risk_score = 5.0  # Score de base
            risk_factors = []
            
            # Facteur: Performance en baisse
            if len(evaluations) >= 2:
                recent_score = evaluations[0].overall_score
                previous_score = evaluations[1].overall_score
                if recent_score < previous_score:
                    risk_score += 1.5
                    risk_factors.append("Performance en baisse")
            
            # Facteur: Score de performance faible
            if employee.performance_score < 7.0:
                risk_score += 2.0
                risk_factors.append("Performance faible")
            
            # Facteur: Ancienneté
            years_in_company = (datetime.now().date() - employee.hire_date).days / 365
            if 2 <= years_in_company <= 5:  # Période critique
                risk_score += 1.0
                risk_factors.append("Période critique d'ancienneté")
            
            # Facteur: Pas d'évaluation récente
            if not evaluations or (datetime.now().date() - evaluations[0].evaluation_date).days > 180:
                risk_score += 1.0
                risk_factors.append("Pas d'évaluation récente")
            
            # Détermination du niveau de risque
            if risk_score >= 8.0:
                risk_level = "Élevé"
            elif risk_score >= 6.0:
                risk_level = "Moyen"
            else:
                risk_level = "Faible"
            
            # Recommandations basées sur les facteurs de risque
            recommendations = []
            if "Performance en baisse" in risk_factors:
                recommendations.append("Entretien individuel pour identifier les causes")
            if "Performance faible" in risk_factors:
                recommendations.append("Plan d'amélioration des performances")
            if "Pas d'évaluation récente" in risk_factors:
                recommendations.append("Programmer une évaluation de performance")
            
            return {
                'risk_score': round(risk_score, 1),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': recommendations
            }
        
        except Exception as e:
            logger.error(f"Erreur dans _calculate_employee_risk: {str(e)}")
            return {
                'risk_score': 5.0,
                'risk_level': 'Moyen',
                'risk_factors': [],
                'recommendations': []
            }

