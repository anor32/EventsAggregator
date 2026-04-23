import os

from dotenv import load_dotenv

load_dotenv()
EVENTS_API_KEY = os.getenv("EVENTS_API_KEY")
