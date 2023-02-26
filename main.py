from dotenv import load_dotenv

load_dotenv()
from src import uscase

new_mails = uscase.get_non_existing_mails()
uscase.save_mails(new_mails)
uscase.notify_new_mails(new_mails)
