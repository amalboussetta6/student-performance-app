from schemas import StudentData
from prediction_service import model, create_student_dataframe


def generate_recommendations(
    data: StudentData,
    current_score: float
):

    recommendations = []


    # --------------------------------------------------
    # 1. Tester une augmentation du temps d'étude
    # --------------------------------------------------

    if data.study_hours_per_week < 39:

        test_df = create_student_dataframe(data)

        new_study_hours = min(
            data.study_hours_per_week + 5,
            39
        )

        test_df.loc[
            0,
            "study_hours_per_week"
        ] = new_study_hours

        new_prediction = model.predict(test_df)[0]

        new_score = float(new_prediction)

        gain = new_score - current_score


        if gain > 0.5:

            recommendations.append({
                "variable": "study_hours_per_week",

                "message": (
                    "Augmenter votre temps d'étude "
                    "pourrait améliorer votre performance."
                ),

                "estimated_gain": round(gain, 2)
            })


    # --------------------------------------------------
    # 2. Tester une amélioration de la présence
    # --------------------------------------------------

    if data.attendance_rate < 100:

        test_df = create_student_dataframe(data)

        new_attendance = min(
            data.attendance_rate + 10,
            100
        )

        test_df.loc[
            0,
            "attendance_rate"
        ] = new_attendance

        new_prediction = model.predict(test_df)[0]

        new_score = float(new_prediction)

        gain = new_score - current_score


        if gain > 0.5:

            recommendations.append({
                "variable": "attendance_rate",

                "message": (
                    "Améliorer votre taux de présence "
                    "pourrait augmenter votre performance."
                ),

                "estimated_gain": round(gain, 2)
            })


    # --------------------------------------------------
    # 3. Trier les recommandations
    # --------------------------------------------------

    recommendations = sorted(
        recommendations,
        key=lambda recommendation:
            recommendation["estimated_gain"],
        reverse=True
    )


    return recommendations