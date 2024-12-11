# Classification Supervisée des Emails

Ce sous-dossier a pour responsabilité d'extraire les emails (ID, objet, émetteur, contenu) via l'API de Gmail, de les stocker dans une base de données locale, puis d'utiliser un modèle de NLP avec `nltk` pour préprocesser les données et déterminer leur catégorie.

## 🥰 Fonctionnalités

- **Extraction des emails** : Le script utilise l'API Gmail pour récupérer les emails et extraire les informations suivantes :
  - ID de l'email
  - Objet de l'email
  - Émetteur de l'email
  - Contenu de l'email

- **Prétraitement et classification** : Utilisation de `nltk` pour prétraiter les données et classifier les emails dans l'une des catégories suivantes :
  - `commercial`
  - `newsletter`
  - `personnel`
  - `service`
  - `autre` (pour les emails ne correspondant à aucune des catégories principales)
  - Les spams sont automatiquement classés comme `commercial`.

- **Enregistrement des résultats** : Les résultats sont enregistrés dans un fichier `emails_classifies.json`, incluant les informations suivantes :
  - ID de l'email
  - Objet de l'email
  - Émetteur de l'email
  - Contenu de l'email
  - Catégorie déterminée (`label_deuxiemeTour`)

## 🤓 Prérequis

Avant d'exécuter ce script, assurez-vous d'avoir :

1. Python 3.x installé.
2. Les bibliothèques `nltk` et `spacy` installées :
    ```bash
   pip install nltk spacy
   python -m spacy download en_core_web_sm
   ```
3. Un fichier `credentials.json` pour l'API Gmail.

## 🧐 Installation

1. Clonez ce dépôt ou copiez le script.
2. Installez les dépendances Python :
    ```bash
   pip install -r requirements.txt
   ```
3. Placez le fichier `credentials.json` dans le répertoire principal

## 😝 Utilisation

1. Lancez le script en exécutant la commande suivante dans votre terminal :
    ```bash
   python main.py
   ```
2. Processus :
    - Le script initialise l'authentification avec l'API Gmail.
    - Les emails sont extraits et stockés dans une base de données locale.
    - Chaque email est prétraité et classifié avec le modèle de NLP.
    - Les résultats sont enregistrés dans le fichier `emails_classifies.json`.
3. Format de sortie : Exemple de structure dans `emails_classifies.json` :
    ```json
    {
        "mail_id_1": {
            "expediteur": "exp1@example.com",
            "objet": "Objet 1",
            "contenu": "Contenu de l'email 1",
            "label_deuxiemeTour": "newsletter"
        },
        "mail_id_2": {
            "expediteur": "exp2@example.com",
            "objet": "Objet 2",
            "contenu": "Contenu de l'email 2",
            "label_deuxiemeTour": "commercial"
        }
    }
    ```

## 🗂️ Structure du Code

Le sous-dossier contient les fichiers suivants :
    - `main.py` : Point d'entrée principal pour le programme. Ce script extrait les emails via l'API Gmail, les prétraite et les analyse à l'aide du modèle de classification supervisée, et enregistre les résultats dans un fichier JSON.
    - `credentials.json` : Fichier de configuration pour l'API Gmail.
    - `requirements.txt` : Liste des dépendances Python nécessaires pour exécuter le script. Inclut `nltk` et `spacy`.
    - `emails_classifies.json` : Fichier généré par le script `main.py` contenant les résultats de la classification. Chaque entrée inclut l'ID de l'email, l'objet, l'émetteur, le contenu, et la catégorie déterminée (`label_deuxiemeTour`).

## 🫣 Exemple de Résultat

Lors de l'exécution, le scirpt affiche les étapes du traitement :
```less
1/100 - email_id_1 : commercial
Label ajouté avec succès !
2/100 - email_id_2 : service
Label ajouté avec succès !
...
Emails non catégorisés : ['email_id_101', 'email_id_102']
```