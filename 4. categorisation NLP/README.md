# Classification Supervisée des Emails

Ce script remplace l'analyse des emails par des modèles LLM par une classification supervisée utilisant `nltk`. Il parcourt une liste de labels issus de `3. appliquer les labels`, les analyse à l'aide d'un modèle de classification supervisée, et génère une sortie catégorisée dans un fichier JSON.

## 🥰 Fonctionnalités

- **Analyse de labels** : Le script prend en entrée des labels et les attribue à l'une des catégories suivantes :
  - `commercial`
  - `newsletter`
  - `personnel`
  - `service`
  - `autre` (pour les labels ne correspondant à aucune des catégories principales)
  - Les spams sont automatiquement classés comme `commercial`.

- **Enregistrement des résultats** : Les résultats sont enregistrés dans un fichier `labels_apres.json`, incluant les informations suivantes :
  - Label initial (`label_premierTour`)
  - Thread ID
  - Label catégorisé après analyse (`label_deuxiemeTour`).

## 🤓 Prérequis

Avant d'exécuter ce script, assurez-vous d'avoir :

1. Python 3.x installé.
2. Les bibliothèques `nltk` et `spacy` installées :
   ```bash
   pip install nltk spacy
   python -m spacy download en_core_web_sm
   ```
3. Un fichier `labels_avant.py` contenant les données `LABELS` récupérées depuis Firebase.

## 🧐 Installation

1. Clonez ce dépôt ou copiez le script.
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Vérifiez que le fichier `labels_avant.py` est structuré comme suit :

    ```python
    LABELS = {
        "mail_id_1": {"label_premierTour": "label1", "threadId": "thread1"},
        "mail_id_2": {"label_premierTour": "label2", "threadId": "thread2"},
        ...
    }
    ```

## 😝 Utilisation

1. Lancez le script en exécutant la commande suivante dans votre terminal :
   ```bash
   python main.py
   ```
2. Processus : Chaque label dans `labels_avant.py` est analysé avec le modèle de classification supervisée.
   Une pause de 1 seconde est incluse entre chaque requête pour éviter les dépassements de limite de l'API.
   Les résultats sont enregistrés dans le fichier `labels_apres.json`.

3. Format de sortie : Exemple de structure dans `labels_apres.json` :
   ```json
   {
       "mail_id_1": {
           "label_premierTour": "label1",
           "threadId": "thread1",
           "label_deuxiemeTour": "newsletter"
       },
       "mail_id_2": {
           "label_premierTour": "label2",
           "threadId": "thread2",
           "label_deuxiemeTour": "commercial"
       }
   }
   ```

## 🫣 Exemple de Résultat

Lors de l'exécution, le script affiche les étapes du traitement :
```less
1/100 - email_id_1 : commercial
Label ajouté avec succès !
2/100 - email_id_2 : service
Label ajouté avec succès !
...
Emails non catégorisés : ['email_id_101', 'email_id_102']
```