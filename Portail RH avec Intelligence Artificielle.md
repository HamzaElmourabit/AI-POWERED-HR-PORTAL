# Portail RH avec Intelligence Artificielle

Un système de gestion des ressources humaines moderne intégrant des fonctionnalités d'intelligence artificielle pour automatiser et optimiser les processus RH.

## 🚀 Fonctionnalités Principales

### 🤖 Intelligence Artificielle Intégrée
- **Analyse automatique de CV** : Tri et évaluation intelligente des candidatures
- **Matching candidat-poste** : Algorithmes de correspondance avancés
- **Prédiction de performance** : Modèles ML pour anticiper les résultats
- **Détection de risque de turnover** : Identification proactive des employés à risque
- **Assistant virtuel RH** : Chatbot intelligent pour répondre aux questions

### 👥 Gestion des Employés
- Profils employés complets avec historique
- Gestion des performances et évaluations
- Organigramme interactif
- Suivi des compétences et formations

### 🎯 Recrutement Intelligent
- Création d'offres d'emploi optimisées par IA
- Analyse automatique des candidatures
- Génération de questions d'entretien personnalisées
- Suivi du pipeline de recrutement

### 📊 Analytics et Reporting
- Tableaux de bord prédictifs
- Métriques de performance en temps réel
- Rapports automatisés
- Benchmarks sectoriels

## 🏗️ Architecture Technique

### Backend (Flask + Python)
- **Framework** : Flask avec SQLAlchemy
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **IA** : Intégration OpenAI GPT-4
- **APIs** : RESTful avec documentation automatique

### Frontend (React)
- **Framework** : React 18 avec Vite
- **UI** : Tailwind CSS + shadcn/ui
- **Graphiques** : Recharts pour les visualisations
- **Routing** : React Router pour la navigation

### Intelligence Artificielle
- **Modèles** : OpenAI GPT-4 pour l'analyse et les prédictions
- **Analytics** : Pandas et NumPy pour le traitement des données
- **Prédictions** : Algorithmes de machine learning personnalisés

## 📦 Structure du Projet

```
portail-rh/
├── portail-rh-backend/          # Backend Flask
│   ├── src/
│   │   ├── models/              # Modèles de données
│   │   ├── routes/              # Routes API
│   │   ├── services/            # Services métier et IA
│   │   ├── scripts/             # Scripts utilitaires
│   │   └── main.py              # Point d'entrée
│   ├── requirements.txt         # Dépendances Python
│   └── venv/                    # Environnement virtuel
├── portail-rh-frontend/         # Frontend React
│   ├── src/
│   │   ├── components/          # Composants React
│   │   ├── pages/               # Pages de l'application
│   │   └── App.jsx              # Composant principal
│   ├── package.json             # Dépendances Node.js
│   └── dist/                    # Build de production
└── docs/                        # Documentation
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.11+
- Node.js 20+
- Git

### Installation Backend

```bash
cd portail-rh-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Configuration des Variables d'Environnement

Créez un fichier `.env` dans le dossier backend :

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///app.db
```

### Démarrage Backend

```bash
cd portail-rh-backend
source venv/bin/activate
python src/main.py
```

Le backend sera accessible sur `http://localhost:5000`

### Installation Frontend

```bash
cd portail-rh-frontend
npm install
# ou pnpm install
```

### Démarrage Frontend

```bash
cd portail-rh-frontend
npm run dev
# ou pnpm run dev
```

Le frontend sera accessible sur `http://localhost:5173`

## 🔧 Configuration

### Base de Données

Pour initialiser la base de données avec des données de test :

```bash
cd portail-rh-backend
source venv/bin/activate
python src/scripts/populate_data.py
```

### APIs OpenAI

1. Créez un compte sur [OpenAI](https://platform.openai.com/)
2. Générez une clé API
3. Ajoutez la clé dans le fichier `.env`

## 📚 Documentation API

### Endpoints Principaux

#### Employés
- `GET /api/employees` - Liste des employés
- `POST /api/employees` - Créer un employé
- `GET /api/employees/{id}` - Détails d'un employé
- `PUT /api/employees/{id}` - Modifier un employé
- `GET /api/employees/{id}/turnover-risk` - Analyse de risque

#### Recrutement
- `GET /api/job-postings` - Liste des offres d'emploi
- `POST /api/job-postings` - Créer une offre
- `GET /api/candidates` - Liste des candidats
- `POST /api/candidates` - Ajouter un candidat
- `POST /api/applications` - Créer une candidature

#### Analytics
- `GET /api/analytics/dashboard` - Analytics du tableau de bord
- `GET /api/analytics/turnover-risks` - Prédictions de turnover
- `POST /api/analytics/insights` - Génération d'insights IA

#### Chatbot
- `POST /api/chatbot/message` - Envoyer un message au chatbot
- `GET /api/chatbot/quick-actions` - Actions rapides disponibles

## 🧪 Tests

### Tests Backend

```bash
cd portail-rh-backend
source venv/bin/activate
python -m pytest tests/
```

### Tests Frontend

```bash
cd portail-rh-frontend
npm test
```

## 🚀 Déploiement

### Déploiement avec Docker

```bash
# Build des images
docker-compose build

# Démarrage des services
docker-compose up -d
```

### Déploiement sur le Cloud

Le projet est configuré pour être déployé sur :
- **Backend** : Heroku, AWS, Google Cloud
- **Frontend** : Vercel, Netlify, AWS S3
- **Base de données** : PostgreSQL sur cloud

## 🔒 Sécurité

- Authentification JWT
- Validation des données d'entrée
- Protection CORS configurée
- Chiffrement des données sensibles
- Audit des accès aux données

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour obtenir de l'aide :
- 📧 Email : support@portail-rh.com
- 📖 Documentation : [docs.portail-rh.com](https://docs.portail-rh.com)
- 🐛 Issues : [GitHub Issues](https://github.com/votre-org/portail-rh/issues)

## 🙏 Remerciements

- [OpenAI](https://openai.com/) pour les APIs d'intelligence artificielle
- [Flask](https://flask.palletsprojects.com/) pour le framework backend
- [React](https://reactjs.org/) pour le framework frontend
- [Tailwind CSS](https://tailwindcss.com/) pour le design system

