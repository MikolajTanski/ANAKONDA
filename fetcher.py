import json
import logging

import requests
from bs4 import BeautifulSoup

from config import Config

log = logging.getLogger(__name__)


class OtodomFetcher:
    """Pobiera strony z Otodom i zwraca surowy __NEXT_DATA__ JSON."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    def fetch(self, url: str) -> dict | None:
        try:
            resp = self.session.get(url, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            log.error("Błąd requestu %s: %s", url, e)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        tag = soup.find("script", id="__NEXT_DATA__")
        if not tag:
            log.warning("Brak __NEXT_DATA__ na stronie: %s", url)
            return None

        try:
            return json.loads(tag.string)
        except json.JSONDecodeError as e:
            log.error("Błąd parsowania JSON: %s", e)
            return None

    def page_url(self, page: int) -> str:
        if page == 1:
            return self.config.BASE_URL
        return f"{self.config.BASE_URL}?page={page}"
