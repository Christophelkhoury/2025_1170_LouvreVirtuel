
# Dossier Technique - Trophée-NSI

## 1. Architecture Système

### 1.1 Vue d'ensemble
Le projet est organisé de la manière suivante :
```
Trophee-NSI/
├── .bolt/
├── server/
├── src/
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── eslint.config.js
├── index.html
├── package-lock.json
├── package.json
├── postcss.config.js
├── requirements.txt
├── tailwind.config.js
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

### 1.2 Technologies Utilisées
- **Backend** : Python 3.12, Flask
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript, TypeScript
- **Frameworks et Bibliothèques** : Tailwind CSS, Vite
- **Sécurité** : Gestion des sessions avec Flask, protection CSRF
- **Dépendances** : Voir requirements.txt et package.json

---

## 2. Structure de la Base de Données

### 2.1 Schéma de la Base de Données
```sql
-- Utilisateurs
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Œuvres d'art
CREATE TABLE artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    style TEXT,
    description TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Réservations
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    artwork_id INTEGER,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (artwork_id) REFERENCES artworks(id)
);
```

---

## 3. API Endpoints

### 3.1 Authentification
- `POST /register` : Inscription d'un nouvel utilisateur
- `POST /login` : Connexion de l'utilisateur
- `GET /logout` : Déconnexion de l'utilisateur

### 3.2 Œuvres d'art
- `GET /artworks` : Liste de toutes les œuvres d'art
- `GET /artwork/<id>` : Détails d'une œuvre spécifique
- `POST /artworks/new` : Ajout d'une nouvelle œuvre (réservé aux administrateurs)
- `PUT /artwork/<id>/edit` : Modification d'une œuvre existante
- `DELETE /artwork/<id>/delete` : Suppression d'une œuvre (réservé aux administrateurs)

### 3.3 Réservations
- `GET /bookings` : Liste des réservations de l'utilisateur connecté
- `POST /artwork/<id>/book` : Réserver une visite pour une œuvre
- `POST /booking/<id>/cancel` : Annulation d'une réservation

---

## 4. Sécurité

### 4.1 Authentification
- **Hachage des mots de passe** : Utilisation de Werkzeug pour sécuriser les mots de passe
- **Sessions sécurisées** : Gestion des sessions avec Flask-Session
- **Protection CSRF** : Intégration de tokens CSRF pour les formulaires

### 4.2 Validation des Données
- **Validation des entrées utilisateur** : Contrôle strict des données saisies
- **Protection contre les injections SQL** : Utilisation de requêtes paramétrées
- **Nettoyage des données** : Sanitization des entrées pour éviter les failles XSS

---

## 5. Performance

### 5.1 Optimisations
- **Mise en cache** : Utilisation de mécanismes de cache pour les pages fréquemment consultées
- **Indexation de la base de données** : Ajout d'index sur les colonnes fréquemment interrogées
- **Optimisation des requêtes SQL** : Réduction du nombre de requêtes et optimisation des jointures

### 5.2 Monitoring
- **Logs d'erreurs** : Enregistrement des erreurs applicatives pour le débogage
- **Métriques de performance** : Suivi des temps de réponse et de la charge serveur
- **Suivi des sessions** : Analyse des comportements utilisateurs pour améliorer l'expérience

---

## 6. Déploiement

### 6.1 Prérequis
- Python 3.12+
- Node.js et npm
- pip
- virtualenv

### 6.2 Installation
```bash
# Création de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate

# Installation des dépendances Python
pip install -r requirements.txt

# Installation des dépendances Node.js
npm install

# Compilation des assets frontend
npm run build

# Configuration de l'environnement
cp .env.example .env
# Modifier le fichier .env avec les paramètres appropriés

# Lancement de l'application
python app.py
```

---

## 7. Maintenance

### 7.1 Sauvegarde
- Sauvegarde régulière de la base de données
- Versioning du code source
- Documentation des changements

### 7.2 Mises à Jour
- Procédure documentée de mise à jour
- Tests de compatibilité après modification
- Plan de rollback en cas d’échec

### 7.3 Tests

#### 7.3.1 Tests Unitaires
- Tests des modèles
- Tests des routes
- Tests des utilitaires

#### 7.3.2 Tests d'Intégration
- Tests des workflows
- Tests de performance
- Tests de sécurité
