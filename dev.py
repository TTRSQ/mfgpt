import time
from src.adapter import gpt
from src.adapter import gmail
import json

mails = gmail.latest_messages()
ids = [m.id for m in mails[:5]]

mail_details = []
for id in ids:
    mail_details.append(gmail.get_message(id))
    time.sleep(1)

for mail in mail_details:
    res = gpt.check_importance(
        json.dumps(
            {
                "title": mail.subject,
                "from": mail.sender,
                "snippet": mail.snippet,
            },
            ensure_ascii=False,
        )
    )
    print("入力:", mail.subject)
    print("出力:", res)
    print()
    time.sleep(1)
