import unicodedata


# ==========================================================
# NORMALISER LE TEXTE
# ==========================================================

def normalize_text(text: str) -> str:

    # Minuscules + suppression des espaces autour
    text = text.lower().strip()

    # Transformer les caractères accentués
    # Exemple : "présence" -> "presence"
    text = unicodedata.normalize(
        "NFD",
        text
    )

    text = "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn"
    )

    # Uniformiser certaines apostrophes
    text = text.replace("’", "'")

    # Supprimer les espaces multiples
    text = " ".join(
        text.split()
    )

    return text


# ==========================================================
# INTENTS DU CHATBOT
# ==========================================================

INTENT_PATTERNS = [

    # ------------------------------------------------------
    # Résumé du profil
    # ------------------------------------------------------

    (
        "profile_summary",
        [
            "resume mon profil",
            "resume de mon profil"
        ]
    ),


    # ------------------------------------------------------
    # Conseil sur la présence
    # IMPORTANT : avant attendance_value
    # ------------------------------------------------------

    (
        "attendance_advice",
        [
            "dois-je ameliorer ma presence",
            "ameliorer ma presence",
            "presence est importante"
        ]
    ),


    # ------------------------------------------------------
    # Conseil sur le temps d'étude
    # IMPORTANT : avant study_hours_value
    # ------------------------------------------------------

    (
        "study_advice",
        [
            "dois-je etudier plus",
            "augmenter mes heures",
            "plus d'heures d'etude",
            "augmenter mon temps d'etude"
        ]
    ),


    # ------------------------------------------------------
    # Priorité
    # ------------------------------------------------------

    (
        "priority",
        [
            "ameliorer en premier",
            "que dois-je ameliorer",
            "ma priorite",
            "quelle est ma priorite"
        ]
    ),


    # ------------------------------------------------------
    # Pourquoi résultat faible
    # ------------------------------------------------------

    (
        "low_score_reason",
        [
            "pourquoi ma note",
            "pourquoi mon score",
            "note est basse",
            "note basse",
            "score faible",
            "pourquoi j'ai cette note"
        ]
    ),


    # ------------------------------------------------------
    # Points manquants
    # ------------------------------------------------------

    (
        "missing_points",
        [
            "combien me manque",
            "combien de points me manque",
            "combien de points manquent",
            "pour atteindre 60",
            "pour avoir 60"
        ]
    ),


    # ------------------------------------------------------
    # Réussite
    # ------------------------------------------------------

    (
        "pass_status",
        [
            "est-ce que j'ai reussi",
            "est ce que j'ai reussi",
            "j'ai reussi",
            "je suis admis",
            "est-ce que je suis admis",
            "est ce que je suis admis"
        ]
    ),


    # ------------------------------------------------------
    # Qualité du résultat
    # ------------------------------------------------------

    (
        "result_quality",
        [
            "mon resultat est bon",
            "ma note est bonne",
            "mon score est bon",
            "est-ce une bonne note",
            "est ce une bonne note"
        ]
    ),


    # ------------------------------------------------------
    # Résultat Pass / Fail
    # ------------------------------------------------------

    (
        "result",
        [
            "quel est mon resultat",
            "mon resultat"
        ]
    ),


    # ------------------------------------------------------
    # Score prédit
    # ------------------------------------------------------

    (
        "score",
        [
            "quelle est ma note",
            "quel est mon score",
            "combien j'ai",
            "combien jai"
        ]
    ),


    # ------------------------------------------------------
    # Taux de présence
    # ------------------------------------------------------

    (
        "attendance_value",
        [
            "mon taux de presence",
            "quelle est ma presence",
            "combien de presence"
        ]
    ),


    # ------------------------------------------------------
    # Temps d'étude
    # ------------------------------------------------------

    (
        "study_hours_value",
        [
            "combien d'heures",
            "combien dheures",
            "mes heures d'etude",
            "mon temps d'etude"
        ]
    ),


    # ------------------------------------------------------
    # Score académique précédent
    # ------------------------------------------------------

    (
        "past_score",
        [
            "ancien score",
            "score precedent",
            "anciens resultats",
            "resultats precedents"
        ]
    ),


    # ------------------------------------------------------
    # Internet
    # ------------------------------------------------------

    (
        "internet",
        [
            "internet",
            "acces internet",
            "acces a internet"
        ]
    ),


    # ------------------------------------------------------
    # Activités extrascolaires
    # ------------------------------------------------------

    (
        "activities",
        [
            "activite extrascolaire",
            "activites extrascolaires"
        ]
    ),


    # ------------------------------------------------------
    # Recommandations
    # ------------------------------------------------------

    (
        "recommendations",
        [
            "mes recommandations",
            "quelles recommandations",
            "quels conseils",
            "donne-moi des conseils",
            "donne moi des conseils",
            "que puis-je ameliorer"
        ]
    ),
]


# ==========================================================
# DÉTECTER L'INTENTION
# ==========================================================

def detect_intent(question: str) -> str:

    normalized_question = normalize_text(
        question
    )

    for intent, patterns in INTENT_PATTERNS:

        for pattern in patterns:

            normalized_pattern = normalize_text(
                pattern
            )

            if normalized_pattern in normalized_question:

                return intent

    return "unknown"