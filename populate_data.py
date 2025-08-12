#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des données de test
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from random import randint, choice, uniform

# Ajout du chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.user import db
from src.models.employee import Employee, PerformanceEvaluation
from src.models.candidate import JobPosting, Candidate, Application
from src.services.ai_service import AIService

def create_sample_employees():
    """Crée des employés de test"""
    employees_data = [
        {
            'employee_id': 'EMP001',
            'first_name': 'Marie',
            'last_name': 'Dubois',
            'email': 'marie.dubois@entreprise.com',
            'phone': '+33 1 23 45 67 89',
            'position': 'Développeuse Senior',
            'department': 'IT',
            'hire_date': date(2022, 3, 15),
            'salary': 65000,
            'skills': json.dumps(['Python', 'React', 'AWS', 'Docker', 'PostgreSQL']),
            'performance_score': 8.5
        },
        {
            'employee_id': 'EMP002',
            'first_name': 'Pierre',
            'last_name': 'Martin',
            'email': 'pierre.martin@entreprise.com',
            'phone': '+33 1 23 45 67 90',
            'position': 'Chef de Projet',
            'department': 'IT',
            'hire_date': date(2021, 9, 1),
            'salary': 70000,
            'skills': json.dumps(['Management', 'Agile', 'Scrum', 'JIRA', 'Leadership']),
            'performance_score': 9.2
        },
        {
            'employee_id': 'EMP003',
            'first_name': 'Sophie',
            'last_name': 'Bernard',
            'email': 'sophie.bernard@entreprise.com',
            'phone': '+33 1 23 45 67 91',
            'position': 'Responsable Marketing',
            'department': 'Marketing',
            'hire_date': date(2020, 11, 20),
            'salary': 58000,
            'skills': json.dumps(['Marketing Digital', 'SEO', 'Google Ads', 'Analytics', 'Content Marketing']),
            'performance_score': 8.8
        },
        {
            'employee_id': 'EMP004',
            'first_name': 'Thomas',
            'last_name': 'Leroy',
            'email': 'thomas.leroy@entreprise.com',
            'phone': '+33 1 23 45 67 92',
            'position': 'Analyste Financier',
            'department': 'Finance',
            'hire_date': date(2023, 1, 10),
            'salary': 45000,
            'skills': json.dumps(['Excel', 'Power BI', 'SQL', 'Finance', 'Comptabilité']),
            'performance_score': 7.5
        },
        {
            'employee_id': 'EMP005',
            'first_name': 'Julie',
            'last_name': 'Moreau',
            'email': 'julie.moreau@entreprise.com',
            'phone': '+33 1 23 45 67 93',
            'position': 'Consultante RH',
            'department': 'RH',
            'hire_date': date(2022, 7, 5),
            'salary': 52000,
            'skills': json.dumps(['Recrutement', 'Formation', 'Gestion des talents', 'SIRH', 'Droit du travail']),
            'performance_score': 8.1
        },
        {
            'employee_id': 'EMP006',
            'first_name': 'Antoine',
            'last_name': 'Rousseau',
            'email': 'antoine.rousseau@entreprise.com',
            'phone': '+33 1 23 45 67 94',
            'position': 'Commercial Senior',
            'department': 'Ventes',
            'hire_date': date(2021, 4, 12),
            'salary': 55000,
            'skills': json.dumps(['Vente', 'Négociation', 'CRM', 'Prospection', 'Relation client']),
            'performance_score': 7.8
        }
    ]

    employees = []
    for emp_data in employees_data:
        employee = Employee(**emp_data)
        db.session.add(employee)
        employees.append(employee)
    
    db.session.commit()
    return employees

def create_sample_job_postings():
    """Crée des offres d'emploi de test"""
    jobs_data = [
        {
            'title': 'Développeur Full Stack Senior',
            'department': 'IT',
            'description': 'Nous recherchons un développeur full stack expérimenté pour rejoindre notre équipe technique dynamique.',
            'requirements': 'Minimum 5 ans d\'expérience en développement web, maîtrise de React, Node.js, et bases de données relationnelles.',
            'salary_min': 55000,
            'salary_max': 75000,
            'location': 'Paris',
            'employment_type': 'CDI',
            'posted_date': date.today() - timedelta(days=15),
            'status': 'active'
        },
        {
            'title': 'Chef de Projet Marketing Digital',
            'department': 'Marketing',
            'description': 'Poste de chef de projet pour piloter nos campagnes marketing digital et coordonner les équipes créatives.',
            'requirements': 'Expérience en gestion de projet marketing, maîtrise des outils digitaux, leadership et créativité.',
            'salary_min': 45000,
            'salary_max': 60000,
            'location': 'Lyon',
            'employment_type': 'CDI',
            'posted_date': date.today() - timedelta(days=10),
            'status': 'active'
        },
        {
            'title': 'Analyste Financier Junior',
            'department': 'Finance',
            'description': 'Opportunité pour un jeune diplômé de rejoindre notre équipe finance et de développer ses compétences analytiques.',
            'requirements': 'Diplôme en finance ou comptabilité, maîtrise d\'Excel, rigueur et esprit analytique.',
            'salary_min': 35000,
            'salary_max': 45000,
            'location': 'Remote',
            'employment_type': 'CDI',
            'posted_date': date.today() - timedelta(days=5),
            'status': 'active'
        }
    ]

    job_postings = []
    for job_data in jobs_data:
        job = JobPosting(**job_data)
        db.session.add(job)
        job_postings.append(job)
    
    db.session.commit()
    return job_postings

def create_sample_candidates():
    """Crée des candidats de test"""
    candidates_data = [
        {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice.johnson@email.com',
            'phone': '+33 6 12 34 56 78',
            'experience_years': 5,
            'skills': json.dumps(['React', 'Node.js', 'Python', 'AWS', 'MongoDB']),
            'ai_score': 8.7,
            'ai_summary': 'Développeuse expérimentée avec une solide expertise en technologies web modernes et cloud.'
        },
        {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob.smith@email.com',
            'phone': '+33 6 12 34 56 79',
            'experience_years': 3,
            'skills': json.dumps(['Marketing Digital', 'SEO', 'Google Ads', 'Analytics', 'Social Media']),
            'ai_score': 7.2,
            'ai_summary': 'Spécialiste marketing digital avec une bonne expérience des campagnes en ligne.'
        },
        {
            'first_name': 'Claire',
            'last_name': 'Wilson',
            'email': 'claire.wilson@email.com',
            'phone': '+33 6 12 34 56 80',
            'experience_years': 2,
            'skills': json.dumps(['Finance', 'Excel', 'Power BI', 'SQL', 'Analyse de données']),
            'ai_score': 9.1,
            'ai_summary': 'Jeune analyste financière très prometteuse avec d\'excellentes compétences analytiques.'
        },
        {
            'first_name': 'David',
            'last_name': 'Brown',
            'email': 'david.brown@email.com',
            'phone': '+33 6 12 34 56 81',
            'experience_years': 7,
            'skills': json.dumps(['Java', 'Spring', 'Microservices', 'Kubernetes', 'DevOps']),
            'ai_score': 8.9,
            'ai_summary': 'Architecte logiciel senior avec une expertise approfondie en systèmes distribués.'
        },
        {
            'first_name': 'Emma',
            'last_name': 'Davis',
            'email': 'emma.davis@email.com',
            'phone': '+33 6 12 34 56 82',
            'experience_years': 4,
            'skills': json.dumps(['UX/UI Design', 'Figma', 'Adobe Creative Suite', 'Prototyping', 'User Research']),
            'ai_score': 8.3,
            'ai_summary': 'Designer UX/UI créative avec une approche centrée utilisateur et de solides compétences techniques.'
        }
    ]

    candidates = []
    for cand_data in candidates_data:
        candidate = Candidate(**cand_data)
        db.session.add(candidate)
        candidates.append(candidate)
    
    db.session.commit()
    return candidates

def create_sample_applications(candidates, job_postings):
    """Crée des candidatures de test"""
    applications_data = [
        {
            'candidate_id': candidates[0].id,  # Alice -> Développeur Full Stack
            'job_posting_id': job_postings[0].id,
            'application_date': date.today() - timedelta(days=3),
            'status': 'interview',
            'ai_match_score': 8.5,
            'ai_analysis': json.dumps({
                'strengths': ['Excellente maîtrise technique', 'Expérience pertinente'],
                'concerns': ['Pas d\'expérience en leadership'],
                'recommendation': 'Candidat très prometteur pour le poste'
            })
        },
        {
            'candidate_id': candidates[1].id,  # Bob -> Chef de Projet Marketing
            'job_posting_id': job_postings[1].id,
            'application_date': date.today() - timedelta(days=2),
            'status': 'screening',
            'ai_match_score': 7.8,
            'ai_analysis': json.dumps({
                'strengths': ['Bonne expérience marketing', 'Compétences digitales'],
                'concerns': ['Manque d\'expérience en gestion d\'équipe'],
                'recommendation': 'Candidat intéressant à approfondir'
            })
        },
        {
            'candidate_id': candidates[2].id,  # Claire -> Analyste Financier
            'job_posting_id': job_postings[2].id,
            'application_date': date.today() - timedelta(days=1),
            'status': 'submitted',
            'ai_match_score': 9.2,
            'ai_analysis': json.dumps({
                'strengths': ['Excellentes compétences analytiques', 'Profil junior parfait'],
                'concerns': ['Peu d\'expérience professionnelle'],
                'recommendation': 'Candidat idéal pour le poste junior'
            })
        }
    ]

    applications = []
    for app_data in applications_data:
        application = Application(**app_data)
        db.session.add(application)
        applications.append(application)
    
    db.session.commit()
    return applications

def create_sample_evaluations(employees):
    """Crée des évaluations de performance de test"""
    evaluations = []
    
    for employee in employees[:3]:  # Évaluations pour les 3 premiers employés
        for i in range(2):  # 2 évaluations par employé
            evaluation_date = date.today() - timedelta(days=90 * (i + 1))
            evaluation = PerformanceEvaluation(
                employee_id=employee.id,
                evaluator_id=employees[1].id,  # Pierre Martin comme évaluateur
                evaluation_date=evaluation_date,
                period_start=evaluation_date - timedelta(days=90),
                period_end=evaluation_date,
                overall_score=round(uniform(7.0, 9.5), 1),
                goals_achievement=round(uniform(7.0, 9.0), 1),
                technical_skills=round(uniform(7.5, 9.5), 1),
                soft_skills=round(uniform(7.0, 9.0), 1),
                comments=f'Évaluation de performance pour la période {evaluation_date - timedelta(days=90)} - {evaluation_date}',
                ai_insights=json.dumps({
                    'performance_trend': choice(['amélioration', 'stable', 'déclin']),
                    'strengths': ['Compétences techniques solides', 'Bon esprit d\'équipe'],
                    'development_areas': ['Communication', 'Leadership'],
                    'recommendations': ['Formation en management', 'Mentorat']
                })
            )
            db.session.add(evaluation)
            evaluations.append(evaluation)
    
    db.session.commit()
    return evaluations

def main():
    """Fonction principale pour peupler la base de données"""
    print("🚀 Début du peuplement de la base de données...")
    
    try:
        # Suppression des données existantes
        print("🗑️  Suppression des données existantes...")
        db.session.query(Application).delete()
        db.session.query(PerformanceEvaluation).delete()
        db.session.query(Candidate).delete()
        db.session.query(JobPosting).delete()
        db.session.query(Employee).delete()
        db.session.commit()
        
        # Création des données de test
        print("👥 Création des employés...")
        employees = create_sample_employees()
        print(f"   ✅ {len(employees)} employés créés")
        
        print("💼 Création des offres d'emploi...")
        job_postings = create_sample_job_postings()
        print(f"   ✅ {len(job_postings)} offres créées")
        
        print("🎯 Création des candidats...")
        candidates = create_sample_candidates()
        print(f"   ✅ {len(candidates)} candidats créés")
        
        print("📝 Création des candidatures...")
        applications = create_sample_applications(candidates, job_postings)
        print(f"   ✅ {len(applications)} candidatures créées")
        
        print("📊 Création des évaluations de performance...")
        evaluations = create_sample_evaluations(employees)
        print(f"   ✅ {len(evaluations)} évaluations créées")
        
        print("✨ Base de données peuplée avec succès!")
        print(f"📈 Résumé:")
        print(f"   - Employés: {len(employees)}")
        print(f"   - Offres d'emploi: {len(job_postings)}")
        print(f"   - Candidats: {len(candidates)}")
        print(f"   - Candidatures: {len(applications)}")
        print(f"   - Évaluations: {len(evaluations)}")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {str(e)}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    # Configuration de l'application Flask pour accéder à la base de données
    from src.main import app
    
    with app.app_context():
        main()

