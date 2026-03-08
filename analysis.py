"""
Lab 6 – pandas + matplotlib
Ładuje dane z MongoDB, liczy statystyki i zapisuje wykresy do plots/
"""

import logging
import os

import pandas as pd
import matplotlib; matplotlib.use("Agg")  # noqa: E702
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from config import Config
from storage import MongoStorage

log = logging.getLogger(__name__)
PLOTS_DIR = "plots"


class DataLoader:
    """Ładuje kolekcję MongoDB do pandas DataFrame."""

    def __init__(self, config: Config):
        self.storage = MongoStorage(config)

    def load(self) -> pd.DataFrame:
        docs = list(self.storage.collection.find({}, {"_id": 0}))
        df = pd.DataFrame(docs)
        log.info("Załadowano %d rekordów z MongoDB", len(df))
        return df


class DataAnalyzer:
    """Czyści dane i liczy podstawowe statystyki."""

    ROOMS_MAP = {
        "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4,
        "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8,
        "NINE": 9, "TEN": 10,
    }

    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        if "rooms" in df.columns:
            df["rooms"] = df["rooms"].map(self.ROOMS_MAP).fillna(
                pd.to_numeric(df["rooms"], errors="coerce")
            )

        numeric = ["price", "price_per_m2", "area", "floor"]
        for col in numeric:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df[df["price"] > 10_000]
        df = df[df["area"] > 5]
        df = df[df["price"] < 20_000_000]
        return df.reset_index(drop=True)

    def summary(self, df: pd.DataFrame):
        log.info("\n%s", df[["price", "price_per_m2", "area", "rooms"]].describe().to_string())

    def top_cities(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        return (
            df.groupby("location_city")["price_per_m2"]
            .median()
            .dropna()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )


class PlotGenerator:
    """Generuje i zapisuje wykresy matplotlib."""

    def __init__(self):
        os.makedirs(PLOTS_DIR, exist_ok=True)
        plt.rcParams["figure.dpi"] = 120
        plt.rcParams["font.size"] = 10

    def _save(self, name: str):
        path = os.path.join(PLOTS_DIR, name)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        log.info("Zapisano wykres: %s", path)

    def price_distribution(self, df: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(8, 4))
        data = df["price"].dropna() / 1_000
        ax.hist(data, bins=60, color="#2196F3", edgecolor="white", linewidth=0.4)
        ax.set_title("Rozkład cen ogłoszeń")
        ax.set_xlabel("Cena (tys. PLN)")
        ax.set_ylabel("Liczba ogłoszeń")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}k"))
        self._save("01_price_distribution.png")

    def price_per_m2_by_city(self, top_cities: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(9, 5))
        colors = plt.cm.Blues_r(range(50, 200, int(150 / len(top_cities))))
        bars = ax.barh(top_cities["location_city"], top_cities["price_per_m2"], color=colors)
        ax.set_title("Mediana ceny za m² – top 10 miast")
        ax.set_xlabel("PLN / m²")
        ax.bar_label(bars, fmt="%.0f", padding=4)
        ax.invert_yaxis()
        self._save("02_price_per_m2_by_city.png")

    def area_vs_price(self, df: pd.DataFrame):
        pool = df[df["area"] < 200]
        sample = pool.sample(min(500, len(pool)), random_state=42)
        fig, ax = plt.subplots(figsize=(8, 5))
        sc = ax.scatter(
            sample["area"], sample["price"] / 1_000,
            alpha=0.35, s=12, c=sample["price_per_m2"],
            cmap="YlOrRd", vmin=3000, vmax=20000,
        )
        plt.colorbar(sc, ax=ax, label="PLN/m²")
        ax.set_title("Powierzchnia a cena")
        ax.set_xlabel("Powierzchnia (m²)")
        ax.set_ylabel("Cena (tys. PLN)")
        self._save("03_area_vs_price.png")

    def rooms_distribution(self, df: pd.DataFrame):
        counts = df["rooms"].value_counts().sort_index()
        counts = counts[counts.index.isin([1, 2, 3, 4, 5, 6])]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(counts.index.astype(str), counts.values, color="#4CAF50", edgecolor="white")
        ax.set_title("Rozkład liczby pokoi")
        ax.set_xlabel("Liczba pokoi")
        ax.set_ylabel("Liczba ogłoszeń")
        self._save("04_rooms_distribution.png")

    def price_by_rooms(self, df: pd.DataFrame):
        data = [
            df[df["rooms"] == r]["price"].dropna().values / 1_000
            for r in [1, 2, 3, 4]
        ]
        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(data, labels=["1 pokój", "2 pokoje", "3 pokoje", "4 pokoje"],
                        patch_artist=True, showfliers=False)
        colors = ["#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5"]
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
        ax.set_title("Cena wg liczby pokoi")
        ax.set_ylabel("Cena (tys. PLN)")
        self._save("05_price_by_rooms.png")


def run_analysis(config: Config):
    loader = DataLoader(config)
    df_raw = loader.load()

    analyzer = DataAnalyzer()
    df = analyzer.prepare(df_raw)
    analyzer.summary(df)
    top_cities = analyzer.top_cities(df)

    plots = PlotGenerator()
    plots.price_distribution(df)
    plots.price_per_m2_by_city(top_cities)
    plots.area_vs_price(df)
    plots.rooms_distribution(df)
    plots.price_by_rooms(df)

    log.info("Analiza zakończona. Wykresy w katalogu: %s/", PLOTS_DIR)
    return df
