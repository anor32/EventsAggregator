import os

from dotenv import load_dotenv

load_dotenv()
EVENTS_API_KEY = os.getenv("EVENTS_API_KEY")
# CLIENT_HOST = 'http://events-provider.dev-2.python-labs.ru'
CLIENT_HOST = "http://student-system-events-provider-web.student-system-events-provider.svc:8000"
