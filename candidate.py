from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    location = db.Column(db.String(100))
    employment_type = db.Column(db.String(50))  # full-time, part-time, contract
    status = db.Column(db.String(20), default='active')  # active, closed, draft
    posted_date = db.Column(db.Date, nullable=False)
    closing_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('employee.id'))
    ai_keywords = db.Column(db.Text)  # AI-extracted keywords for matching
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='job_posting', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'department': self.department,
            'description': self.description,
            'requirements': self.requirements,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'location': self.location,
            'employment_type': self.employment_type,
            'status': self.status,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'created_by': self.created_by,
            'ai_keywords': self.ai_keywords,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    linkedin_url = db.Column(db.String(200))
    resume_path = db.Column(db.String(500))
    cover_letter = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of skills
    experience_years = db.Column(db.Integer)
    education = db.Column(db.Text)  # JSON string of education
    ai_score = db.Column(db.Float, default=0.0)  # AI-calculated overall score
    ai_summary = db.Column(db.Text)  # AI-generated candidate summary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='candidate', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'linkedin_url': self.linkedin_url,
            'resume_path': self.resume_path,
            'cover_letter': self.cover_letter,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'education': self.education,
            'ai_score': self.ai_score,
            'ai_summary': self.ai_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='submitted')  # submitted, screening, interview, rejected, hired
    ai_match_score = db.Column(db.Float, default=0.0)  # AI-calculated job match score
    ai_analysis = db.Column(db.Text)  # AI analysis of candidate-job fit
    recruiter_notes = db.Column(db.Text)
    interview_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_posting_id': self.job_posting_id,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status,
            'ai_match_score': self.ai_match_score,
            'ai_analysis': self.ai_analysis,
            'recruiter_notes': self.recruiter_notes,
            'interview_feedback': self.interview_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

