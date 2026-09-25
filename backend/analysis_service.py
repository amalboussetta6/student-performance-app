from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

from data_service import load_dataset
from prediction_service import model


def calculate_feature_importance():

    # Charger le dataset
    df = load_dataset()


    # Variable à prédire
    y = df["final_exam_score"]


    # Variables utilisées pour faire la prédiction
    X = df.drop(
        columns=[
            "final_exam_score",
            "student_id",
            "pass_fail"
        ]
    )


    # Séparer les données
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )


    # Calculer l'importance des variables
    importance = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=20,
        random_state=42,
        scoring="r2"
    )


    # Préparer la réponse
    features = []

    for variable, value in zip(
        X_test.columns,
        importance.importances_mean
    ):

        features.append({
            "variable": variable,
            "importance": round(
                float(value),
                4
            )
        })


    # Trier du plus important au moins important
    features = sorted(
        features,
        key=lambda item: item["importance"],
        reverse=True
    )


    return features