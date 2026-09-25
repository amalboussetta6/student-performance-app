from schemas import StudentData, ChatData
from prediction_service import model, predict_student
from recommendation_service import generate_recommendations
from chatbot_service import generate_chat_answer
from similarity_service import find_similar_profiles
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

    # Charger le dataset
    df = pd.read_csv("student_performance_dataset.csv")

    # Normaliser les noms des colonnes
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Supprimer les doublons
    df = df.drop_duplicates().reset_index(drop=True)

    # Variable cible
    y = df["final_exam_score"]

    # Variables utilisées par le modèle
    X = df.drop(
        columns=[
            "final_exam_score",
            "student_id",
            "pass_fail"
        ]
    )

    # Même découpage 80 / 20 utilisé pendant le projet
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    # Calcul de l'importance des variables
    importance = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=20,
        random_state=42,
        scoring="r2"
    )

    features = []

    for variable, value in zip(
        X_test.columns,
        importance.importances_mean
    ):
        features.append({
            "variable": variable,
            "importance": round(float(value), 4)
        })

    # Trier de la plus importante à la moins importante
    features = sorted(
        features,
        key=lambda item: item["importance"],
        reverse=True
    )

    return {
        "features": features
    }

@app.post("/similar-profiles")
def get_similar_profiles(data: StudentData):

    return find_similar_profiles(data)



