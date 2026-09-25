from schemas import ChatData


# Traduction des noms techniques vers des noms lisibles
VARIABLE_LABELS = {
    "study_hours_per_week": "temps d'étude",
    "attendance_rate": "taux de présence",
    "past_exam_scores": "résultats académiques précédents",
    "internet_access_at_home": "accès aux ressources numériques",
    "extracurricular_activities": (
        "organisation entre études et activités extrascolaires"
    ),
    "parental_education_level": "environnement éducatif"
}


def get_best_recommendation(recommendations: list):

    if len(recommendations) == 0:
        return None

    return max(
        recommendations,
        key=lambda recommendation:
            recommendation["estimated_gain"]
    )


def get_variable_label(variable: str):

    return VARIABLE_LABELS.get(
        variable,
        variable
    )


def generate_chat_answer(data: ChatData):

    question = data.question.lower().strip()


    # --------------------------------------------------
    # 1. Question sur la priorité
    # --------------------------------------------------

    if (
        "améliorer en premier" in question
        or "ameliorer en premier" in question
        or "que dois-je améliorer" in question
        or "que dois-je ameliorer" in question
        or "priorité" in question
        or "priorite" in question
    ):

        best_recommendation = get_best_recommendation(
            data.recommendations
        )

        if best_recommendation is None:

            return (
                "Votre profil est déjà assez équilibré. "
                "Continuez à maintenir de bonnes habitudes "
                "d'étude et une présence régulière."
            )

        variable = best_recommendation["variable"]

        variable_label = get_variable_label(
            variable
        )

        return (
            f"Votre priorité devrait être d'améliorer votre "
            f"{variable_label}, car c'est actuellement "
            f"l'élément le plus important à travailler "
            f"dans votre profil."
        )


    # --------------------------------------------------
    # 2. Question sur une note basse
    # --------------------------------------------------

    if (
        "pourquoi ma note" in question
        or "pourquoi mon score" in question
        or "note est basse" in question
        or "note basse" in question
        or "score faible" in question
    ):

        if data.result == "Pass":

            return (
                "Votre résultat est globalement satisfaisant. "
                "Vous pouvez toutefois continuer à améliorer "
                "certaines habitudes pour progresser davantage."
            )


        best_recommendation = get_best_recommendation(
            data.recommendations
        )


        if best_recommendation is None:

            return (
                "Votre résultat semble dépendre de plusieurs "
                "éléments de votre profil plutôt que d'un seul "
                "point particulier. Essayez de maintenir une "
                "bonne régularité dans vos études et votre "
                "présence en cours."
            )


        variable = best_recommendation["variable"]

        variable_label = get_variable_label(
            variable
        )


        return (
            f"Votre résultat peut notamment être lié à votre "
            f"{variable_label}. C'est actuellement l'un des "
            f"principaux points que vous pouvez travailler "
            f"pour améliorer votre performance."
        )


    # --------------------------------------------------
    # 3. Question non reconnue
    # --------------------------------------------------

    return (
        "Je peux vous aider à comprendre votre résultat "
        "et à identifier les points que vous pouvez améliorer. "
        "Vous pouvez par exemple me demander : "
        "\"Que dois-je améliorer en premier ?\" "
        "ou \"Pourquoi ma note est-elle basse ?\""
    )