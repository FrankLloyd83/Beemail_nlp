"""
Module de prétraitement de texte pour la catégorisation de mails.
"""

import re
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("punkt_tab")
nltk.download("words")


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
    french_stop_words = set(stopwords.words("french"))
    english_stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    english_words = set(words.words("en"))
    html_stop_words = [
        "html",
        "body",
        "head",
        "div",
        "span",
        "class",
        "id",
        "style",
        "table",
        "tr",
        "td",
        "ul",
        "ol",
        "li",
        "br",
        "hr",
        "meta",
        "link",
        "script",
        "none",
        "block",
        "inline",
        "display",
        "auto",
        "fixed",
        "relative",
        "absolute",
        "static",
        "width",
        "height",
        "margin",
        "padding",
        "border",
        "color",
        "background",
        "font",
        "size",
        "align",
        "top",
        "bottom",
        "left",
        "right",
        "center",
        "position",
        "overflow",
        "float",
        "clear",
        "text",
        "align",
        "style",
        "cursor",
        "pointer",
        "important",
        "screen",
        "media",
        "medium",
        "max",
        "min",
        "vh",
        "vw",
        "px",
        "rem",
        "em",
        "percent",
        "z-index",
    ]

    token_doc_counts = Counter()

    for mail in mails:
        # Nettoyer le texte (exemple : enlever les balises HTML et caractères spéciaux)
        text = mail.get("objet", "") + " " + mail.get("contenu", "")
        text = re.sub(r"<[^>]+>", " ", text)  # Supprime les balises HTML
        text = text.lower()  # Convertit en minuscules

        # Tokenisation
        tokens = word_tokenize(text)

        tokens = [
            lemmatizer.lemmatize(word)
            for word in tokens
            if word.isalpha()
            and word not in french_stop_words
            and word not in english_stop_words
            and word not in html_stop_words
            and len(word) >= 3
            and word in english_words
        ]

        mail["preprocessed"] = " ".join(tokens)
        token_doc_counts.update(set(tokens))

    min_doc_count = 5
    max_doc_ratio = 0.5

    for mail in mails:
        tokens = mail["preprocessed"].split()
        tokens = [
            token
            for token in tokens
            if min_doc_count < token_doc_counts[token] < max_doc_ratio * len(mails)
        ]
        mail["preprocessed"] = " ".join(tokens)

    # Enregistrer les résultats prétraités dans un fichier JSON
    with open("data/mails.json", "w", encoding="utf-8") as f:
        json.dump(mails, f, ensure_ascii=False, indent=4)

    return mails
