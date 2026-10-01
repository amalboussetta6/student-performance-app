from schemas import StudentData
from prediction_service import model, create_student_dataframe


# --------------------------------------------------
# Variables que l'étudiant peut réellement améliorer
# --------------------------------------------------

ACTIONABLE_FEATURES = {
    "study_hours_per_week": {
        "increase": 5,
        "maximum": 39,
        "message": (
            "Augmenter votre temps d'étude "
            "pourrait améliorer votre performance."
        )
    },

    "attendance_rate": {
        "increase": 10,
        "maximum": 100,
        "message": (
            "Améliorer votre taux de présence "
            "pourrait augmenter votre performance."
        )
    }
}


# --------------------------------------------------
# Calculer l'influence locale des variables
# --------------------------------------------------

def calculate_local_influences(
    data: StudentData,
    current_score: float
):

    influences = []

    for variable, config in ACTIONABLE_FEATURES.items():

        current_value = getattr(
            data,
            variable
        )

        maximum = config["maximum"]
        increase = config["increase"]

        # Si la variable est déjà au maximum,
        # on ne peut plus la tester
        if current_value >= maximum:
            continue


        # Créer une copie des données de l'étudiant
        test_df = create_student_dataframe(data)


        # Simuler une amélioration réaliste
        tested_value = min(
            current_value + increase,
            maximum
        )


        # Modifier uniquement la variable testée
        test_df.loc[
            0,
            variable
        ] = tested_value


        # Nouvelle prédiction
        new_prediction = model.predict(
            test_df
        )[0]

        new_score = float(
            new_prediction
        )


        # Impact du changement sur la prédiction
        gain = (
            new_score
            - float(current_score)
        )


        influences.append({
            "variable": variable,

            "current_value": round(
                float(current_value),
                2
            ),

            "tested_value": round(
                float(tested_value),
                2
            ),

            "estimated_gain": round(
                gain,
                2
            ),

            "message": config["message"]
        })


    # Plus grand impact en premier
    influences = sorted(
        influences,
        key=lambda item:
            item["estimated_gain"],
        reverse=True
    )


    return influences


# --------------------------------------------------
# Générer les recommandations
# --------------------------------------------------

def generate_recommendations(
    data: StudentData,
    current_score: float
):

    influences = calculate_local_influences(
        data,
        current_score
    )


    recommendations = []


    for influence in influences:

        # On garde uniquement les changements
        # ayant un effet positif suffisamment important
        if influence["estimated_gain"] > 0.5:

            recommendations.append({
                "variable":
                    influence["variable"],

                "message":
                    influence["message"],

                "current_value":
                    influence["current_value"],

                "tested_value":
                    influence["tested_value"],

                "estimated_gain":
                    influence["estimated_gain"]
            })


    return recommendations