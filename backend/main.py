from schemas import StudentData, ChatData
from prediction_service import model, predict_student
from recommendation_service import generate_recommendations
from chatbot_service import generate_chat_answer
from similarity_service import find_similar_profiles
from analysis_service import calculate_feature_importance

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



import pandas as pd

from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split


app = FastAPI()
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





@app.get("/")
def home():

    return {"message": "API fonctionne"}




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

@app.post("/chat")
def chat(data: ChatData):

    answer = generate_chat_answer(data)

    return {
        "answer": answer
    }

@app.get("/feature-importance")
def get_feature_importance():

    features = calculate_feature_importance()

    return {
        "features": features
    }

@app.post("/similar-profiles")
def get_similar_profiles(data: StudentData):

    return find_similar_profiles(data)



