from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.employee import Employee, PerformanceEvaluation
from src.services.ai_service import AIService
from datetime import datetime, date
import json

employees_bp = Blueprint('employees', __name__)
ai_service = AIService()

@employees_bp.route('/employees', methods=['GET'])
def get_employees():
    """Récupère la liste des employés avec filtres optionnels."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        department = request.args.get('department')
        status = request.args.get('status', 'active')
        
        query = Employee.query.filter_by(status=status)
        
        if department:
            query = query.filter_by(department=department)
        
        employees = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'employees': [emp.to_dict() for emp in employees.items],
            'total': employees.total,
            'pages': employees.pages,
            'current_page': page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees', methods=['POST'])
def create_employee():
    """Crée un nouvel employé."""
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['employee_id', 'first_name', 'last_name', 'email', 'position', 'department', 'hire_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Vérification de l'unicité
        if Employee.query.filter_by(employee_id=data['employee_id']).first():
            return jsonify({'error': 'ID employé déjà existant'}), 400
        
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email déjà utilisé'}), 400
        
        # Conversion de la date
        hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        
        employee = Employee(
            employee_id=data['employee_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            position=data['position'],
            department=data['department'],
            hire_date=hire_date,
            salary=data.get('salary'),
            manager_id=data.get('manager_id'),
            skills=json.dumps(data.get('skills', [])),
            status=data.get('status', 'active')
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify(employee.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Récupère les détails d'un employé."""
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        # Récupération des évaluations
        evaluations = PerformanceEvaluation.query.filter_by(employee_id=employee_id).order_by(
            PerformanceEvaluation.evaluation_date.desc()
        ).limit(5).all()
        
        result = employee.to_dict()
        result['evaluations'] = [eval.to_dict() for eval in evaluations]
        
        # Ajout des insights IA si demandé
        if request.args.get('include_ai_insights') == 'true':
            ai_insights = ai_service.analyze_performance_data(
                employee.to_dict(),
                [eval.to_dict() for eval in evaluations]
            )
            result['ai_insights'] = ai_insights
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Met à jour un employé."""
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        # Mise à jour des champs
        for field in ['first_name', 'last_name', 'email', 'phone', 'position', 
                     'department', 'salary', 'manager_id', 'status']:
            if field in data:
                setattr(employee, field, data[field])
        
        if 'skills' in data:
            employee.skills = json.dumps(data['skills'])
        
        if 'hire_date' in data:
            employee.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(employee.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees/<int:employee_id>/performance', methods=['POST'])
def create_performance_evaluation(employee_id):
    """Crée une nouvelle évaluation de performance."""
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json()
        
        required_fields = ['evaluator_id', 'evaluation_date', 'period_start', 'period_end', 'overall_score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        evaluation = PerformanceEvaluation(
            employee_id=employee_id,
            evaluator_id=data['evaluator_id'],
            evaluation_date=datetime.strptime(data['evaluation_date'], '%Y-%m-%d').date(),
            period_start=datetime.strptime(data['period_start'], '%Y-%m-%d').date(),
            period_end=datetime.strptime(data['period_end'], '%Y-%m-%d').date(),
            overall_score=data['overall_score'],
            goals_achievement=data.get('goals_achievement'),
            technical_skills=data.get('technical_skills'),
            soft_skills=data.get('soft_skills'),
            comments=data.get('comments')
        )
        
        # Génération d'insights IA
        employee_data = employee.to_dict()
        performance_history = [eval.to_dict() for eval in employee.evaluations]
        ai_insights = ai_service.analyze_performance_data(employee_data, performance_history)
        evaluation.ai_insights = json.dumps(ai_insights)
        
        # Mise à jour du score de performance de l'employé
        employee.performance_score = data['overall_score']
        
        db.session.add(evaluation)
        db.session.commit()
        
        return jsonify(evaluation.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees/<int:employee_id>/turnover-risk', methods=['GET'])
def get_turnover_risk(employee_id):
    """Analyse le risque de turnover d'un employé."""
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        # Récupération des données de l'équipe pour le contexte
        team_members = Employee.query.filter_by(
            department=employee.department,
            status='active'
        ).all()
        
        team_data = [member.to_dict() for member in team_members if member.id != employee_id]
        
        risk_analysis = ai_service.predict_turnover_risk(
            employee.to_dict(),
            team_data
        )
        
        return jsonify(risk_analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/departments', methods=['GET'])
def get_departments():
    """Récupère la liste des départements."""
    try:
        departments = db.session.query(Employee.department).distinct().all()
        return jsonify([dept[0] for dept in departments if dept[0]])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employees_bp.route('/employees/analytics', methods=['GET'])
def get_employee_analytics():
    """Récupère les analytics des employés."""
    try:
        total_employees = Employee.query.filter_by(status='active').count()
        
        # Répartition par département
        dept_stats = db.session.query(
            Employee.department,
            db.func.count(Employee.id)
        ).filter_by(status='active').group_by(Employee.department).all()
        
        # Performance moyenne par département
        perf_stats = db.session.query(
            Employee.department,
            db.func.avg(Employee.performance_score)
        ).filter_by(status='active').group_by(Employee.department).all()
        
        return jsonify({
            'total_employees': total_employees,
            'department_distribution': [
                {'department': dept, 'count': count} 
                for dept, count in dept_stats
            ],
            'performance_by_department': [
                {'department': dept, 'avg_score': round(float(avg_score or 0), 2)} 
                for dept, avg_score in perf_stats
            ]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

