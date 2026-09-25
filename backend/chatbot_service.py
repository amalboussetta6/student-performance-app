from schemas import ChatData


# ==========================================================
# NOMS LISIBLES DES VARIABLES
# ==========================================================

VARIABLE_LABELS = {
    "gender": "genre",

    "study_hours_per_week":
        "temps d'étude",

    "attendance_rate":
        "taux de présence",

    "past_exam_scores":
        "résultats académiques précédents",

    "parental_education_level":
        "environnement éducatif",

    "internet_access_at_home":
        "accès aux ressources numériques",

    "extracurricular_activities":
        "organisation entre études et activités extrascolaires"
}


# ==========================================================
# RÉCUPÉRER LA MEILLEURE RECOMMANDATION
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
# TRANSFORMER UN NOM TECHNIQUE EN TEXTE LISIBLE
# ==========================================================

def get_variable_label(variable: str):

    return VARIABLE_LABELS.get(
        variable,
        variable
    )


# ==========================================================
# CHERCHER UNE RECOMMANDATION POUR UNE VARIABLE
# ==========================================================

def find_recommendation(
    recommendations: list,
    variable: str
):

    return next(
        (
            recommendation
            for recommendation in recommendations

            if recommendation["variable"]
            == variable
        ),
        None
    )


# ==========================================================
# CONSTRUIRE UN RÉSUMÉ DES RECOMMANDATIONS
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

        variable_label = get_variable_label(
            variable
        )

        labels.append(variable_label)


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
# GÉNÉRER LA RÉPONSE DU CHATBOT
# ==========================================================

def generate_chat_answer(data: ChatData):

    # ------------------------------------------------------
    # Préparer la question
    # ------------------------------------------------------

    question = (
        data.question
        .lower()
        .strip()
    )


    # ======================================================
    # 1. RÉSUMER LE PROFIL COMPLET
    # ======================================================

    if (
        "résume mon profil" in question
        or "resume mon profil" in question
        or "résumé de mon profil" in question
        or "resume de mon profil" in question
        or "mon profil" == question
    ):

        student = data.student


        internet_text = (
            "avec accès à Internet"
            if student.internet_access_at_home.lower()
            == "yes"
            else "sans accès à Internet"
        )


        activities_text = (
            "avec des activités extrascolaires"
            if student.extracurricular_activities.lower()
            == "yes"
            else "sans activités extrascolaires"
        )


        return (
            f"Votre profil indique "
            f"{student.study_hours_per_week:.1f} heures "
            f"d'étude par semaine, un taux de présence "
            f"de {student.attendance_rate:.2f} %, "
            f"un score académique précédent de "
            f"{student.past_exam_scores:.2f} sur 100, "
            f"{internet_text} et "
            f"{activities_text}. "
            f"Votre score prédit actuel est de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # 2. QUELLE EST MA NOTE ?
    # ======================================================

    if (
        "quelle est ma note" in question
        or "quel est mon score" in question
        or "combien j'ai" in question
        or "combien jai" in question
        or question == "ma note"
        or question == "mon score"
    ):

        return (
            f"Votre score prédit est de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # 3. QUEL EST MON RÉSULTAT ?
    # ======================================================

    if (
        "quel est mon résultat" in question
        or "quel est mon resultat" in question
        or question == "mon résultat"
        or question == "mon resultat"
    ):

        if data.result == "Pass":

            return (
                f"Votre résultat est Pass avec un "
                f"score prédit de "
                f"{data.predicted_score:.2f} sur 100."
            )


        return (
            f"Votre résultat est Fail avec un "
            f"score prédit de "
            f"{data.predicted_score:.2f} sur 100."
        )


    # ======================================================
    # 4. EST-CE QUE J'AI RÉUSSI ?
    # ======================================================

    if (
        "est-ce que j'ai réussi" in question
        or "est ce que j'ai réussi" in question
        or "est-ce que jai réussi" in question
        or "est ce que jai reussi" in question
        or "j'ai réussi" in question
        or "jai reussi" in question
        or "je suis admis" in question
        or "est-ce que je suis admis" in question
        or "est ce que je suis admis" in question
    ):

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
    # 5. COMBIEN ME MANQUE-T-IL POUR RÉUSSIR ?
    # ======================================================

    if (
        "combien me manque" in question
        or "combien de points me manque" in question
        or "combien de points manquent" in question
        or "pour atteindre 60" in question
        or "pour avoir 60" in question
    ):

        if data.predicted_score >= 60:

            return (
                "Votre score prédit atteint déjà "
                "le seuil de réussite de "
                "60 sur 100."
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
    # 6. QUEL EST MON TAUX DE PRÉSENCE ?
    # ======================================================

    if (
        "mon taux de présence" in question
        or "mon taux de presence" in question
        or "quelle est ma présence" in question
        or "quelle est ma presence" in question
        or "combien de présence" in question
        or "combien de presence" in question
    ):

        attendance = (
            data.student.attendance_rate
        )


        return (
            f"Votre taux de présence actuel "
            f"est de {attendance:.2f} %."
        )


    # ======================================================
    # 7. COMBIEN D'HEURES J'ÉTUDIE ?
    # ======================================================

    if (
        "combien d'heures" in question
        or "combien dheures" in question
        or "mes heures d'étude" in question
        or "mes heures d etude" in question
        or "mon temps d'étude" in question
        or "mon temps d etude" in question
    ):

        study_hours = (
            data.student.study_hours_per_week
        )


        return (
            f"Vous avez indiqué environ "
            f"{study_hours:.1f} heures d'étude "
            f"par semaine."
        )


    # ======================================================
    # 8. QUEL EST MON SCORE PRÉCÉDENT ?
    # ======================================================

    if (
        "ancien score" in question
        or "score précédent" in question
        or "score precedent" in question
        or "anciens résultats" in question
        or "anciens resultats" in question
        or "résultats précédents" in question
        or "resultats precedents" in question
    ):

        past_score = (
            data.student.past_exam_scores
        )


        return (
            f"Votre score académique précédent "
            f"est de {past_score:.2f} sur 100."
        )


    # ======================================================
    # 9. ACCÈS À INTERNET
    # ======================================================

    if (
        "internet" in question
        or "accès internet" in question
        or "acces internet" in question
        or "accès à internet" in question
        or "acces a internet" in question
    ):

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
    # 10. ACTIVITÉS EXTRASCOLAIRES
    # ======================================================

    if (
        "activité extrascolaire" in question
        or "activités extrascolaires" in question
        or "activite extrascolaire" in question
        or "activites extrascolaires" in question
    ):

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
    # 11. DOIS-JE AMÉLIORER MA PRÉSENCE ?
    # ======================================================

    if (
        "dois-je améliorer ma présence" in question
        or "dois-je ameliorer ma presence" in question
        or "améliorer ma présence" in question
        or "ameliorer ma presence" in question
        or "présence est importante" in question
        or "presence est importante" in question
    ):

        attendance_recommendation = (
            find_recommendation(
                data.recommendations,
                "attendance_rate"
            )
        )


        if attendance_recommendation:

            return (
                f"Votre taux de présence actuel "
                f"est de "
                f"{data.student.attendance_rate:.2f} %. "
                "Dans votre profil actuel, "
                "améliorer votre présence fait partie "
                "des pistes identifiées pour progresser."
            )


        return (
            f"Votre taux de présence actuel "
            f"est de "
            f"{data.student.attendance_rate:.2f} %. "
            "La présence n'apparaît pas actuellement "
            "comme une recommandation prioritaire "
            "pour votre profil."
        )


    # ======================================================
    # 12. DOIS-JE ÉTUDIER PLUS ?
    # ======================================================

    if (
        "dois-je étudier plus" in question
        or "dois-je etudier plus" in question
        or "augmenter mes heures" in question
        or "plus d'heures d'étude" in question
        or "plus d heures d etude" in question
        or "augmenter mon temps d'étude" in question
        or "augmenter mon temps d etude" in question
    ):

        study_recommendation = (
            find_recommendation(
                data.recommendations,
                "study_hours_per_week"
            )
        )


        if study_recommendation:

            return (
                f"Vous avez indiqué "
                f"{data.student.study_hours_per_week:.1f} "
                "heures d'étude par semaine. "
                "Dans votre profil actuel, augmenter "
                "le temps d'étude fait partie des pistes "
                "identifiées pour progresser."
            )


        return (
            f"Vous avez indiqué "
            f"{data.student.study_hours_per_week:.1f} "
            "heures d'étude par semaine. "
            "Augmenter ce temps n'apparaît pas "
            "actuellement comme une recommandation "
            "prioritaire."
        )


    # ======================================================
    # 13. QUE DOIS-JE AMÉLIORER EN PREMIER ?
    # ======================================================

    if (
        "améliorer en premier" in question
        or "ameliorer en premier" in question
        or "que dois-je améliorer" in question
        or "que dois-je ameliorer" in question
        or "ma priorité" in question
        or "ma priorite" in question
        or question == "priorité"
        or question == "priorite"
    ):

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
    # 14. QUELLES SONT MES RECOMMANDATIONS ?
    # ======================================================

    if (
        "mes recommandations" in question
        or "quelles recommandations" in question
        or "quels conseils" in question
        or "donne-moi des conseils" in question
        or "donne moi des conseils" in question
        or "que puis-je améliorer" in question
        or "que puis-je ameliorer" in question
    ):

        return get_recommendations_summary(
            data.recommendations
        )


    # ======================================================
    # 15. POURQUOI MA NOTE EST-ELLE BASSE ?
    # ======================================================

    if (
        "pourquoi ma note" in question
        or "pourquoi mon score" in question
        or "note est basse" in question
        or "note basse" in question
        or "score faible" in question
        or "pourquoi j'ai cette note" in question
        or "pourquoi jai cette note" in question
    ):

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
                "plutôt que d'un seul point particulier. "
                "Essayez de maintenir une bonne "
                "régularité dans vos études et "
                "votre présence en cours."
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
            "points que vous pouvez travailler "
            "pour améliorer votre performance."
        )


    # ======================================================
    # 16. EST-CE QUE MON RÉSULTAT EST BON ?
    # ======================================================

    if (
        "mon résultat est bon" in question
        or "mon resultat est bon" in question
        or "ma note est bonne" in question
        or "mon score est bon" in question
        or "est-ce une bonne note" in question
        or "est ce une bonne note" in question
    ):

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
    # 17. QUESTION NON RECONNUE
    # ======================================================

    return (
        "Je peux vous aider à comprendre votre résultat "
        "et votre profil. Vous pouvez me demander par "
        "exemple : "
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