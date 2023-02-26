import os
import functions_framework
from dotenv import load_dotenv

load_dotenv()

from src import uscase


@functions_framework.http
def hello_http(request):
    new_mails = uscase.get_non_existing_mails()
    uscase.save_mails(new_mails)
    uscase.notify_new_mails(new_mails)
    return "ok"


load_dotenv(".env.local")

if os.environ.get("APP_ENV") == "local":
    hello_http(None)
