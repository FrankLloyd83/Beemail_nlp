"""
Module de prétraitement de texte pour la catégorisation de mails.
"""

import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Assurez-vous d'avoir téléchargé les ressources nécessaires
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("punkt_tab")


def preprocess_mails(mails):
    """
    Prétraite une liste d'emails en nettoyant le texte, en supprimant les 
    stopwords, en tokenisant et en lemmatisant.

    Args:
        mails (list of dict): Liste de dictionnaires contenant les emails 
        avec les clés "subject" et "body".

    Returns:
        list of str: Liste de textes prétraités.
    """
    stop_words = set(stopwords.words("french"))
    lemmatizer = WordNetLemmatizer()
    preprocessed = []

    for mail in mails:
        # Nettoyer le texte (exemple : enlever les balises HTML et caractères spéciaux)
        text = mail.get("subject", "") + " " + mail.get("body", "")
        text = re.sub(r"<[^>]+>", " ", text)  # Supprime les balises HTML
        text = text.lower()  # Convertit en minuscules

        # Tokenisation
        tokens = word_tokenize(text)

        # Suppression des stopwords, lemmatisation, suppression des mots de moins de 3 caractères et des tokens non alphabétiques
        tokens = [
            lemmatizer.lemmatize(word) for word in tokens
            if word.isalpha() and word not in stop_words and len(word) >= 3
        ]

        preprocessed.append(" ".join(tokens))

    # Enregistrer les résultats prétraités dans un fichier JSON
    with open("data/preprocessed_mails.json", "w", encoding="utf-8") as f:
        json.dump(preprocessed, f, ensure_ascii=False, indent=4)

    return preprocessed
