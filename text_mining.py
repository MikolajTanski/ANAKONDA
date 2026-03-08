"""
Lab 5 – text mining + word cloud
Analizuje tytuły ogłoszeń: częstotliwość słów, n-gramy, word cloud.
"""

import logging
import os
import re
from collections import Counter

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from wordcloud import WordCloud

log = logging.getLogger(__name__)
PLOTS_DIR = "plots"

STOPWORDS_PL = {
    "do", "na", "w", "z", "i", "o", "a", "się", "że", "to", "nie",
    "jak", "po", "przy", "za", "od", "przez", "ale", "lub", "oraz",
    "już", "też", "dla", "co", "km", "ul", "m2", "zł", "pln",
    "ul", "al", "os", "nr", "we", "ze", "ku", "pod", "nad",
}


class TextCleaner:
    def clean(self, text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r"[^a-ząćęłńóśźż\s]", " ", text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 2 and t not in STOPWORDS_PL]


class FrequencyAnalyzer:
    def __init__(self):
        self.cleaner = TextCleaner()

    def word_freq(self, titles: pd.Series, top_n: int = 30) -> Counter:
        all_tokens = []
        for title in titles.dropna():
            all_tokens.extend(self.cleaner.clean(str(title)))
        return Counter(all_tokens).most_common(top_n)

    def bigrams(self, titles: pd.Series, top_n: int = 20) -> list[tuple]:
        all_tokens = []
        for title in titles.dropna():
            tokens = self.cleaner.clean(str(title))
            all_tokens.extend(zip(tokens, tokens[1:]))
        return Counter(all_tokens).most_common(top_n)


class TextVisualizer:
    def __init__(self):
        os.makedirs(PLOTS_DIR, exist_ok=True)

    def _save(self, name: str):
        path = os.path.join(PLOTS_DIR, name)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        log.info("Zapisano wykres: %s", path)

    def wordcloud(self, titles: pd.Series):
        cleaner = TextCleaner()
        all_tokens = []
        for title in titles.dropna():
            all_tokens.extend(cleaner.clean(str(title)))
        text = " ".join(all_tokens)

        wc = WordCloud(
            width=1200, height=600,
            background_color="white",
            colormap="Blues",
            max_words=150,
            collocations=False,
        ).generate(text)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("Word Cloud – tytuły ogłoszeń Otodom", fontsize=14, pad=12)
        self._save("06_wordcloud.png")

    def top_words_bar(self, freq: list[tuple]):
        words, counts = zip(*freq)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(words[::-1], counts[::-1], color="#1565C0")
        ax.set_title("Top 30 słów w tytułach ogłoszeń")
        ax.set_xlabel("Liczba wystąpień")
        self._save("07_top_words.png")

    def top_bigrams_bar(self, bigrams: list[tuple]):
        labels = [f"{a} {b}" for (a, b), _ in bigrams]
        counts = [c for _, c in bigrams]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(labels[::-1], counts[::-1], color="#0D47A1")
        ax.set_title("Top 20 bigramów w tytułach ogłoszeń")
        ax.set_xlabel("Liczba wystąpień")
        self._save("08_top_bigrams.png")


def run_text_mining(df: pd.DataFrame):
    analyzer = FrequencyAnalyzer()
    visualizer = TextVisualizer()

    freq = analyzer.word_freq(df["title"], top_n=30)
    bigrams = analyzer.bigrams(df["title"], top_n=20)

    log.info("Top 10 słów: %s", freq[:10])
    log.info("Top 5 bigramów: %s", bigrams[:5])

    visualizer.wordcloud(df["title"])
    visualizer.top_words_bar(freq)
    visualizer.top_bigrams_bar(bigrams)

    log.info("Text mining zakończony.")
