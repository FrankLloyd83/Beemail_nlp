"""
Ce script permet de charger des mails depuis un fichier JSON, 
de les prétraiter et de les catégoriser.
"""

import json
from preprocessing import preprocess_mails
from categorizer import categorize_mails


def main():
    """
    Fonction principale du script.
    """
    # Charger les mails depuis un fichier JSON (ou une source externe)
    with open("data/example_mails.json", "r", encoding="utf-8") as f:
        mails = json.load(f)

    # Étape 1 : Prétraitement des mails
    preprocessed_mails = preprocess_mails(mails)

    # Étape 2 : Catégorisation
    categories = categorize_mails(preprocessed_mails)

    # Affichage des résultats
    for mail, category in zip(mails, categories):
        print(f"Mail: {mail['subject']} -> Catégorie: {category}")


if __name__ == "__main__":
    main()
