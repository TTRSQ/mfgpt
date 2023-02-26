import time
from src.adapter import gpt

mails = [
    "メールの内容",
]

for mail in mails:
    res = gpt.check_importance(mail)
    print("入力:", mail)
    print("出力:", res)
    print()
    time.sleep(1)
