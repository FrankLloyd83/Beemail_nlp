"""
Ce script permet de charger des mails depuis un fichier JSON, 
de les prétraiter et de les catégoriser.
"""

import json
from gmail import authenticate_gmail, get_id, fill_data
from preprocessing import preprocess_mails
from categorizer import categorize_mails


def main():
    """
    Fonction principale du script.
    """
    # Charger les mails depuis un fichier JSON (ou une source externe)
    gmail_service = authenticate_gmail()
    ids = get_id(gmail_service, max_results=10)

    # Remplir les données des mails
    fill_data(gmail_service, ids)

    # Charger les mails depuis le fichier JSON
    with open("data/mails.json", "r", encoding="utf-8") as file:
        mails = json.load(file)

    # Étape 1 : Prétraitement des mails
    preprocessed_mails = preprocess_mails(mails)

    # Étape 2 : Catégorisation
    categories = categorize_mails(preprocessed_mails)

    # Affichage des résultats
    for mail, category in zip(mails, categories):
        print(f"Mail: {mail['objet']} -> Catégorie: {category}")


if __name__ == "__main__":
    main()
