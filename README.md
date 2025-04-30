# Musée Virtuel - Musée d'Art Virtuel avec Génération IA

🚀 **Application Déployée** : [https://museevirtuel.netlify.app/](https://museevirtuel.netlify.app/)
🔧 **Backend API** : [https://trophee-nsi-3.onrender.com](https://trophee-nsi-3.onrender.com) (endpoint de test pour vérifier le statut de l'API)

Une application web moderne qui combine les fonctionnalités d'une galerie d'art traditionnelle avec la génération d'art par intelligence artificielle, offrant des expériences de visualisation en 2D et 3D.

---

## Fonctionnalités

- **Galerie d'Art par Style** : Parcourez des collections d'œuvres organisées selon différents styles artistiques.  
- **Génération d'Art par IA** : Créez de nouvelles œuvres d'art à l'aide de l'IA, en fonction des styles artistiques sélectionnés.  
- **Modes de Visualisation Doubles** :
  - **Vue Galerie 2D** : Disposition en grille traditionnelle avec des informations détaillées sur les œuvres.
  - **Vue Musée 3D** : Environnement immersif en 3D avec murs et cadres virtuels.
- **Éléments Interactifs** :
  - Mode plein écran en vue 3D.  
  - Œuvres cliquables avec informations détaillées.  
  - Génération d'images en temps réel avec retour visuel.

---

## Technologies

### Frontend
- React 18  
- TypeScript  
- Tailwind CSS  
- Three.js avec React Three Fiber  
- Lucide React pour les icônes

### Backend
- Node.js
- Express
- Stability AI API

---

## Déploiement de l'Application

### Prérequis
- Un compte GitHub
- Un compte Render (pour le backend)
- Un compte Netlify (pour le frontend)

### 1. Déploiement du Backend (Render)

1. **Créer un compte Render**
   - Allez sur [render.com](https://render.com)
   - Créez un compte gratuit

2. **Déployer le Backend**
   - Dans le dashboard Render, cliquez sur "New +"
   - Sélectionnez "Web Service"
   - Connectez votre repository GitHub
   - Sélectionnez le repository "2025_1170_LouvreVirtuel"
   - Configurez le service :
     - Name: `louvre-virtuel-backend`
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `flask run --host=0.0.0.0 --port=10000`
     - Plan: `Free`

3. **Configurer les Variables d'Environnement**
   - Dans les paramètres du service, allez dans "Environment"
   - Ajoutez la variable :
     - Key: `STABILITY_API_KEY`
     - Value: `sk-...` (la clé API fournie)

### 2. Déploiement du Frontend (Netlify)

1. **Créer un compte Netlify**
   - Allez sur [netlify.com](https://netlify.com)
   - Créez un compte gratuit

2. **Déployer le Frontend**
   - Dans le dashboard Netlify, cliquez sur "New site from Git"
   - Connectez votre repository GitHub
   - Sélectionnez le repository "2025_1170_LouvreVirtuel"
   - Configurez le build :
     - Build command: `npm run build`
     - Publish directory: `dist`
     - Base directory: `frontend`

3. **Configurer les Variables d'Environnement**
   - Dans les paramètres du site, allez dans "Environment"
   - Ajoutez la variable :
     - Key: `VITE_API_URL`
     - Value: `https://votre-backend-url.onrender.com`

### 3. Vérification du Déploiement

1. **Backend**
   - Vérifiez que l'URL du backend est accessible
   - Testez l'endpoint de santé : `https://votre-backend-url.onrender.com/api/status`

2. **Frontend**
   - Vérifiez que le site est accessible
   - Testez la génération d'images
   - Vérifiez que les images s'affichent correctement

### Notes Importantes

- **API Key** : Utilisez la clé API fournie par mail (pour raison de securite). Elle est préchargée avec 1000 crédits.
- **Coûts** : Chaque génération d'image coûte 0.009$. La clé fournie permet environ 111 images.
- **Limites** : Le plan gratuit de Render a des limites de temps d'exécution. 

### Support

Pour toute question concernant le déploiement, contactez :
- Email: [elkhourychristophe2121@gmail.com]
- GitHub: [Christophelkhoury]

## Structure du Projet

```
2025_1170_LouvreVirtuel/
├── server/             # Backend Node.js
│   └── index.js       # Serveur Express
├── frontend/          # Frontend Vue.js
│   ├── src/
│   └── dist/
└── README.md
```

## Technologies Utilisées

- Backend: Python, Flask
- Frontend: Vue.js, Vite
- API: Stability AI
- Déploiement: Render (Backend), Netlify (Frontend)
