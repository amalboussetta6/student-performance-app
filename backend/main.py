from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import StudentData, ChatData
from prediction_service import predict_student
from recommendation_service import generate_recommendations
from chatbot_service import generate_chat_answer
from similarity_service import find_similar_profiles
from analysis_service import calculate_feature_importance


# --------------------------------------------------
# Création de l'application FastAPI
# --------------------------------------------------

app = FastAPI(
    title="Student Performance Prediction API",
    description="API de prédiction de la performance académique",
    version="1.0.0"
)


# --------------------------------------------------
# Configuration CORS
# --------------------------------------------------

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Route de test
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Student Performance API fonctionne"
    }


# --------------------------------------------------
# Prédiction
# --------------------------------------------------

@app.post("/predict")
def predict(data: StudentData):

    predicted_score, result = predict_student(data)

    recommendations = generate_recommendations(
        data,
        predicted_score
    )

    return {
        "predicted_score": predicted_score,
        "result": result,
        "recommendations": recommendations
    }


# --------------------------------------------------
# Importance des variables
# --------------------------------------------------

@app.get("/feature-importance")
def get_feature_importance():

    features = calculate_feature_importance()

    return {
        "features": features
    }


# --------------------------------------------------
# Assistant conversationnel
# --------------------------------------------------

@app.post("/chat")
def chat(data: ChatData):

    answer = generate_chat_answer(data)

    return {
        "answer": answer
    }


# --------------------------------------------------
# Profils similaires
# --------------------------------------------------

@app.post("/similar-profiles")
def get_similar_profiles(data: StudentData):

    return find_similar_profiles(data)