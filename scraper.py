import time
import random
import logging

from config import Config
from fetcher import OtodomFetcher
from parser import OtodomParser
from storage import MongoStorage

log = logging.getLogger(__name__)


class OtodomScraper:
    """Orkiestruje cały proces scrapingu."""

    def __init__(self, config: Config):
        self.config = config
        self.fetcher = OtodomFetcher(config)
        self.parser = OtodomParser()
        self.storage = MongoStorage(config)

    def run(self):
        total_inserted = total_updated = 0
        total_pages = None
        page = 1

        while True:
            url = self.fetcher.page_url(page)
            log.info("Strona %d → %s", page, url)

            next_data = self.fetcher.fetch(url)
            if not next_data:
                log.error("Przerywam – brak danych na stronie %d", page)
                break

            if page == 1:
                total_pages = self.parser.get_total_pages(next_data)
                if self.config.MAX_PAGES:
                    total_pages = min(total_pages, self.config.MAX_PAGES)
                log.info("Łącznie stron: %d", total_pages)

            listings = self.parser.extract_listings(next_data)
            log.info("  Znalezione ogłoszenia: %d", len(listings))

            inserted, updated = self.storage.save(listings)
            total_inserted += inserted
            total_updated += updated
            log.info("  Zapisano: +%d nowych, %d zaktualizowanych", inserted, updated)

            if page >= total_pages:
                log.info("Osiągnięto ostatnią stronę (%d).", total_pages)
                break

            page += 1
            delay = random.uniform(self.config.DELAY_MIN, self.config.DELAY_MAX)
            log.info("  Czekam %.1f s...", delay)
            time.sleep(delay)

        log.info("Gotowe. Łącznie nowych: %d, zaktualizowanych: %d", total_inserted, total_updated)
