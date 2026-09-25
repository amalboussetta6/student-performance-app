from schemas import StudentData, ChatData
from prediction_service import model, predict_student
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


def generate_recommendations(data, current_score):

    recommendations = []

    # 1. Tester une augmentation des heures d'étude
    if data.study_hours_per_week < 39:

        improved_hours = min(
            data.study_hours_per_week + 5,
            39
        )

        test_df = pd.DataFrame([{
            "gender": data.gender,
            "study_hours_per_week": improved_hours,
            "attendance_rate": data.attendance_rate,
            "past_exam_scores": data.past_exam_scores,
            "parental_education_level": data.parental_education_level,
            "internet_access_at_home": data.internet_access_at_home,
            "extracurricular_activities": data.extracurricular_activities
        }])

        new_score = float(model.predict(test_df)[0])

        gain = new_score - current_score

        if gain > 0.5:
            recommendations.append({
                "variable": "study_hours_per_week",
                "message": "Augmenter votre temps d'étude pourrait améliorer votre performance.",
                "estimated_gain": round(gain, 2)
            })
    # 2. Tester une amélioration du taux de présence
    if data.attendance_rate < 100:

        improved_attendance = min(
            data.attendance_rate + 10,
            100
        )

        test_df = pd.DataFrame([{
            "gender": data.gender,
            "study_hours_per_week": data.study_hours_per_week,
            "attendance_rate": improved_attendance,
            "past_exam_scores": data.past_exam_scores,
            "parental_education_level": data.parental_education_level,
            "internet_access_at_home": data.internet_access_at_home,
            "extracurricular_activities": data.extracurricular_activities
        }])

        new_score = float(model.predict(test_df)[0])

        gain = new_score - current_score

        if gain > 0.5:
            recommendations.append({
                "variable": "attendance_rate",
                "message": "Améliorer votre taux de présence pourrait augmenter votre performance.",
                "estimated_gain": round(gain, 2)
            })

    recommendations = sorted(
        recommendations,
        key=lambda recommendation: recommendation["estimated_gain"],
        reverse=True
    )
    return recommendations

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




@app.post("/chat")
def chat(data: ChatData):

    # Nettoyer la question
    question = data.question.lower().strip()

    # Noms naturels pour les variables
    labels = {
        "study_hours_per_week": "temps d'étude",
        "attendance_rate": "taux de présence",
        "past_exam_scores": "résultats académiques précédents",
        "internet_access_at_home": "accès aux ressources numériques",
        "extracurricular_activities": "organisation entre études et activités extrascolaires",
        "parental_education_level": "environnement éducatif"
    }

    # -------------------------------------------------
    # 1. QUESTION :
    # "Que dois-je améliorer en premier ?"
    # -------------------------------------------------

    if (
        "améliorer en premier" in question
        or "ameliorer en premier" in question
        or "que dois-je améliorer" in question
        or "que dois-je ameliorer" in question
        or "priorité" in question
        or "priorite" in question
    ):

        # Si aucune recommandation n'est disponible
        if len(data.recommendations) == 0:

            return {
                "answer": (
                    "Votre profil est déjà assez équilibré. "
                    "Continuez à maintenir de bonnes habitudes d'étude "
                    "et une présence régulière."
                )
            }

        # Chercher la recommandation la plus importante
        best_recommendation = max(
            data.recommendations,
            key=lambda recommendation: recommendation["estimated_gain"]
        )

        variable = best_recommendation["variable"]

        variable_label = labels.get(
            variable,
            variable
        )

        return {
            "answer": (
                f"Votre priorité devrait être d'améliorer votre "
                f"{variable_label}, car c'est actuellement l'élément "
                f"le plus important à travailler dans votre profil."
            )
        }

    # -------------------------------------------------
    # 2. QUESTION :
    # "Pourquoi ma note est-elle basse ?"
    # -------------------------------------------------

    if (
        "pourquoi ma note" in question
        or "pourquoi mon score" in question
        or "note est basse" in question
        or "note basse" in question
        or "score faible" in question
    ):

        # Si l'étudiant a déjà un résultat positif
        if data.result == "Pass":

            return {
                "answer": (
                    "Votre résultat est globalement satisfaisant. "
                    "Vous pouvez toutefois continuer à améliorer certaines "
                    "habitudes pour progresser davantage."
                )
            }

        # Si aucune recommandation particulière n'existe
        if len(data.recommendations) == 0:

            return {
                "answer": (
                    "Votre résultat semble dépendre de plusieurs éléments "
                    "de votre profil plutôt que d'un seul point particulier. "
                    "Essayez de maintenir une bonne régularité dans vos études "
                    "et votre présence en cours."
                )
            }

        # Chercher le principal point à améliorer
        best_recommendation = max(
            data.recommendations,
            key=lambda recommendation: recommendation["estimated_gain"]
        )

        variable = best_recommendation["variable"]

        variable_label = labels.get(
            variable,
            variable
        )

        return {
            "answer": (
                f"Votre résultat peut notamment être lié à votre "
                f"{variable_label}. "
                f"C'est actuellement l'un des principaux points "
                f"que vous pouvez travailler pour améliorer votre performance."
            )
        }

    # -------------------------------------------------
    # 3. RÉPONSE PAR DÉFAUT
    # -------------------------------------------------

    return {
        "answer": (
            "Je peux vous aider à comprendre votre résultat "
            "et à identifier les points que vous pouvez améliorer. "
            "Vous pouvez par exemple me demander : "
            "\"Que dois-je améliorer en premier ?\" "
            "ou \"Pourquoi ma note est-elle basse ?\""
        )
    }

    # Nettoyer la question pour faciliter la comparaison
    question = data.question.lower().strip()

    # -------------------------------------------------
    # QUESTION :
    # "Que dois-je améliorer en premier ?"
    # -------------------------------------------------

    if (
        "améliorer en premier" in question
        or "ameliorer en premier" in question
        or "que dois-je améliorer" in question
        or "que dois-je ameliorer" in question
        or "priorité" in question
        or "priorite" in question
    ):

        # Si aucune recommandation n'a été trouvée
        if len(data.recommendations) == 0:

            return {
                "answer": (
                    "Votre profil est déjà assez équilibré. "
                    "Continuez à maintenir de bonnes habitudes "
                    "d'étude et une présence régulière."
                )
            }

        # Chercher la recommandation la plus importante
        best_recommendation = max(
            data.recommendations,
            key=lambda recommendation: recommendation["estimated_gain"]
        )

        # Transformer les noms techniques en noms naturels
        labels = {
            "study_hours_per_week": "temps d'étude",
            "attendance_rate": "taux de présence",
            "past_exam_scores": "résultats académiques précédents",
            "internet_access_at_home": "accès aux ressources numériques",
            "extracurricular_activities": "organisation entre études et activités extrascolaires",
            "parental_education_level": "environnement éducatif"
        }

        variable = best_recommendation["variable"]

        variable_label = labels.get(
            variable,
            variable
        )

        # Réponse simple et naturelle
        return {
            "answer": (
                f"Votre priorité devrait être d'améliorer votre "
                f"{variable_label}, car c'est actuellement l'élément "
                f"le plus important à travailler dans votre profil."
            )
        }

    # -------------------------------------------------
    # RÉPONSE PAR DÉFAUT
    # -------------------------------------------------

    return {
        "answer": (
            "Je peux vous aider à comprendre votre résultat "
            "et à identifier les points que vous pouvez améliorer. "
            "Vous pouvez par exemple me demander : "
            "\"Que dois-je améliorer en premier ?\""
        )
    }

    question = data.question.lower().strip()

    if (
        ("améliorer" in question or "ameliorer" in question)
        and
        (
            "premier" in question
            or "priorité" in question
            or "priorite" in question
        )
    ):

        if len(data.recommendations) > 0:

            best_recommendation = data.recommendations[0]

            variable = best_recommendation["variable"]
            gain = best_recommendation["estimated_gain"]

            labels = {
                "study_hours_per_week": "votre temps d'étude",
                "attendance_rate": "votre taux de présence"
            }

            variable_label = labels.get(
                variable,
                variable
            )

            answer = (
                f"Votre priorité devrait être {variable_label}. "
                f"Selon la simulation du modèle, cette amélioration "
                f"pourrait augmenter votre score d'environ {gain:.2f} points."
            )

            return {
                "answer": answer
            }

        else:

            return {
                "answer":
                "Le modèle n'a identifié aucune amélioration prioritaire "
                "parmi les recommandations actuellement testées."
            }

    return {
        "answer":
        "Je n'ai pas encore appris à répondre à cette question."
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