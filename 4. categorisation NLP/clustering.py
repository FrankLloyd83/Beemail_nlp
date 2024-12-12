"""
Module qui permet de regrouper les emails en fonction de leur contenu
par un algorithme de clustering
"""

import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster_mails(mails, n_clusters=5):
    """
    Fonction qui regroupe les mails en fonction de leur objet
    par un algorithme de clustering

    Args:
        mails (Table): Tableau de mails
        n_clusters (int): Nombre de clusters

    Returns:
        dict: Dictionnaire avec les indices des mails par cluster
    """
    # Récupération du contenu préprocessé des mails
    text = [mail["preprocessed"] for mail in mails]

    # Vectorisation des contenus
    vectorizer = TfidfVectorizer(stop_words="english")
    x = vectorizer.fit_transform(text)

    # Clustering des contenus
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(x)

    # Création des clusters
    clusters = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(mails[i])

    # Attribution du cluster à chaque mail
    for i, label in enumerate(kmeans.labels_):
        mails[i]["cluster"] = str(label)

    return mails, kmeans, vectorizer


def display_clusters(mails):
    """
    Fonction qui affiche les clusters

    Args:
        mails (dict): Dictionnaire des mails avec leur cluster
    """
    for mail in mails:
        print(f"Cluster {mail['cluster']}: {mail['objet']}")


def save_cluster_results(mails, kmeans, vectorizer):
    """
    Fonction qui sauvegarde les modèles de clustering et de vectorisation au format pickle

    Args:
        mails (dict): Dictionnaire des mails avec leur cluster
        kmeans (KMeans): Modèle de clustering
        vectorizer (TfidfVectorizer): Vectorizer
    """
    with open("data/clustering_results.json", "w", encoding="utf-8") as file:
        json.dump(mails, file, ensure_ascii=False, indent=4)

    with open("data/kmeans.pkl", "wb") as file:
        pickle.dump(kmeans, file)

    with open("data/vectorizer.pkl", "wb") as file:
        pickle.dump(vectorizer, file)


def load_cluster_results(filename="data/clustering_results.json"):
    """
    Fonction qui charge les résultats du clustering

    Args:
        filename (str): Nom du fichier de sauvegarde

    Returns:
        dict: Dictionnaire avec les indices des mails par cluster
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
