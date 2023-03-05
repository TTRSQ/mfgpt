from dataclasses import dataclass
from typing import List

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# adapter
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


@dataclass
class ListItem:
    id: str
    threadId: str


@dataclass
class DetailItem:
    id: str
    threadId: str
    sender: str
    subject: str
    snippet: str
    timeStamp: int


def __auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("./keys/token.json"):
        creds = Credentials.from_authorized_user_file("./keys/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./keys/client_secret.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("./keys/token.json", "w") as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    return service


def latest_messages() -> List[ListItem]:
    service = __auth()

    try:
        messages_result = (
            service.users()
            .messages()
            .list(userId="me", maxResults=100, includeSpamTrash=False)
            .execute()
        )
        messages = messages_result["messages"]

        retMsgs = []
        for message in messages:
            retMsgs.append(ListItem(message["id"], message["threadId"]))
        return retMsgs

    except HttpError as error:
        raise error


def get_message(id: str) -> DetailItem:
    service = __auth()

    try:
        message_result = service.users().messages().get(userId="me", id=id).execute()
        froms = [
            item["value"]
            for item in message_result["payload"]["headers"]
            if item["name"] == "From"
        ]
        subjects = [
            item["value"]
            for item in message_result["payload"]["headers"]
            if item["name"] == "Subject"
        ]

        return DetailItem(
            id,
            message_result["threadId"],
            froms[0] if len(froms) > 0 else "Unknown",
            subjects[0] if len(subjects) > 0 else "Nontitle",
            message_result["snippet"],
            int(int(message_result["internalDate"]) / 1000),
        )

    except HttpError as error:
        raise error


def generate_prompt(mail: DetailItem) -> str:
    sub = mail.subject.replace('"', "").replace("'", "").replace("　", " ")
    sender = mail.sender.replace('"', "").replace("'", "").replace("　", " ")
    snipet = mail.snippet.replace('"', "").replace("'", "").replace("　", " ")
    prompt = f"title: {sub}\nfrom: {sender}\nsnippet: {snipet}\n\n\n###\n\n"
    return prompt
