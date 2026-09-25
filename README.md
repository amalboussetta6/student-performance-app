# Student Performance Prediction

Application web permettant de prédire la performance académique d'un étudiant à partir de ses habitudes et de son parcours scolaire.

Le projet combine un modèle de Machine Learning avec une API FastAPI et une interface web Angular.

## Fonctionnalités

- Prédiction de la note finale
- Classification Pass / Fail
- Recommandations personnalisées
- Importance des variables
- Assistant conversationnel
- Historique du chatbot
- Recherche de profils étudiants similaires
- Comparaison avec la performance moyenne des profils similaires

## Technologies utilisées

### Machine Learning
- Python
- Pandas
- Scikit-learn
- Joblib

### Backend
- FastAPI
- Uvicorn

### Frontend
- Angular
- TypeScript
- HTML
- CSS
- Bootstrap

## Architecture

```text
student-performance-app/
│
├── backend/
│   ├── main.py
│   ├── student_performance_model.joblib
│   ├── student_performance_dataset.csv
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── angular.json
│
├── .gitignore
└── README.md