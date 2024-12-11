"""
Module qui permet de récupérer les ID et threadsID de ma boite mail et 
les enregistrer dans un fichier id_data.py
"""

import os
import json
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():
    """
    Fonction qui permet de s'authentifier sur Gmail.

    Returns:
        Service : Service Gmail
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_id(service, max_results=10):
    """Fonction qui retourne tous les ID et threadsID de ma boite mail
    et les enregistre sous forme de tableau dans un fichier id_data.py
    1. Setup la fonction : création du tableau data_id, et configuration
    du fichier id_data.py pour pouvoir écrire dedans
    2. Récupère tous les "id" et "threadId" de ma boite mail
    3. Enregistre "id" et "threadId" dans id_data puis passe à la page suivante

    Returns:
        Table : [{"id" : id, "threadId" : threadId, "label_premierTour": ""}, ...]
    """
    data_id = []
    i = 0
    print(f"Page {i}")

    # Récupère les messages de la première page
    message = service.users().messages().list(userId="me").execute()
    for msg in message["messages"]:
        if len(data_id) >= max_results:
            break
        message_id = msg["id"]
        thread_id = msg["threadId"]
        data_id.append({"id": message_id, "threadId": thread_id, "label": ""})

    # Récupérer les pages suivantes si elles existent
    while "nextPageToken" in message and len(data_id) < max_results:
        message = (
            service.users()
            .messages()
            .list(userId="me", pageToken=message["nextPageToken"])
            .execute()
        )
        for msg in message["messages"]:
            if len(data_id) >= max_results:
                break
            message_id = msg["id"]
            thread_id = msg["threadId"]
            data_id.append({"id": message_id, "threadId": thread_id, "label": ""})

        i += 1
        print(f"Page {i}")

    # Enregistre les données sous forme de tableau dans le fichier
    with open("data/id_data.json", "w", encoding="utf-8") as file_id:
        json.dump(data_id, file_id, ensure_ascii=False, indent=4)

    return data_id


def get_objet_expediteur(service, mail_id):
    """
    Fonction qui retourne l'objet et l'expediteur d'un mail en fonction de l'id d'un
    mail avec l'API de gmail

    Args:
        service ():
        mailID (String): ID du mail dans l'API Gmail

    Returns:
        Table: [objet, expediteur]
    """
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=mail_id, format="metadata")
        .execute()
    )
    headers = msg.get("payload", {}).get("headers", [])

    expediteur = None
    objet = None

    for header in headers:
        if header.get("name") == "From":
            expediteur = header.get("value")
        elif header.get("name") == "Subject":
            objet = header.get("value")

    return [objet, expediteur]


def get_contenu_mail(service, mail_id):
    """Fonction qui retourne le contenu d'un mail (texte ou HTML) à partir de l'id d'un mail
    grâce à l'API de gmail. Décodage du mail pour afficher une chaîne de caractères
    classique que l'on peut lire sans problème.

    Args:
        service ():
        mail_id (String): id du mail

    Returns:
        String: contenu du mail
    """
    message = (
        service.users().messages().get(userId="me", id=mail_id, format="raw").execute()
    )
    msg_str = base64.urlsafe_b64decode(message["raw"].encode("utf-8")).decode(
        "utf-8", errors="replace"
    )
    mime_msg = email.message_from_string(msg_str)

    contenu_mail = ""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                contenu_mail = part.get_payload(decode=True)
                if contenu_mail:
                    contenu_mail = contenu_mail.decode("utf-8", errors="replace")
                    break
            elif content_type == "text/html" and "attachment" not in content_disposition:
                contenu_mail = part.get_payload(decode=True)
                if contenu_mail:
                    contenu_mail = contenu_mail.decode("utf-8", errors="replace")
                    break
    else:
        contenu_mail = mime_msg.get_payload(decode=True)
        if contenu_mail:
            contenu_mail = contenu_mail.decode("utf-8", errors="replace")

    return contenu_mail if contenu_mail else "Contenu de l'e-mail introuvable"


def fill_data(service, data_id):
    """
    Fonction qui remplit les données de data_id avec l'objet, l'expediteur et le contenu
    de chaque mail

    Args:
        service ():
        data_id (Table): Tableau de données
    """
    for mail in data_id:
        mail_id = mail["id"]
        objet, expediteur = get_objet_expediteur(service, mail_id)
        mail["objet"] = objet
        mail["expediteur"] = expediteur
        mail["contenu"] = get_contenu_mail(service, mail_id)

    with open("data/mails.json", "w", encoding="utf-8") as file_id:
        json.dump(data_id, file_id, ensure_ascii=False, indent=4)
