# Guide de Déploiement - Portail RH

Ce guide détaille les différentes méthodes de déploiement du Portail RH avec IA.

## 🚀 Options de Déploiement

### 1. Déploiement Local avec Docker

#### Prérequis
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB espace disque

#### Configuration
1. Clonez le repository
```bash
git clone https://github.com/votre-org/portail-rh.git
cd portail-rh
```

2. Configurez les variables d'environnement
```bash
cp .env.example .env
# Éditez le fichier .env avec vos valeurs
```

3. Démarrez les services
```bash
docker-compose up -d
```

4. Initialisez la base de données
```bash
docker-compose exec backend python src/scripts/populate_data.py
```

L'application sera accessible sur :
- Frontend : http://localhost:3000
- Backend API : http://localhost:5000
- Base de données : localhost:5432

### 2. Déploiement sur Heroku

#### Backend (Flask)

1. Créez une application Heroku
```bash
heroku create portail-rh-backend
```

2. Ajoutez les add-ons
```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

3. Configurez les variables d'environnement
```bash
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set FLASK_ENV=production
```

4. Déployez
```bash
git subtree push --prefix=portail-rh-backend heroku main
```

#### Frontend (React)

1. Buildez l'application
```bash
cd portail-rh-frontend
npm run build
```

2. Déployez sur Netlify ou Vercel
```bash
# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod
```

### 3. Déploiement sur AWS

#### Architecture recommandée
- **Frontend** : S3 + CloudFront
- **Backend** : ECS Fargate ou EC2
- **Base de données** : RDS PostgreSQL
- **Cache** : ElastiCache Redis

#### Étapes de déploiement

1. **Infrastructure avec Terraform**
```hcl
# main.tf
provider "aws" {
  region = "eu-west-1"
}

# S3 bucket pour le frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "portail-rh-frontend"
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier = "portail-rh-db"
  engine     = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  db_name  = "portail_rh"
  username = "postgres"
  password = var.db_password
  
  skip_final_snapshot = true
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "portail-rh"
}
```

2. **Déploiement du backend sur ECS**
```bash
# Build et push de l'image
docker build -t portail-rh-backend ./portail-rh-backend
docker tag portail-rh-backend:latest 123456789.dkr.ecr.eu-west-1.amazonaws.com/portail-rh-backend:latest
docker push 123456789.dkr.ecr.eu-west-1.amazonaws.com/portail-rh-backend:latest

# Déploiement ECS
aws ecs update-service --cluster portail-rh --service backend --force-new-deployment
```

3. **Déploiement du frontend sur S3**
```bash
cd portail-rh-frontend
npm run build
aws s3 sync dist/ s3://portail-rh-frontend --delete
aws cloudfront create-invalidation --distribution-id E123456789 --paths "/*"
```

### 4. Déploiement sur Google Cloud Platform

#### Services utilisés
- **Frontend** : Cloud Storage + Cloud CDN
- **Backend** : Cloud Run
- **Base de données** : Cloud SQL PostgreSQL

#### Étapes

1. **Configuration du projet**
```bash
gcloud config set project portail-rh-project
gcloud services enable run.googleapis.com sql-component.googleapis.com
```

2. **Déploiement du backend**
```bash
cd portail-rh-backend
gcloud run deploy backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

3. **Configuration de la base de données**
```bash
gcloud sql instances create portail-rh-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1

gcloud sql databases create portail_rh --instance=portail-rh-db
```

### 5. Déploiement sur Azure

#### Services utilisés
- **Frontend** : Static Web Apps
- **Backend** : Container Instances ou App Service
- **Base de données** : Azure Database for PostgreSQL

#### Étapes

1. **Création des ressources**
```bash
az group create --name portail-rh-rg --location westeurope

az postgres server create \
  --resource-group portail-rh-rg \
  --name portail-rh-db \
  --location westeurope \
  --admin-user postgres \
  --admin-password YourPassword123 \
  --sku-name B_Gen5_1
```

2. **Déploiement du backend**
```bash
az container create \
  --resource-group portail-rh-rg \
  --name portail-rh-backend \
  --image portail-rh-backend:latest \
  --dns-name-label portail-rh-api \
  --ports 5000 \
  --environment-variables OPENAI_API_KEY=your_key
```

## 🔧 Configuration de Production

### Variables d'environnement

#### Backend
```env
# Flask
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# Base de données
DATABASE_URL=postgresql://user:password@host:5432/dbname

# OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_API_BASE=https://api.openai.com/v1

# Redis (optionnel)
REDIS_URL=redis://localhost:6379

# Sécurité
CORS_ORIGINS=https://your-frontend-domain.com
JWT_SECRET_KEY=your-jwt-secret

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

#### Frontend
```env
# API
VITE_API_BASE_URL=https://your-backend-domain.com/api

# Analytics (optionnel)
VITE_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
VITE_SENTRY_DSN=your-frontend-sentry-dsn
```

### Optimisations de Performance

#### Backend
1. **Mise en cache avec Redis**
```python
# Configuration Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
cache = redis.from_url(REDIS_URL)

# Cache des requêtes fréquentes
@cache.memoize(timeout=300)
def get_employee_analytics():
    return analytics_service.get_employee_analytics()
```

2. **Optimisation des requêtes SQL**
```python
# Utilisation d'eager loading
employees = Employee.query.options(
    joinedload(Employee.evaluations),
    joinedload(Employee.manager)
).all()
```

3. **Pagination et filtres**
```python
# Pagination efficace
employees = Employee.query.filter_by(status='active').paginate(
    page=page, per_page=20, error_out=False
)
```

#### Frontend
1. **Code splitting**
```javascript
// Lazy loading des pages
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Employees = lazy(() => import('./pages/Employees'))
```

2. **Optimisation des images**
```javascript
// Utilisation de WebP et lazy loading
<img 
  src="image.webp" 
  loading="lazy" 
  alt="Description"
/>
```

### Sécurité

#### HTTPS et SSL
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
}
```

#### Authentification JWT
```python
# Configuration JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

@jwt_required()
def protected_endpoint():
    current_user = get_jwt_identity()
    return jsonify(user=current_user)
```

#### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@limiter.limit("100 per minute")
@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    pass
```

### Monitoring et Logs

#### Configuration Sentry
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

#### Logs structurés
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_entry)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
app.logger.addHandler(handler)
```

### Sauvegarde et Récupération

#### Sauvegarde automatique de la base de données
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://portail-rh-backups/
```

#### Cron job pour les sauvegardes
```bash
# Ajout au crontab
0 2 * * * /path/to/backup.sh
```

## 🔍 Vérification du Déploiement

### Tests de santé
```bash
# Test de l'API backend
curl -f http://your-backend-domain.com/api/health || exit 1

# Test du frontend
curl -f http://your-frontend-domain.com || exit 1
```

### Métriques à surveiller
- Temps de réponse API < 500ms
- Taux d'erreur < 1%
- Utilisation CPU < 80%
- Utilisation mémoire < 85%
- Espace disque disponible > 20%

## 🆘 Dépannage

### Problèmes courants

#### Backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs backend

# Vérifier les variables d'environnement
docker-compose exec backend env | grep -E "(DATABASE_URL|OPENAI_API_KEY)"
```

#### Erreurs de base de données
```bash
# Vérifier la connexion
docker-compose exec backend python -c "from src.models.user import db; print(db.engine.url)"

# Réinitialiser la base de données
docker-compose exec backend python -c "from src.models.user import db; db.create_all()"
```

#### Problèmes de performance
```bash
# Analyser les requêtes lentes
docker-compose exec db psql -U postgres -d portail_rh -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;"
```

Pour plus d'aide, consultez la [documentation complète](https://docs.portail-rh.com) ou ouvrez une [issue GitHub](https://github.com/votre-org/portail-rh/issues).

