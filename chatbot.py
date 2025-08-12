from flask import Blueprint, request, jsonify
from src.services.ai_service import AIService
from src.models.user import db
from src.models.employee import Employee
from src.models.candidate import JobPosting
import json

chatbot_bp = Blueprint('chatbot', __name__)
ai_service = AIService()

@chatbot_bp.route('/chatbot/message', methods=['POST'])
def handle_chatbot_message():
    """Traite un message du chatbot RH."""
    try:
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'Message requis'}), 400
        
        user_message = data['message']
        user_context = data.get('context', {})
        
        # Enrichissement du contexte avec des données RH si pertinent
        enhanced_context = enhance_context_with_hr_data(user_message, user_context)
        
        # Génération de la réponse IA
        response = ai_service.chatbot_response(user_message, enhanced_context)
        
        # Détection d'intentions spécifiques pour des actions automatiques
        intent = detect_intent(user_message)
        suggestions = generate_suggestions(intent, enhanced_context)
        
        return jsonify({
            'response': response,
            'intent': intent,
            'suggestions': suggestions,
            'context': enhanced_context
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def enhance_context_with_hr_data(message, context):
    """Enrichit le contexte avec des données RH pertinentes."""
    enhanced_context = context.copy()
    
    try:
        message_lower = message.lower()
        
        # Si la question concerne les employés
        if any(keyword in message_lower for keyword in ['employé', 'employee', 'équipe', 'team', 'collègue']):
            total_employees = Employee.query.filter_by(status='active').count()
            departments = db.session.query(Employee.department).distinct().all()
            enhanced_context['total_employees'] = total_employees
            enhanced_context['departments'] = [dept[0] for dept in departments if dept[0]]
        
        # Si la question concerne le recrutement
        if any(keyword in message_lower for keyword in ['recrutement', 'recruitment', 'poste', 'job', 'candidat']):
            active_jobs = JobPosting.query.filter_by(status='active').count()
            job_departments = db.session.query(JobPosting.department).distinct().all()
            enhanced_context['active_job_postings'] = active_jobs
            enhanced_context['hiring_departments'] = [dept[0] for dept in job_departments if dept[0]]
        
        # Si la question concerne les congés ou politiques RH
        if any(keyword in message_lower for keyword in ['congé', 'vacation', 'politique', 'policy', 'règlement']):
            enhanced_context['hr_policies'] = {
                'annual_leave': '25 jours par an',
                'sick_leave': '10 jours par an',
                'maternity_leave': '16 semaines',
                'remote_work': 'Jusqu\'à 2 jours par semaine'
            }
        
    except Exception as e:
        print(f"Erreur lors de l'enrichissement du contexte: {e}")
    
    return enhanced_context

def detect_intent(message):
    """Détecte l'intention de l'utilisateur."""
    message_lower = message.lower()
    
    # Intentions de recherche d'informations
    if any(keyword in message_lower for keyword in ['qui est', 'who is', 'contact', 'téléphone', 'email']):
        return 'search_employee'
    
    if any(keyword in message_lower for keyword in ['combien', 'how many', 'nombre', 'statistique']):
        return 'get_statistics'
    
    if any(keyword in message_lower for keyword in ['poste', 'job', 'recrutement', 'candidature']):
        return 'job_inquiry'
    
    if any(keyword in message_lower for keyword in ['congé', 'vacation', 'absence', 'leave']):
        return 'leave_inquiry'
    
    if any(keyword in message_lower for keyword in ['politique', 'policy', 'règlement', 'procedure']):
        return 'policy_inquiry'
    
    if any(keyword in message_lower for keyword in ['formation', 'training', 'développement', 'development']):
        return 'training_inquiry'
    
    if any(keyword in message_lower for keyword in ['salaire', 'salary', 'paie', 'payroll']):
        return 'payroll_inquiry'
    
    return 'general_inquiry'

def generate_suggestions(intent, context):
    """Génère des suggestions basées sur l'intention détectée."""
    suggestions = []
    
    if intent == 'search_employee':
        suggestions = [
            "Rechercher un employé par nom",
            "Voir l'organigramme",
            "Contacter le service RH"
        ]
    
    elif intent == 'get_statistics':
        suggestions = [
            "Voir les statistiques des employés",
            "Consulter les métriques de recrutement",
            "Analyser les performances par département"
        ]
    
    elif intent == 'job_inquiry':
        suggestions = [
            "Voir les postes ouverts",
            "Postuler à un emploi",
            "Contacter un recruteur"
        ]
    
    elif intent == 'leave_inquiry':
        suggestions = [
            "Demander un congé",
            "Vérifier mon solde de congés",
            "Voir le calendrier des congés"
        ]
    
    elif intent == 'policy_inquiry':
        suggestions = [
            "Consulter le manuel employé",
            "Voir les politiques RH",
            "Contacter le service juridique"
        ]
    
    elif intent == 'training_inquiry':
        suggestions = [
            "Voir les formations disponibles",
            "S'inscrire à une formation",
            "Consulter mon plan de développement"
        ]
    
    elif intent == 'payroll_inquiry':
        suggestions = [
            "Voir mes fiches de paie",
            "Mettre à jour mes informations bancaires",
            "Contacter la comptabilité"
        ]
    
    else:
        suggestions = [
            "Poser une question sur les RH",
            "Chercher un employé",
            "Voir les postes disponibles",
            "Consulter les politiques"
        ]
    
    return suggestions

@chatbot_bp.route('/chatbot/quick-actions', methods=['GET'])
def get_quick_actions():
    """Retourne les actions rapides disponibles."""
    try:
        quick_actions = [
            {
                'id': 'search_employee',
                'title': 'Rechercher un employé',
                'description': 'Trouver les coordonnées d\'un collègue',
                'icon': 'person_search'
            },
            {
                'id': 'job_postings',
                'title': 'Postes ouverts',
                'description': 'Voir les opportunités de carrière',
                'icon': 'work'
            },
            {
                'id': 'leave_request',
                'title': 'Demande de congé',
                'description': 'Soumettre une demande d\'absence',
                'icon': 'event_available'
            },
            {
                'id': 'hr_policies',
                'title': 'Politiques RH',
                'description': 'Consulter les règlements internes',
                'icon': 'policy'
            },
            {
                'id': 'training',
                'title': 'Formations',
                'description': 'Découvrir les opportunités de formation',
                'icon': 'school'
            },
            {
                'id': 'org_chart',
                'title': 'Organigramme',
                'description': 'Visualiser la structure organisationnelle',
                'icon': 'account_tree'
            }
        ]
        
        return jsonify({'quick_actions': quick_actions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/chatbot/faq', methods=['GET'])
def get_faq():
    """Retourne les questions fréquemment posées."""
    try:
        faq = [
            {
                'question': 'Comment demander un congé?',
                'answer': 'Vous pouvez soumettre une demande de congé via le portail RH ou en contactant votre manager directement.',
                'category': 'congés'
            },
            {
                'question': 'Où trouver mes fiches de paie?',
                'answer': 'Vos fiches de paie sont disponibles dans votre espace personnel du portail RH, section "Paie".',
                'category': 'paie'
            },
            {
                'question': 'Comment mettre à jour mes informations personnelles?',
                'answer': 'Rendez-vous dans votre profil employé pour modifier vos informations de contact et bancaires.',
                'category': 'profil'
            },
            {
                'question': 'Quelles formations sont disponibles?',
                'answer': 'Consultez le catalogue de formations dans la section "Développement" du portail RH.',
                'category': 'formation'
            },
            {
                'question': 'Comment contacter le service RH?',
                'answer': 'Vous pouvez nous contacter par email à rh@entreprise.com ou par téléphone au 01 23 45 67 89.',
                'category': 'contact'
            }
        ]
        
        return jsonify({'faq': faq})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/chatbot/feedback', methods=['POST'])
def submit_feedback():
    """Permet de soumettre un feedback sur le chatbot."""
    try:
        data = request.get_json()
        
        required_fields = ['message_id', 'rating', 'feedback']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Ici, vous pourriez sauvegarder le feedback en base de données
        # pour améliorer le chatbot
        
        return jsonify({
            'message': 'Merci pour votre feedback!',
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

