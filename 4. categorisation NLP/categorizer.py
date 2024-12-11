"""
Module de catégorisation de mails.
"""

import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "data/model.pkl"
VECTORIZER_PATH = "data/vectorizer.pkl"

def train_model():
    """
    Entraîne un modèle et le sauvegarde, ou charge un modèle existant.
    """
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        # Charger un modèle déjà existant
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    else:
        # Charger les données d'entraînement
        with open("data/categories.json", "r", encoding="utf-8") as f:
            category_data = json.load(f)
        texts = [item["text"] for item in category_data]
        labels = [item["category"] for item in category_data]

        # Entraîner le modèle
        vectorizer = TfidfVectorizer()
        x = vectorizer.fit_transform(texts)

        model = LogisticRegression()
        model.fit(x, labels)

        # Sauvegarder le modèle et le vectoriseur
        joblib.dump(model, MODEL_PATH)
        joblib.dump(vectorizer, VECTORIZER_PATH)

    return vectorizer, model


def categorize_mails(preprocessed_mails):
    """
    Catégorise une liste de mails prétraités.
    
    Args:
        preprocessed_mails (list of str): Liste de textes prétraités.
    
    Returns:
        list of str: Liste des catégories attribuées.
    """
    vectorizer, model = train_model()
    x = vectorizer.transform(preprocessed_mails)
    return model.predict(x)
