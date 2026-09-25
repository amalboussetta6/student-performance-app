from schemas import StudentData, ChatData
from prediction_service import model, predict_student
from recommendation_service import generate_recommendations
from chatbot_service import generate_chat_answer
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


    # -------------------------------------------------
    # 1. VARIABLES NUMÉRIQUES
    # -------------------------------------------------

    numeric_values = {
        "study_hours_per_week": data.study_hours_per_week,
        "attendance_rate": data.attendance_rate,
        "past_exam_scores": data.past_exam_scores
    }


    # -------------------------------------------------
    # 2. VARIABLES CATÉGORIELLES
    # -------------------------------------------------

    categorical_values = {
        "gender": data.gender,
        "parental_education_level": data.parental_education_level,
        "internet_access_at_home": data.internet_access_at_home,
        "extracurricular_activities": data.extracurricular_activities
    }


    # Distance initiale = 0
    df["distance"] = 0.0


    # -------------------------------------------------
    # 3. DISTANCE POUR LES VARIABLES NUMÉRIQUES
    # -------------------------------------------------

    for column, user_value in numeric_values.items():

        column_min = df[column].min()
        column_max = df[column].max()

        column_range = column_max - column_min

        if column_range > 0:

            df["distance"] += (
                abs(df[column] - user_value)
                / column_range
            )


    # -------------------------------------------------
    # 4. DISTANCE POUR LES VARIABLES CATÉGORIELLES
    # -------------------------------------------------

    for column, user_value in categorical_values.items():

        df["distance"] += (
            df[column] != user_value
        ).astype(int)


    # -------------------------------------------------
    # 5. MOYENNE DE LA DISTANCE
    # -------------------------------------------------

    total_variables = (
        len(numeric_values)
        + len(categorical_values)
    )

    df["distance"] = (
        df["distance"]
        / total_variables
    )


    # -------------------------------------------------
    # 6. PRENDRE LES 5 PROFILS LES PLUS PROCHES
    # -------------------------------------------------

    similar_students = (
        df
        .sort_values("distance")
        .head(5)
    )


    # -------------------------------------------------
    # 7. PERFORMANCE MOYENNE
    # -------------------------------------------------

    average_score = round(
        float(
            similar_students["final_exam_score"].mean()
        ),
        2
    )


    # Pourcentage d'étudiants ayant réussi
    pass_rate = round(
        float(
            (
                similar_students["pass_fail"]
                .str.lower()
                == "pass"
            ).mean()
            * 100
        ),
        2
    )


    # -------------------------------------------------
    # 8. PRÉPARER UNE PETITE LISTE DES PROFILS
    # -------------------------------------------------

    profiles = []

    for _, student in similar_students.iterrows():

        profiles.append({
            "study_hours_per_week":
                float(student["study_hours_per_week"]),

            "attendance_rate":
                round(float(student["attendance_rate"]), 2),

            "past_exam_scores":
                float(student["past_exam_scores"]),

            "final_exam_score":
                float(student["final_exam_score"]),

            "result":
                student["pass_fail"]
        })


    # -------------------------------------------------
    # 9. RETOURNER LE RÉSULTAT
    # -------------------------------------------------

    return {
        "number_of_profiles": len(similar_students),
        "average_score": average_score,
        "pass_rate": pass_rate,
        "profiles": profiles
    }