from flask import Blueprint, request, jsonify
from src.services.analytics_service import AnalyticsService
import logging

analytics_bp = Blueprint('analytics', __name__)
analytics_service = AnalyticsService()

@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Récupère les analytics pour le tableau de bord."""
    try:
        # Récupération de toutes les analytics
        employee_analytics = analytics_service.get_employee_analytics()
        recruitment_analytics = analytics_service.get_recruitment_analytics()
        performance_analytics = analytics_service.get_performance_analytics()
        turnover_risks = analytics_service.predict_turnover_risks()
        
        # Compilation des données
        dashboard_data = {
            'employees': employee_analytics,
            'recruitment': recruitment_analytics,
            'performance': performance_analytics,
            'turnover_risks': turnover_risks,
            'summary': {
                'total_employees': employee_analytics.get('total_employees', 0),
                'active_jobs': recruitment_analytics.get('total_active_jobs', 0),
                'avg_performance': performance_analytics.get('avg_performance', 0),
                'high_risk_employees': turnover_risks.get('high_risk_employees', 0)
            }
        }
        
        return jsonify(dashboard_data)
    
    except Exception as e:
        logging.error(f"Erreur dans get_dashboard_analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/employees', methods=['GET'])
def get_employee_analytics():
    """Récupère les analytics détaillées des employés."""
    try:
        analytics = analytics_service.get_employee_analytics()
        return jsonify(analytics)
    
    except Exception as e:
        logging.error(f"Erreur dans get_employee_analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/recruitment', methods=['GET'])
def get_recruitment_analytics():
    """Récupère les analytics de recrutement."""
    try:
        analytics = analytics_service.get_recruitment_analytics()
        return jsonify(analytics)
    
    except Exception as e:
        logging.error(f"Erreur dans get_recruitment_analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Récupère les analytics de performance."""
    try:
        analytics = analytics_service.get_performance_analytics()
        return jsonify(analytics)
    
    except Exception as e:
        logging.error(f"Erreur dans get_performance_analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/turnover-risks', methods=['GET'])
def get_turnover_risks():
    """Récupère les prédictions de risque de turnover."""
    try:
        risks = analytics_service.predict_turnover_risks()
        return jsonify(risks)
    
    except Exception as e:
        logging.error(f"Erreur dans get_turnover_risks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/insights', methods=['POST'])
def generate_ai_insights():
    """Génère des insights IA basés sur les données fournies."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données requises'}), 400
        
        insights = analytics_service.generate_ai_insights(data)
        return jsonify(insights)
    
    except Exception as e:
        logging.error(f"Erreur dans generate_ai_insights: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/reports/monthly', methods=['GET'])
def get_monthly_report():
    """Génère un rapport mensuel complet."""
    try:
        # Récupération de toutes les données
        employee_analytics = analytics_service.get_employee_analytics()
        recruitment_analytics = analytics_service.get_recruitment_analytics()
        performance_analytics = analytics_service.get_performance_analytics()
        turnover_risks = analytics_service.predict_turnover_risks()
        
        # Compilation du rapport
        report_data = {
            'employees': employee_analytics,
            'recruitment': recruitment_analytics,
            'performance': performance_analytics,
            'turnover_risks': turnover_risks
        }
        
        # Génération d'insights IA pour le rapport
        ai_insights = analytics_service.generate_ai_insights(report_data)
        
        monthly_report = {
            'report_date': request.args.get('date', '2024-02-01'),
            'data': report_data,
            'ai_insights': ai_insights,
            'executive_summary': {
                'total_employees': employee_analytics.get('total_employees', 0),
                'new_hires': len(employee_analytics.get('hiring_trend', [])),
                'avg_performance': performance_analytics.get('avg_performance', 0),
                'recruitment_success_rate': recruitment_analytics.get('conversion_rates', {}).get('overall_success_rate', 0),
                'employees_at_risk': turnover_risks.get('total_at_risk', 0)
            }
        }
        
        return jsonify(monthly_report)
    
    except Exception as e:
        logging.error(f"Erreur dans get_monthly_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/predictions', methods=['GET'])
def get_predictions():
    """Récupère les prédictions IA pour les 3 prochains mois."""
    try:
        # Récupération des données historiques
        employee_analytics = analytics_service.get_employee_analytics()
        performance_analytics = analytics_service.get_performance_analytics()
        
        # Génération de prédictions avec l'IA
        prediction_data = {
            'historical_data': {
                'performance_trend': performance_analytics.get('performance_trend', []),
                'hiring_trend': employee_analytics.get('hiring_trend', [])
            }
        }
        
        # Simulation de prédictions (à remplacer par un modèle ML réel)
        predictions = {
            'next_3_months': {
                'performance_forecast': [
                    {'month': '2024-03', 'predicted_score': 8.4, 'confidence': 85},
                    {'month': '2024-04', 'predicted_score': 8.6, 'confidence': 80},
                    {'month': '2024-05', 'predicted_score': 8.5, 'confidence': 75}
                ],
                'turnover_forecast': [
                    {'month': '2024-03', 'predicted_turnover': 2.1, 'confidence': 78},
                    {'month': '2024-04', 'predicted_turnover': 1.9, 'confidence': 72},
                    {'month': '2024-05', 'predicted_turnover': 2.3, 'confidence': 68}
                ],
                'hiring_needs': [
                    {'department': 'IT', 'predicted_needs': 3, 'reason': 'Croissance prévue'},
                    {'department': 'Marketing', 'predicted_needs': 2, 'reason': 'Remplacement turnover'},
                    {'department': 'Ventes', 'predicted_needs': 4, 'reason': 'Expansion commerciale'}
                ]
            },
            'recommendations': [
                'Anticiper le recrutement en IT pour soutenir la croissance',
                'Mettre en place des actions de rétention en Marketing',
                'Préparer un plan de formation pour améliorer les performances'
            ]
        }
        
        return jsonify(predictions)
    
    except Exception as e:
        logging.error(f"Erreur dans get_predictions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/benchmarks', methods=['GET'])
def get_benchmarks():
    """Récupère les benchmarks sectoriels."""
    try:
        # Simulation de benchmarks sectoriels
        benchmarks = {
            'industry_averages': {
                'turnover_rate': 15.2,
                'performance_score': 7.8,
                'recruitment_success_rate': 18.5,
                'time_to_hire_days': 32
            },
            'company_performance': {
                'turnover_rate': 12.8,
                'performance_score': 8.3,
                'recruitment_success_rate': 23.6,
                'time_to_hire_days': 28
            },
            'comparison': {
                'turnover_rate': 'better',  # 16% mieux que la moyenne
                'performance_score': 'better',  # 6% mieux
                'recruitment_success_rate': 'better',  # 28% mieux
                'time_to_hire_days': 'better'  # 13% plus rapide
            },
            'recommendations': [
                'Maintenir les bonnes pratiques de rétention',
                'Capitaliser sur l\'efficacité du processus de recrutement',
                'Continuer à investir dans le développement des performances'
            ]
        }
        
        return jsonify(benchmarks)
    
    except Exception as e:
        logging.error(f"Erreur dans get_benchmarks: {str(e)}")
        return jsonify({'error': str(e)}), 500

