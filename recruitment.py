from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.candidate import JobPosting, Candidate, Application
from src.services.ai_service import AIService
from datetime import datetime, date
import json
import os
from werkzeug.utils import secure_filename

recruitment_bp = Blueprint('recruitment', __name__)
ai_service = AIService()

UPLOAD_FOLDER = 'uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@recruitment_bp.route('/job-postings', methods=['GET'])
def get_job_postings():
    """Récupère la liste des offres d'emploi."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'active')
        department = request.args.get('department')
        
        query = JobPosting.query.filter_by(status=status)
        
        if department:
            query = query.filter_by(department=department)
        
        job_postings = query.order_by(JobPosting.posted_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'job_postings': [job.to_dict() for job in job_postings.items],
            'total': job_postings.total,
            'pages': job_postings.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/job-postings', methods=['POST'])
def create_job_posting():
    """Crée une nouvelle offre d'emploi avec optimisation IA."""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'department', 'description', 'requirements', 'posted_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Génération d'une description optimisée avec l'IA si demandé
        if data.get('use_ai_optimization', False):
            ai_description = ai_service.generate_job_description(
                data['title'],
                data['department'],
                data['requirements'] if isinstance(data['requirements'], list) else [data['requirements']]
            )
            data['description'] = ai_description.get('description', data['description'])
            data['ai_keywords'] = json.dumps(ai_description.get('keywords', []))
        
        job_posting = JobPosting(
            title=data['title'],
            department=data['department'],
            description=data['description'],
            requirements=data['requirements'] if isinstance(data['requirements'], str) else '\n'.join(data['requirements']),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            location=data.get('location'),
            employment_type=data.get('employment_type', 'full-time'),
            posted_date=datetime.strptime(data['posted_date'], '%Y-%m-%d').date(),
            closing_date=datetime.strptime(data['closing_date'], '%Y-%m-%d').date() if data.get('closing_date') else None,
            created_by=data.get('created_by'),
            ai_keywords=data.get('ai_keywords'),
            status=data.get('status', 'active')
        )
        
        db.session.add(job_posting)
        db.session.commit()
        
        return jsonify(job_posting.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/job-postings/<int:job_id>', methods=['GET'])
def get_job_posting(job_id):
    """Récupère les détails d'une offre d'emploi."""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        
        result = job_posting.to_dict()
        
        # Ajout des candidatures si demandé
        if request.args.get('include_applications') == 'true':
            applications = Application.query.filter_by(job_posting_id=job_id).all()
            result['applications'] = [app.to_dict() for app in applications]
            result['application_count'] = len(applications)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/candidates', methods=['GET'])
def get_candidates():
    """Récupère la liste des candidats."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        min_score = request.args.get('min_score', type=float)
        
        query = Candidate.query
        
        if min_score:
            query = query.filter(Candidate.ai_score >= min_score)
        
        candidates = query.order_by(Candidate.ai_score.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'candidates': [candidate.to_dict() for candidate in candidates.items],
            'total': candidates.total,
            'pages': candidates.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/candidates', methods=['POST'])
def create_candidate():
    """Crée un nouveau candidat avec analyse IA du CV."""
    try:
        data = request.get_json()
        
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Vérification de l'unicité de l'email
        if Candidate.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email déjà utilisé'}), 400
        
        candidate = Candidate(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            linkedin_url=data.get('linkedin_url'),
            cover_letter=data.get('cover_letter'),
            experience_years=data.get('experience_years', 0)
        )
        
        # Analyse IA du CV si fourni
        if data.get('resume_text'):
            ai_analysis = ai_service.analyze_resume(data['resume_text'])
            candidate.skills = json.dumps(ai_analysis.get('skills', []))
            candidate.ai_score = ai_analysis.get('score', 0)
            candidate.ai_summary = ai_analysis.get('summary', '')
            candidate.experience_years = ai_analysis.get('experience_years', candidate.experience_years)
            
            if ai_analysis.get('education'):
                candidate.education = json.dumps(ai_analysis.get('education'))
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify(candidate.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/candidates/<int:candidate_id>/analyze', methods=['POST'])
def analyze_candidate_for_job(candidate_id):
    """Analyse l'adéquation d'un candidat pour un poste spécifique."""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        data = request.get_json()
        
        if 'job_posting_id' not in data:
            return jsonify({'error': 'ID de poste requis'}), 400
        
        job_posting = JobPosting.query.get_or_404(data['job_posting_id'])
        
        # Analyse IA de l'adéquation candidat-poste
        job_description = f"{job_posting.title}\n{job_posting.description}\n{job_posting.requirements}"
        resume_text = f"Compétences: {candidate.skills}\nExpérience: {candidate.experience_years} ans\nRésumé: {candidate.ai_summary}"
        
        ai_analysis = ai_service.analyze_resume(resume_text, job_description)
        
        return jsonify({
            'candidate_id': candidate_id,
            'job_posting_id': data['job_posting_id'],
            'match_score': ai_analysis.get('job_match_score', 0),
            'analysis': ai_analysis,
            'recommendation': 'Recommandé' if ai_analysis.get('job_match_score', 0) >= 70 else 'À examiner'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/applications', methods=['POST'])
def create_application():
    """Crée une nouvelle candidature avec analyse IA automatique."""
    try:
        data = request.get_json()
        
        required_fields = ['candidate_id', 'job_posting_id', 'application_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        candidate = Candidate.query.get_or_404(data['candidate_id'])
        job_posting = JobPosting.query.get_or_404(data['job_posting_id'])
        
        # Vérification si candidature déjà existante
        existing_app = Application.query.filter_by(
            candidate_id=data['candidate_id'],
            job_posting_id=data['job_posting_id']
        ).first()
        
        if existing_app:
            return jsonify({'error': 'Candidature déjà existante pour ce poste'}), 400
        
        application = Application(
            candidate_id=data['candidate_id'],
            job_posting_id=data['job_posting_id'],
            application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date(),
            status=data.get('status', 'submitted')
        )
        
        # Analyse IA automatique de l'adéquation
        job_description = f"{job_posting.title}\n{job_posting.description}\n{job_posting.requirements}"
        resume_text = f"Compétences: {candidate.skills}\nExpérience: {candidate.experience_years} ans\nRésumé: {candidate.ai_summary}"
        
        ai_analysis = ai_service.analyze_resume(resume_text, job_description)
        application.ai_match_score = ai_analysis.get('job_match_score', 0)
        application.ai_analysis = json.dumps(ai_analysis)
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify(application.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/applications/<int:application_id>/interview-questions', methods=['GET'])
def generate_interview_questions(application_id):
    """Génère des questions d'entretien personnalisées pour une candidature."""
    try:
        application = Application.query.get_or_404(application_id)
        candidate = Candidate.query.get(application.candidate_id)
        job_posting = JobPosting.query.get(application.job_posting_id)
        
        candidate_profile = {
            'name': f"{candidate.first_name} {candidate.last_name}",
            'skills': json.loads(candidate.skills) if candidate.skills else [],
            'experience_years': candidate.experience_years,
            'summary': candidate.ai_summary
        }
        
        questions = ai_service.generate_interview_questions(
            job_posting.title,
            candidate_profile
        )
        
        return jsonify({
            'application_id': application_id,
            'questions': questions,
            'candidate_name': f"{candidate.first_name} {candidate.last_name}",
            'job_title': job_posting.title
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Met à jour le statut d'une candidature."""
    try:
        application = Application.query.get_or_404(application_id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Statut requis'}), 400
        
        application.status = data['status']
        
        if 'recruiter_notes' in data:
            application.recruiter_notes = data['recruiter_notes']
        
        if 'interview_feedback' in data:
            application.interview_feedback = data['interview_feedback']
        
        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(application.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recruitment_bp.route('/recruitment/analytics', methods=['GET'])
def get_recruitment_analytics():
    """Récupère les analytics de recrutement."""
    try:
        # Statistiques générales
        total_jobs = JobPosting.query.filter_by(status='active').count()
        total_candidates = Candidate.query.count()
        total_applications = Application.query.count()
        
        # Applications par statut
        app_status_stats = db.session.query(
            Application.status,
            db.func.count(Application.id)
        ).group_by(Application.status).all()
        
        # Score moyen des candidats
        avg_candidate_score = db.session.query(
            db.func.avg(Candidate.ai_score)
        ).scalar() or 0
        
        # Top départements qui recrutent
        dept_hiring_stats = db.session.query(
            JobPosting.department,
            db.func.count(JobPosting.id)
        ).filter_by(status='active').group_by(JobPosting.department).all()
        
        return jsonify({
            'total_active_jobs': total_jobs,
            'total_candidates': total_candidates,
            'total_applications': total_applications,
            'avg_candidate_score': round(float(avg_candidate_score), 2),
            'applications_by_status': [
                {'status': status, 'count': count} 
                for status, count in app_status_stats
            ],
            'hiring_by_department': [
                {'department': dept, 'active_jobs': count} 
                for dept, count in dept_hiring_stats
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

