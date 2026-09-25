from pathlib import Path

import pandas as pd

from schemas import StudentData


# --------------------------------------------------
# Chemin vers le dataset
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "student_performance_dataset.csv"


# --------------------------------------------------
# Charger et préparer le dataset
# --------------------------------------------------

def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    df = df.drop_duplicates().reset_index(drop=True)

    return df


# --------------------------------------------------
# Rechercher les profils similaires
# --------------------------------------------------

def find_similar_profiles(
    data: StudentData,
    number_of_profiles: int = 5
):

    df = load_dataset()


    # Variables numériques
    numeric_values = {
        "study_hours_per_week":
            data.study_hours_per_week,

        "attendance_rate":
            data.attendance_rate,

        "past_exam_scores":
            data.past_exam_scores
    }


    # Variables catégorielles
    categorical_values = {
        "gender":
            data.gender,

        "parental_education_level":
            data.parental_education_level,

        "internet_access_at_home":
            data.internet_access_at_home,

        "extracurricular_activities":
            data.extracurricular_activities
    }


    # Distance initiale
    df["distance"] = 0.0


    # --------------------------------------------------
    # Distance des variables numériques
    # --------------------------------------------------

    for column, user_value in numeric_values.items():

        column_min = df[column].min()
        column_max = df[column].max()

        column_range = column_max - column_min


        if column_range > 0:

            normalized_difference = (
                abs(df[column] - user_value)
                / column_range
            )

            df["distance"] += normalized_difference


    # --------------------------------------------------
    # Distance des variables catégorielles
    # --------------------------------------------------

    for column, user_value in categorical_values.items():

        categorical_difference = (
            df[column] != user_value
        ).astype(int)

        df["distance"] += categorical_difference


    # --------------------------------------------------
    # Calculer la distance moyenne
    # --------------------------------------------------

    total_variables = (
        len(numeric_values)
        + len(categorical_values)
    )

    df["distance"] = (
        df["distance"]
        / total_variables
    )


    # --------------------------------------------------
    # Garder les profils les plus proches
    # --------------------------------------------------

    similar_students = (
        df
        .sort_values("distance")
        .head(number_of_profiles)
    )


    # --------------------------------------------------
    # Performance moyenne
    # --------------------------------------------------

    average_score = round(
        float(
            similar_students[
                "final_exam_score"
            ].mean()
        ),
        2
    )


    # --------------------------------------------------
    # Taux de réussite
    # --------------------------------------------------

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


    # --------------------------------------------------
    # Préparer la réponse
    # --------------------------------------------------

    profiles = []

    for _, student in similar_students.iterrows():

        profiles.append({
            "study_hours_per_week":
                float(
                    student[
                        "study_hours_per_week"
                    ]
                ),

            "attendance_rate":
                round(
                    float(
                        student[
                            "attendance_rate"
                        ]
                    ),
                    2
                ),

            "past_exam_scores":
                float(
                    student[
                        "past_exam_scores"
                    ]
                ),

            "final_exam_score":
                float(
                    student[
                        "final_exam_score"
                    ]
                ),

            "result":
                student["pass_fail"]
        })


    return {
        "number_of_profiles":
            len(similar_students),

        "average_score":
            average_score,

        "pass_rate":
            pass_rate,

        "profiles":
            profiles
    }