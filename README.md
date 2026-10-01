# 🎓 Student Performance Prediction

Application web intelligente permettant de prédire la performance académique d'un étudiant à partir de ses habitudes scolaires.

Le projet combine **Machine Learning**, **FastAPI** et **Angular** afin de proposer une solution complète allant de la prédiction de la note jusqu'à l'analyse des facteurs influents, aux recommandations personnalisées, à la comparaison avec des profils similaires et à un assistant conversationnel.

---

## 📌 Présentation du projet

La réussite académique peut dépendre de plusieurs facteurs liés aux habitudes de l'étudiant, tels que :

- le temps consacré aux études ;
- le taux de présence ;
- les résultats académiques précédents ;
- l'environnement éducatif ;
- l'accès à Internet ;
- les activités extrascolaires.

L'objectif du projet est d'utiliser le Machine Learning afin d'estimer la performance académique d'un étudiant à partir de ces informations.

Le projet a été développé en deux grandes phases.

### Phase 1 — Data Science et Machine Learning

La première phase comprend :

- exploration du dataset ;
- nettoyage des données ;
- suppression des doublons ;
- préparation des variables ;
- encodage des variables catégorielles ;
- séparation des données en ensembles d'entraînement et de test ;
- entraînement de plusieurs modèles ;
- évaluation des performances ;
- sélection du modèle final ;
- sauvegarde du pipeline Machine Learning.

### Phase 2 — Application Web et fonctionnalités intelligentes

La deuxième phase transforme le prototype initial en une véritable application web composée de :

- un frontend Angular ;
- une API REST FastAPI ;
- un modèle Machine Learning chargé au démarrage du backend ;
- un système de recommandations personnalisées ;
- une analyse de l'importance des variables ;
- un assistant conversationnel ;
- un système de recherche de profils similaires.

---

# 🎯 Objectifs

L'application permet de :

- saisir le profil et les habitudes d'un étudiant ;
- prédire sa note finale ;
- déterminer un résultat `Pass` ou `Fail` ;
- identifier les variables ayant le plus d'influence sur le modèle ;
- proposer des pistes d'amélioration personnalisées ;
- comparer le profil avec des étudiants similaires du dataset ;
- permettre à l'étudiant de poser des questions sur son résultat.

---

# 🏗️ Architecture

L'application suit une architecture séparant le frontend, l'API et le modèle Machine Learning.

```text
Utilisateur
    │
    ▼
Angular Frontend
    │
    │ HTTP / REST
    ▼
FastAPI Backend
    │
    ├── Prediction Service
    ├── Recommendation Service
    ├── Analysis Service
    ├── Similarity Service
    └── Chatbot Service
    │
    ▼
Scikit-learn Pipeline
    │
    ▼
Prédiction
```

---

# 🧠 Machine Learning

Le modèle est entraîné à partir du dataset **Student Performance Prediction Dataset**.

## Variables utilisées

Les variables d'entrée utilisées par l'application sont :

| Variable | Description |
|---|---|
| `gender` | Genre de l'étudiant |
| `study_hours_per_week` | Nombre d'heures d'étude par semaine |
| `attendance_rate` | Taux de présence |
| `past_exam_scores` | Résultats des examens précédents |
| `parental_education_level` | Niveau d'éducation des parents |
| `internet_access_at_home` | Accès Internet à domicile |
| `extracurricular_activities` | Participation à des activités extrascolaires |

La variable cible utilisée pour la prédiction est :

```text
final_exam_score
```

---

## Prétraitement

Le pipeline Machine Learning prend en charge la préparation nécessaire des données avant la prédiction.

Le modèle final est sauvegardé dans :

```text
backend/student_performance_model.joblib
```

Le fichier `.joblib` contient le pipeline utilisé par l'API pour effectuer les prédictions.

---

# 🚀 Backend FastAPI

Le backend est développé avec **FastAPI**.

Il est responsable de :

- recevoir les données envoyées par Angular ;
- valider les données ;
- appeler le modèle Machine Learning ;
- générer la prédiction ;
- produire les recommandations ;
- calculer l'importance des variables ;
- rechercher les profils similaires ;
- gérer l'assistant conversationnel.

---

## Endpoints API

### `GET /`

Vérifie que l'API fonctionne.

Exemple :

```json
{
  "message": "Student Performance API fonctionne"
}
```

---

### `POST /predict`

Reçoit le profil de l'étudiant et retourne :

- le score prédit ;
- le résultat ;
- les recommandations personnalisées.

Exemple de requête :

```json
{
  "gender": "Male",
  "study_hours_per_week": 20,
  "attendance_rate": 75,
  "past_exam_scores": 70,
  "parental_education_level": "Bachelors",
  "internet_access_at_home": "Yes",
  "extracurricular_activities": "Yes"
}
```

Exemple de réponse :

```json
{
  "predicted_score": 65.42,
  "result": "Pass",
  "recommendations": [
    {
      "variable": "attendance_rate",
      "message": "Améliorer votre taux de présence pourrait augmenter votre performance.",
      "current_value": 75,
      "tested_value": 85,
      "estimated_gain": 2.31
    }
  ]
}
```

---

### `GET /feature-importance`

Retourne l'importance globale des variables utilisées par le modèle.

Cette analyse est calculée avec la méthode **Permutation Importance**.

Exemple :

```json
{
  "features": [
    {
      "variable": "past_exam_scores",
      "importance": 0.42
    }
  ]
}
```

---

### `POST /similar-profiles`

Recherche dans le dataset les étudiants ayant un profil proche de celui fourni par l'utilisateur.

Le système prend en compte :

- les différences entre variables numériques ;
- les différences entre variables catégorielles.

L'API retourne notamment :

- les profils les plus similaires ;
- leur score final ;
- leur résultat ;
- leur performance moyenne ;
- leur taux de réussite.

---

### `POST /chat`

Permet d'interagir avec l'assistant étudiant.

L'assistant utilise :

- la prédiction actuelle ;
- le résultat ;
- le profil étudiant ;
- les recommandations générées.

Exemples de questions :

```text
Quelle est ma note ?
```

```text
Est-ce que j'ai réussi ?
```

```text
Pourquoi ma note est-elle basse ?
```

```text
Que dois-je améliorer en premier ?
```

```text
Dois-je étudier plus ?
```

```text
Dois-je améliorer ma présence ?
```

```text
Combien me manque-t-il pour réussir ?
```

---

# 💡 Recommandations personnalisées

Le système de recommandations effectue des simulations locales sur certaines variables que l'étudiant peut améliorer.

Les variables actuellement simulées sont :

```text
study_hours_per_week
attendance_rate
```

Pour chaque variable, le système :

1. récupère la valeur actuelle ;
2. crée une nouvelle situation simulée ;
3. relance le modèle ;
4. compare la nouvelle prédiction à la prédiction initiale ;
5. calcule le gain estimé ;
6. classe les recommandations selon leur impact.

Exemple :

```text
Taux de présence

Valeur actuelle : 70 %
Valeur simulée : 80 %
Gain estimé : +3.25 points
```

Les recommandations correspondent à des simulations du modèle et ne doivent pas être interprétées comme des relations causales.

---

# 📊 Importance des variables

L'application propose également une analyse globale des variables.

La méthode utilisée est :

```text
Permutation Importance
```

Le principe consiste à modifier aléatoirement les valeurs d'une variable et à mesurer la diminution des performances du modèle.

Une diminution importante signifie que la variable joue un rôle important dans les prédictions du modèle.

Cette analyse est différente des recommandations personnalisées :

```text
Feature Importance
        =
analyse globale du modèle

Recommandations
        =
analyse locale du profil étudiant
```

---

# 👥 Profils similaires

L'application recherche les étudiants du dataset dont les habitudes sont proches du profil saisi.

Pour les variables numériques, les différences sont normalisées afin d'éviter qu'une variable ayant une grande échelle domine le calcul.

Pour les variables catégorielles :

```text
Même valeur       → distance = 0
Valeur différente → distance = 1
```

Les profils ayant la distance la plus faible sont sélectionnés.

L'application affiche ensuite :

- leurs heures d'étude ;
- leur présence ;
- leurs résultats précédents ;
- leur note finale ;
- leur résultat ;
- leur performance moyenne ;
- leur taux de réussite.

Ces informations sont fournies à titre comparatif et ne représentent pas une probabilité individuelle de réussite.

---

# 💬 Assistant conversationnel

L'assistant conversationnel permet d'expliquer les résultats de manière simple.

Il s'agit d'un assistant basé sur la détection d'intentions.

Le système :

```text
Question utilisateur
        ↓
Normalisation du texte
        ↓
Détection de l'intention
        ↓
Analyse du contexte étudiant
        ↓
Génération de la réponse
```

Exemples d'intentions :

- résumé du profil ;
- score prédit ;
- résultat ;
- statut de réussite ;
- points manquants ;
- conseils sur la présence ;
- conseils sur le temps d'étude ;
- priorité d'amélioration ;
- recommandations ;
- explication d'un score faible.

---

# 🌐 Frontend Angular

Le frontend est développé avec :

- Angular ;
- TypeScript ;
- HTML ;
- CSS ;
- Bootstrap.

L'interface permet de saisir les informations de l'étudiant et d'afficher :

- la prédiction ;
- le résultat ;
- les recommandations personnalisées ;
- les profils similaires ;
- le chatbot ;
- l'importance globale des variables.

---

# 📁 Structure du projet

```text
student-performance-app/
│
├── backend/
│   │
│   ├── main.py
│   ├── schemas.py
│   ├── prediction_service.py
│   ├── recommendation_service.py
│   ├── analysis_service.py
│   ├── similarity_service.py
│   ├── chatbot_service.py
│   ├── chatbot_intents.py
│   ├── data_service.py
│   ├── student_performance_model.joblib
│   └── requirements.txt
│
├── data/
│   └── student_performance_dataset_clean.csv
│
├── frontend/
│   │
│   ├── src/
│   │   └── app/
│   │       └── prediction/
│   │           ├── prediction.component.ts
│   │           ├── prediction.component.html
│   │           └── prediction.component.css
│   │
│   ├── package.json
│   └── angular.json
│
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## Prérequis

Le projet a été testé avec :

```text
Python 3.12
Node.js
npm
Angular
```

Python 3.12 est recommandé pour garantir la compatibilité avec les dépendances du projet.

---

# 🐍 Installation du backend

Se placer dans le dossier backend :

```powershell
cd backend
```

Créer un environnement virtuel :

```powershell
py -3.12 -m venv venv-local
```

Activer l'environnement :

```powershell
.\venv-local\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

Lancer l'API :

```powershell
python -m uvicorn main:app --reload
```

Le backend fonctionne sur :

```text
http://127.0.0.1:8000
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

---

# 🅰️ Installation du frontend

Ouvrir un deuxième terminal.

Se placer dans le dossier frontend :

```powershell
cd frontend
```

Installer les dépendances :

```powershell
npm install
```

Lancer Angular :

```powershell
npx ng serve
```

L'application est disponible sur :

```text
http://localhost:4200
```

---

# 🔄 Communication Frontend / Backend

Le frontend Angular envoie des requêtes HTTP vers FastAPI.

```text
Angular
http://localhost:4200

        │
        │ HTTP
        ▼

FastAPI
http://127.0.0.1:8000

        │
        ▼

Machine Learning Model
```

CORS est configuré dans FastAPI afin d'autoriser le frontend Angular local.

---

# 🛠️ Technologies utilisées

## Data Science / Machine Learning

```text
Python
Pandas
NumPy
SciPy
Scikit-learn
Joblib
```

## Backend

```text
FastAPI
Pydantic
Uvicorn
```

## Frontend

```text
Angular
TypeScript
HTML
CSS
Bootstrap
```

## Outils

```text
Git
GitHub
VS Code
Jupyter / Google Colab
```

---

# 📈 Workflow général

```text
Dataset
   ↓
Exploration
   ↓
Nettoyage
   ↓
Prétraitement
   ↓
Train / Test
   ↓
Entraînement
   ↓
Évaluation
   ↓
Pipeline final
   ↓
Joblib
   ↓
FastAPI
   ↓
Angular
   ↓
Utilisateur
```

---

# 🔐 Remarques

Les prédictions et recommandations fournies par l'application sont basées sur les données disponibles dans le dataset et sur le comportement du modèle Machine Learning.

Elles sont destinées à fournir une estimation et une aide à l'analyse.

Les recommandations simulées ne représentent pas une relation causale garantie entre une habitude et la performance académique.

---

# 📚 Projet de stage

Projet réalisé dans le cadre d'un **stage d'été 2026**.

Sujet :

> **Prédiction de la performance académique selon les habitudes de l'étudiant**

Le projet a évolué d'un prototype Data Science vers une application web complète intégrant un frontend Angular, une API FastAPI et plusieurs fonctionnalités d'analyse basées sur le Machine Learning.

---

# 👩‍💻 Auteur

**Amal Boussetta**

Projet de stage d'été 2026.

---

# 🏷️ Mots-clés

`Machine Learning` `Python` `FastAPI` `Angular` `Scikit-learn`
`Data Science` `REST API` `Student Performance`
`Explainable AI` `TypeScript`