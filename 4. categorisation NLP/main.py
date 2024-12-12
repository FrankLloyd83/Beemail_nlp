"""
Ce script permet de charger des mails depuis un fichier JSON, 
de les prétraiter et de les catégoriser.
"""

from gmail import authenticate_gmail, get_id, fill_data
from preprocessing import preprocess_mails
from clustering import (
    cluster_mails,
    display_clusters,
    save_cluster_results,
)


def main():
    """
    Fonction principale du script.
    """
    # Charger les mails depuis un fichier JSON (ou une source externe)
    gmail_service = authenticate_gmail()
    ids = get_id(gmail_service, max_results=100)

    # Remplir les données des mails
    mails = fill_data(gmail_service, ids)

    # Étape 1 : Prétraitement des mails
    preprocessed_mails = preprocess_mails(mails)

    # Étape 2 : Clusterisation
    categories = ["Catégorie 1", "Catégorie 2", "Catégorie 3"]
    clusterized_mails, kmeans, vectorizer = cluster_mails(
        preprocessed_mails, n_clusters=len(categories)
    )
    display_clusters(clusterized_mails)
    save_cluster_results(clusterized_mails, kmeans, vectorizer)


if __name__ == "__main__":
    main()
