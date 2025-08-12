# Documentation API - Portail RH

## Vue d'ensemble

L'API du Portail RH fournit des endpoints RESTful pour gérer les employés, le recrutement, les analytics et les fonctionnalités d'IA.

**Base URL**: `http://localhost:5000/api`

## Authentification

Actuellement, l'API ne nécessite pas d'authentification pour le développement. En production, utilisez JWT tokens.

```http
Authorization: Bearer <token>
```

## Endpoints

### 👥 Employés

#### Lister les employés
```http
GET /api/employees
```

**Paramètres de requête:**
- `page` (int): Numéro de page (défaut: 1)
- `per_page` (int): Éléments par page (défaut: 20)
- `department` (string): Filtrer par département
- `status` (string): Statut de l'employé (défaut: 'active')

**Réponse:**
```json
{
  "employees": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "first_name": "Marie",
      "last_name": "Dubois",
      "email": "marie.dubois@entreprise.com",
      "position": "Développeuse Senior",
      "department": "IT",
      "performance_score": 8.5,
      "status": "active"
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

#### Créer un employé
```http
POST /api/employees
```

**Corps de la requête:**
```json
{
  "employee_id": "EMP007",
  "first_name": "Jean",
  "last_name": "Dupont",
  "email": "jean.dupont@entreprise.com",
  "phone": "+33 1 23 45 67 95",
  "position": "Développeur",
  "department": "IT",
  "hire_date": "2024-02-01",
  "salary": 50000,
  "skills": ["Python", "React", "SQL"]
}
```

#### Obtenir un employé
```http
GET /api/employees/{id}
```

**Paramètres de requête:**
- `include_ai_insights` (bool): Inclure les insights IA

#### Analyser le risque de turnover
```http
GET /api/employees/{id}/turnover-risk
```

**Réponse:**
```json
{
  "risk_score": 7.2,
  "risk_level": "Moyen",
  "risk_factors": [
    "Performance en baisse",
    "Pas d'évaluation récente"
  ],
  "retention_strategies": [
    "Entretien individuel",
    "Plan de formation"
  ]
}
```

### 🎯 Recrutement

#### Lister les offres d'emploi
```http
GET /api/job-postings
```

#### Créer une offre d'emploi
```http
POST /api/job-postings
```

**Corps de la requête:**
```json
{
  "title": "Développeur Full Stack",
  "department": "IT",
  "description": "Description du poste...",
  "requirements": "Exigences du poste...",
  "salary_min": 45000,
  "salary_max": 65000,
  "location": "Paris",
  "employment_type": "CDI",
  "posted_date": "2024-02-01",
  "use_ai_optimization": true
}
```

#### Lister les candidats
```http
GET /api/candidates
```

#### Analyser un candidat pour un poste
```http
POST /api/candidates/{id}/analyze
```

**Corps de la requête:**
```json
{
  "job_posting_id": 1
}
```

**Réponse:**
```json
{
  "candidate_id": 1,
  "job_posting_id": 1,
  "match_score": 8.5,
  "analysis": {
    "strengths": ["Excellente maîtrise technique"],
    "concerns": ["Pas d'expérience en leadership"],
    "recommendation": "Candidat très prometteur"
  }
}
```

#### Générer des questions d'entretien
```http
GET /api/applications/{id}/interview-questions
```

**Réponse:**
```json
{
  "application_id": 1,
  "questions": [
    "Pouvez-vous décrire votre expérience avec React?",
    "Comment gérez-vous les projets complexes?",
    "Quels sont vos objectifs de carrière?"
  ],
  "candidate_name": "Alice Johnson",
  "job_title": "Développeur Full Stack Senior"
}
```

### 📊 Analytics

#### Analytics du tableau de bord
```http
GET /api/analytics/dashboard
```

**Réponse:**
```json
{
  "employees": {
    "total_employees": 247,
    "department_distribution": [
      {"department": "IT", "count": 45},
      {"department": "Marketing", "count": 32}
    ]
  },
  "recruitment": {
    "total_active_jobs": 12,
    "avg_candidate_score": 7.8
  },
  "performance": {
    "avg_performance": 8.3
  },
  "turnover_risks": {
    "high_risk_employees": 3
  }
}
```

#### Prédictions de turnover
```http
GET /api/analytics/turnover-risks
```

#### Générer des insights IA
```http
POST /api/analytics/insights
```

**Corps de la requête:**
```json
{
  "data": {
    "performance_trend": [...],
    "turnover_data": [...]
  }
}
```

#### Rapport mensuel
```http
GET /api/analytics/reports/monthly?date=2024-02-01
```

#### Prédictions futures
```http
GET /api/analytics/predictions
```

### 🤖 Chatbot

#### Envoyer un message
```http
POST /api/chatbot/message
```

**Corps de la requête:**
```json
{
  "message": "Combien d'employés travaillent dans le département IT?",
  "context": {
    "user_id": "user123",
    "session_id": "session456"
  }
}
```

**Réponse:**
```json
{
  "response": "Il y a actuellement 45 employés dans le département IT.",
  "intent": "get_statistics",
  "suggestions": [
    "Voir les détails du département IT",
    "Comparer avec les autres départements"
  ],
  "context": {
    "total_employees": 247,
    "departments": ["IT", "Marketing", "Finance"]
  }
}
```

#### Actions rapides
```http
GET /api/chatbot/quick-actions
```

#### FAQ
```http
GET /api/chatbot/faq
```

## Codes d'erreur

| Code | Description |
|------|-------------|
| 200  | Succès |
| 201  | Créé avec succès |
| 400  | Requête invalide |
| 404  | Ressource non trouvée |
| 500  | Erreur serveur |

## Exemples d'utilisation

### JavaScript/Fetch
```javascript
// Récupérer la liste des employés
const response = await fetch('/api/employees?department=IT');
const data = await response.json();

// Créer un nouvel employé
const newEmployee = {
  employee_id: 'EMP008',
  first_name: 'Alice',
  last_name: 'Martin',
  email: 'alice.martin@entreprise.com',
  position: 'Designer UX',
  department: 'Design',
  hire_date: '2024-02-01'
};

const response = await fetch('/api/employees', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(newEmployee)
});
```

### Python/Requests
```python
import requests

# Récupérer les analytics
response = requests.get('http://localhost:5000/api/analytics/dashboard')
analytics = response.json()

# Analyser un candidat
analysis_data = {'job_posting_id': 1}
response = requests.post(
    'http://localhost:5000/api/candidates/1/analyze',
    json=analysis_data
)
analysis = response.json()
```

### cURL
```bash
# Lister les employés
curl -X GET "http://localhost:5000/api/employees?department=IT"

# Créer une candidature
curl -X POST "http://localhost:5000/api/applications" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_posting_id": 1,
    "application_date": "2024-02-01"
  }'
```

## Limites de taux

- 1000 requêtes par heure par IP
- 100 requêtes par minute pour les endpoints d'IA

## Support

Pour toute question sur l'API :
- 📧 Email : api-support@portail-rh.com
- 📖 Documentation : [docs.portail-rh.com](https://docs.portail-rh.com)
- 🐛 Issues : [GitHub Issues](https://github.com/votre-org/portail-rh/issues)

