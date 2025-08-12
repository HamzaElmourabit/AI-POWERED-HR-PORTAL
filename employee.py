from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.String(20), default='active')  # active, inactive, terminated
    skills = db.Column(db.Text)  # JSON string of skills
    performance_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')
    evaluations = db.relationship('PerformanceEvaluation', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'department': self.department,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'salary': self.salary,
            'manager_id': self.manager_id,
            'status': self.status,
            'skills': self.skills,
            'performance_score': self.performance_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PerformanceEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evaluation_date = db.Column(db.Date, nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    overall_score = db.Column(db.Float, nullable=False)
    goals_achievement = db.Column(db.Float)
    technical_skills = db.Column(db.Float)
    soft_skills = db.Column(db.Float)
    comments = db.Column(db.Text)
    ai_insights = db.Column(db.Text)  # AI-generated insights
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    evaluator = db.relationship('Employee', foreign_keys=[evaluator_id])

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'evaluator_id': self.evaluator_id,
            'evaluation_date': self.evaluation_date.isoformat() if self.evaluation_date else None,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'overall_score': self.overall_score,
            'goals_achievement': self.goals_achievement,
            'technical_skills': self.technical_skills,
            'soft_skills': self.soft_skills,
            'comments': self.comments,
            'ai_insights': self.ai_insights,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

