from pathlib import Path

import joblib
import pandas as pd

from schemas import StudentData


# --------------------------------------------------
# Chemin vers le modèle
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "student_performance_model.joblib"


# --------------------------------------------------
# Chargement du modèle Machine Learning
# --------------------------------------------------

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# Transformer StudentData en DataFrame
# --------------------------------------------------

def create_student_dataframe(data: StudentData):

    student_df = pd.DataFrame([
        {
            "gender": data.gender,
            "study_hours_per_week": data.study_hours_per_week,
            "attendance_rate": data.attendance_rate,
            "past_exam_scores": data.past_exam_scores,
            "parental_education_level": data.parental_education_level,
            "internet_access_at_home": data.internet_access_at_home,
            "extracurricular_activities": data.extracurricular_activities
        }
    ])

    return student_df


# --------------------------------------------------
# Faire une prédiction
# --------------------------------------------------

def predict_student(data: StudentData):

    student_df = create_student_dataframe(data)

    prediction = model.predict(student_df)[0]

    predicted_score = round(
        float(prediction),
        2
    )

    result = (
        "Pass"
        if predicted_score >= 60
        else "Fail"
    )

    return predicted_score, result