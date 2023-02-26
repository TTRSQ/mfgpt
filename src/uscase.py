from src.adapter import gmail
from src.adapter import bq
from src.adapter import gpt
import time
from typing import List
from src.adapter import line
import json


def get_non_existing_mails() -> List[gmail.DetailItem]:
    print("get latest mails")
    mails = gmail.latest_messages()
    print(f"got {len(mails)} mails")
    if len(mails) == 0:
        return []

    print("check existence")
    exists_mails = bq.list_mails([m.id for m in mails])
    print(f"got {len(exists_mails)} exists mails")
    existence_map = {m.id: True for m in exists_mails}
    new_mails = [m for m in mails if m.id not in existence_map]
    print(f"got {len(new_mails)} new mails")

    print("get detail of new mails")
    detail_new_mails: List[gmail.DetailItem] = []
    for idx in range(len(new_mails)):
        m = new_mails[idx]
        print(f"loading mail of {idx+1}/{len(new_mails)}: ", m.id)
        detail_mail = gmail.get_message(m.id)
        detail_new_mails.append(detail_mail)
        time.sleep(0.5)

    return detail_new_mails


def save_mails(new_mails: List[gmail.DetailItem]):
    if len(new_mails) == 0:
        print("skip insert")
        return
    print("insert new mails to bq length: ", len(new_mails))
    bq.insert_mails(
        [
            bq.Row(m.id, m.threadId, m.sender, m.subject, m.snippet, m.timeStamp)
            for m in new_mails
        ]
    )
    print("inserted")


def notify_new_mails(new_mails: List[gmail.DetailItem]):
    if len(new_mails) == 0:
        print("skip notify")
        return
    print("notify new mails")
    message = ""
    for m in new_mails:
        message += f"https://mail.google.com/mail/u/0/#inbox/{m.id}\n"
        j_res = gpt.check_importance(
            json.dumps(
                {
                    "title": m.subject,
                    "from": m.sender,
                    "snippet": m.snippet,
                },
                ensure_ascii=False,
            )
        )

        # GPTが重要と判断したら通知
        if j_res.is_important:
            message += f"{m.snippet}\n"
            message += f"\n通知理由: {j_res.reason}"
            line.notify_message(message)
        else:
            print("skip notify", j_res.all_statements)
        time.sleep(1)
