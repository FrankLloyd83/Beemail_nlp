"""
Module de prétraitement de texte pour la catégorisation de mails.
"""

import re


def preprocess_mails(mails):
    """
    Prétraite une liste de mails.

    Args:
        mails (list of dict): Chaque mail est un dictionnaire avec des clés 
        comme 'subject' et 'body'.

    Returns:
        list of str: Liste de textes prétraités.
    """
    preprocessed = []
    for mail in mails:
        # Nettoyer le texte (exemple : enlever les balises HTML et caractères spéciaux)
        text = mail.get("subject", "") + " " + mail.get("body", "")
        text = re.sub(r"<[^>]+>", " ", text)  # Supprime les balises HTML
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)  # Supprime caractères spéciaux
        text = text.lower()  # Convertit en minuscules
        preprocessed.append(text.strip())
    return preprocessed
