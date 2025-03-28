# Musée Virtuel - Musée d'Art Virtuel avec Génération IA

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

- Flask (Python)  
- API Hugging Face pour la génération d'images par IA

---

## Démarrage

### Prérequis

- Node.js (v18 ou plus)  
- Python 3.8 ou plus  
- Clé API Hugging Face

---

### Configuration de l'Environnement

1. Créez un fichier `.env` à la racine du projet :

```env
VITE_API_URL=http://localhost:10000
HUGGINGFACE_API_KEY=votre_cle_api_ici
PORT=10000
```

---

### Installation

1. Installez les dépendances du frontend :

```bash
npm install
```

2. Installez les dépendances du backend :

```bash
pip install -r requirements.txt
```

---

## 🛠️ Remarque importante : erreur de génération IA

Si vous rencontrez une erreur lors de la génération d'une image (par exemple un message **"Service Unavailable"**), cela peut être dû à une surcharge ou une instabilité de l'API Hugging Face.

> **Solution** : fermez simplement l'onglet et rouvrez l'application depuis le lien d'origine. Cela relance la session et permet de regénérer correctement l’image.
