"""
Pipeline:
  Lab2 (scraping) → Lab1 (MongoDB) → Lab6 (pandas/matplotlib)
                                    → Lab5 (text mining/wordcloud)
                                    → Lab4 (machine learning)

Uruchomienie pełne:   python main.py
Tylko analiza:        python main.py --skip-scraping
"""

import argparse
import logging

from config import Config
from scraper import OtodomScraper
from analysis import run_analysis
from text_mining import run_text_mining
from ml import run_ml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-scraping", action="store_true",
                        help="Pomiń scraping, użyj danych już w bazie")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = Config()

    # Lab 2 + Lab 1: scraping → MongoDB
    if not args.skip_scraping:
        log.info("=== LAB 2 + LAB 1: Scraping → MongoDB ===")
        OtodomScraper(config).run()

    # Lab 6: pandas + matplotlib
    log.info("=== LAB 6: Analiza danych (pandas + matplotlib) ===")
    df = run_analysis(config)

    # Lab 5: text mining + word cloud
    log.info("=== LAB 5: Text mining + Word Cloud ===")
    run_text_mining(df)

    # Lab 4: machine learning
    log.info("=== LAB 4: Uczenie maszynowe ===")
    run_ml(df)

    log.info("Gotowe. Wykresy zapisane w katalogu plots/")
