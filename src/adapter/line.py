import os
import requests

line_notify_token = os.environ.get("LINE_NOTIFY_TOKEN")


def notify_message(message: str):
    requests.post(
        "https://notify-api.line.me/api/notify",
        data={"message": message},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {line_notify_token}",
        },
    )
