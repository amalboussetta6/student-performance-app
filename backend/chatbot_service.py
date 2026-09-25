from schemas import ChatData
from chatbot_intents import detect_intent


# ==========================================================
# NOMS LISIBLES DES VARIABLES
# ==========================================================

VARIABLE_LABELS = {
    "gender": "genre",
    "study_hours_per_week": "temps d'étude",
    "attendance_rate": "taux de présence",
    "past_exam_scores": "résultats académiques précédents",
    "parental_education_level": "environnement éducatif",
    "internet_access_at_home": "accès aux ressources numériques",
    "extracurricular_activities":
        "organisation entre études et activités extrascolaires"
}


# ==========================================================
# MEILLEURE RECOMMANDATION
# ==========================================================

def get_best_recommendation(recommendations: list):

    if len(recommendations) == 0:
        return None

    return max(
        recommendations,
        key=lambda recommendation:
            recommendation["estimated_gain"]
    )


# ==========================================================
# NOM TECHNIQUE -> TEXTE LISIBLE
# ==========================================================

def get_variable_label(variable: str):

    return VARIABLE_LABELS.get(
        variable,
        variable
    )


# ==========================================================
# CHERCHER UNE RECOMMANDATION PRÉCISE
# ==========================================================

def find_recommendation(
    recommendations: list,
    variable: str
):

    return next(
        (
            recommendation
            for recommendation in recommendations
            if recommendation["variable"] == variable
        ),
        None
    )


# ==========================================================
# RÉSUMÉ DES RECOMMANDATIONS
# ==========================================================

def get_recommendations_summary(
    recommendations: list
):

    if len(recommendations) == 0:

        return (
            "Je n'ai pas identifié de recommandation "
            "prioritaire pour ce profil. "
            "Continuez à maintenir de bonnes habitudes "
            "de travail et une présence régulière."
        )


    labels = []

    for recommendation in recommendations:

        variable = recommendation["variable"]

        labels.append(
            get_variable_label(variable)
        )


    if len(labels) == 1:

        return (
            f"Le principal point que vous pouvez "
            f"travailler est votre {labels[0]}."
        )


    return (
        "Les principaux points que vous pouvez "
        "travailler sont : "
        + ", ".join(labels)
        + "."
    )


# ==========================================================
# RÉPONSE DU CHATBOT
# ==========================================================

def generate_chat_answer(data: ChatData):

    # ------------------------------------------------------
    # 1. Comprendre le type de question
    # ------------------------------------------------------

    intent = detect_intent(
        data.question
    )


    # ======================================================
    # RÉSUMÉ DU PROFIL
    # ======================================================

    if intent == "profile_summary":

        student = data.student

        internet_text = (
            "avec accès à Internet"
            if student.internet_access_at_home.lower() == "yes"
            else "sans accès à Internet"
        )

        activities_text = (
            "avec des activités extrascolaires"
            if student.extracurricular_activities.lower() == "yes"
            else "sans activités extrascolaires"
        )

        return (
            f"Votre profil indique "
            f"{student.study_hours_per_week:.1f} heures "
            f"d'étude par semaine, un taux de présence "
            f"de {student.attendance_rate:.2f} %, "
            f"un score académique précédent de "
            f"{student.past_exam_scores:.2f} sur 100, "
            f"{internet_text} et {activities_text}. "
            f"Votre score prédit actuel est de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # SCORE PRÉDIT
    # ======================================================

    if intent == "score":

        return (
            f"Votre score prédit est de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # RÉSULTAT PASS / FAIL
    # ======================================================

    if intent == "result":

        return (
            f"Votre résultat est {data.result} "
            f"avec un score prédit de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # EST-CE QUE L'ÉTUDIANT A RÉUSSI ?
    # ======================================================

    if intent == "pass_status":

        if data.result == "Pass":

            return (
                "Oui. Selon la prédiction actuelle, "
                "vous êtes en situation de réussite "
                f"avec {data.predicted_score:.2f} "
                "sur 100."
            )

        return (
            "Non. Selon la prédiction actuelle, "
            f"votre score est de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # POINTS MANQUANTS
    # ======================================================

    if intent == "missing_points":

        if data.predicted_score >= 60:

            return (
                "Votre score prédit atteint déjà "
                "le seuil de réussite de 60 sur 100."
            )

        missing_points = round(
            60 - data.predicted_score,
            2
        )

        return (
            f"Il vous manque environ "
            f"{missing_points} points pour atteindre "
            f"le seuil de 60 sur 100."
        )


    # ======================================================
    # TAUX DE PRÉSENCE
    # ======================================================

    if intent == "attendance_value":

        attendance = (
            data.student.attendance_rate
        )

        return (
            f"Votre taux de présence actuel "
            f"est de {attendance:.2f} %."
        )


    # ======================================================
    # HEURES D'ÉTUDE
    # ======================================================

    if intent == "study_hours_value":

        study_hours = (
            data.student.study_hours_per_week
        )

        return (
            f"Vous avez indiqué environ "
            f"{study_hours:.1f} heures d'étude "
            f"par semaine."
        )


    # ======================================================
    # SCORE PRÉCÉDENT
    # ======================================================

    if intent == "past_score":

        past_score = (
            data.student.past_exam_scores
        )

        return (
            f"Votre score académique précédent "
            f"est de {past_score:.2f} sur 100."
        )


    # ======================================================
    # INTERNET
    # ======================================================

    if intent == "internet":

        internet = (
            data.student.internet_access_at_home
        )

        if internet.lower() == "yes":

            return (
                "Vous avez indiqué disposer "
                "d'un accès à Internet à domicile."
            )

        return (
            "Vous avez indiqué ne pas disposer "
            "d'un accès à Internet à domicile."
        )


    # ======================================================
    # ACTIVITÉS EXTRASCOLAIRES
    # ======================================================

    if intent == "activities":

        activities = (
            data.student.extracurricular_activities
        )

        if activities.lower() == "yes":

            return (
                "Vous avez indiqué participer "
                "à des activités extrascolaires."
            )

        return (
            "Vous avez indiqué ne pas participer "
            "à des activités extrascolaires."
        )


    # ======================================================
    # CONSEIL SUR LA PRÉSENCE
    # ======================================================

    if intent == "attendance_advice":

        recommendation = find_recommendation(
            data.recommendations,
            "attendance_rate"
        )

        attendance = (
            data.student.attendance_rate
        )

        if recommendation is not None:

            return (
                f"Votre taux de présence actuel est de "
                f"{attendance:.2f} %. "
                "Dans votre profil actuel, améliorer "
                "la présence fait partie des pistes "
                "identifiées pour progresser."
            )

        return (
            f"Votre taux de présence actuel est de "
            f"{attendance:.2f} %. "
            "La présence n'apparaît pas actuellement "
            "comme une recommandation prioritaire."
        )


    # ======================================================
    # CONSEIL SUR LE TEMPS D'ÉTUDE
    # ======================================================

    if intent == "study_advice":

        recommendation = find_recommendation(
            data.recommendations,
            "study_hours_per_week"
        )

        study_hours = (
            data.student.study_hours_per_week
        )

        if recommendation is not None:

            return (
                f"Vous avez indiqué "
                f"{study_hours:.1f} heures d'étude "
                "par semaine. Dans votre profil actuel, "
                "augmenter le temps d'étude fait partie "
                "des pistes identifiées pour progresser."
            )

        return (
            f"Vous avez indiqué "
            f"{study_hours:.1f} heures d'étude "
            "par semaine. Augmenter ce temps "
            "n'apparaît pas actuellement comme "
            "une recommandation prioritaire."
        )


    # ======================================================
    # PRIORITÉ
    # ======================================================

    if intent == "priority":

        best_recommendation = (
            get_best_recommendation(
                data.recommendations
            )
        )

        if best_recommendation is None:

            return (
                "Votre profil est déjà assez équilibré. "
                "Continuez à maintenir de bonnes "
                "habitudes d'étude et une présence "
                "régulière."
            )


        variable = (
            best_recommendation["variable"]
        )

        variable_label = (
            get_variable_label(variable)
        )

        return (
            f"Votre priorité devrait être "
            f"d'améliorer votre {variable_label}. "
            "C'est actuellement le point "
            "le plus intéressant à travailler "
            "dans votre profil."
        )


    # ======================================================
    # LISTE DES RECOMMANDATIONS
    # ======================================================

    if intent == "recommendations":

        return get_recommendations_summary(
            data.recommendations
        )


    # ======================================================
    # POURQUOI LE SCORE EST FAIBLE ?
    # ======================================================

    if intent == "low_score_reason":

        if data.result == "Pass":

            return (
                "Votre résultat est globalement "
                "satisfaisant. Vous pouvez toutefois "
                "continuer à améliorer certaines "
                "habitudes pour progresser davantage."
            )


        best_recommendation = (
            get_best_recommendation(
                data.recommendations
            )
        )


        if best_recommendation is None:

            return (
                "Votre résultat semble dépendre "
                "de plusieurs éléments de votre profil "
                "plutôt que d'un seul point particulier."
            )


        variable = (
            best_recommendation["variable"]
        )

        variable_label = (
            get_variable_label(variable)
        )

        return (
            f"Votre résultat peut notamment être "
            f"lié à votre {variable_label}. "
            "C'est actuellement l'un des principaux "
            "points que vous pouvez travailler."
        )


    # ======================================================
    # QUALITÉ DU RÉSULTAT
    # ======================================================

    if intent == "result_quality":

        if data.predicted_score >= 60:

            return (
                f"Votre score prédit est de "
                f"{data.predicted_score:.2f} sur 100 "
                "et dépasse le seuil de réussite."
            )

        return (
            f"Votre score prédit est de "
            f"{data.predicted_score:.2f} sur 100. "
            "Il reste donc certains points "
            "à améliorer pour atteindre "
            "le seuil de réussite."
        )


    # ======================================================
    # QUESTION NON RECONNUE
    # ======================================================

    return (
        "Je n'ai pas reconnu précisément votre question. "
        "Vous pouvez me demander par exemple : "
        "\"Résume mon profil\", "
        "\"Quelle est ma note ?\", "
        "\"Est-ce que j'ai réussi ?\", "
        "\"Combien me manque-t-il pour réussir ?\", "
        "\"Quel est mon taux de présence ?\", "
        "\"Dois-je étudier plus ?\", "
        "\"Dois-je améliorer ma présence ?\", "
        "\"Que dois-je améliorer en premier ?\", "
        "\"Quelles sont mes recommandations ?\" "
        "ou \"Pourquoi ma note est-elle basse ?\""
    )