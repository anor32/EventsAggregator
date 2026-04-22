from app.setings.config import EVENTS_API_KEY


class EventsProviderClient:
    base_url = "http://events-provider.dev-2.python-labs.ru"
    headers = {"x-api-key": EVENTS_API_KEY}
