"""
Lab 4 – uczenie maszynowe
Regresja ceny mieszkania na podstawie: powierzchnia, pokoje, piętro, miasto.
"""

import logging

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

log = logging.getLogger(__name__)
PLOTS_DIR = "plots"


class FeatureEngineer:
    """Przygotowuje cechy do modelu ML."""

    def __init__(self):
        self.city_encoder = LabelEncoder()

    def prepare(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        features = ["area", "rooms", "floor", "location_city", "is_private", "price_per_m2"]
        target = "price"

        ROOMS_MAP = {
            "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4,
            "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8,
        }

        data = df[features + [target]].copy()
        data["rooms"] = data["rooms"].map(ROOMS_MAP).fillna(
            pd.to_numeric(data["rooms"], errors="coerce")
        )
        data = data.dropna(subset=["area", "price"])

        data["floor"] = pd.to_numeric(data["floor"], errors="coerce").fillna(0)
        data["rooms"] = data["rooms"].fillna(data["rooms"].median())
        data["is_private"] = data["is_private"].fillna(False).astype(int)

        # Kodowanie miasta jako liczba (mediana ceny/m2 dla miasta)
        city_median = df.groupby("location_city")["price_per_m2"].median()
        data["city_price_level"] = data["location_city"].map(city_median).fillna(city_median.median())
        data = data.drop(columns=["location_city", "price_per_m2"])

        X = data.drop(columns=[target])
        y = data[target]
        return X, y


class PricePredictor:
    """Trenuje i porównuje modele regresji."""

    MODELS = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    def train_and_evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        results = {}
        for name, model in self.MODELS.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            cv = cross_val_score(model, X, y, cv=5, scoring="r2").mean()
            results[name] = {
                "model": model, "y_test": y_test, "y_pred": y_pred,
                "MAE": mae, "R2": r2, "CV_R2": cv,
            }
            log.info("%-22s MAE=%8.0f PLN  R²=%.3f  CV_R²=%.3f", name, mae, r2, cv)
        return results

    def feature_importance(self, model, feature_names: list) -> pd.Series:
        if hasattr(model, "feature_importances_"):
            return pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
        return pd.Series()


class MLVisualizer:
    def __init__(self):
        os.makedirs(PLOTS_DIR, exist_ok=True)

    def _save(self, name: str):
        path = os.path.join(PLOTS_DIR, name)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        log.info("Zapisano wykres: %s", path)

    def actual_vs_predicted(self, results: dict):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, (name, r) in zip(axes, results.items()):
            sample_idx = np.random.choice(len(r["y_test"]), min(400, len(r["y_test"])), replace=False)
            y_t = np.array(r["y_test"])[sample_idx] / 1_000
            y_p = np.array(r["y_pred"])[sample_idx] / 1_000
            ax.scatter(y_t, y_p, alpha=0.3, s=10, color="#1976D2")
            lim = max(y_t.max(), y_p.max())
            ax.plot([0, lim], [0, lim], "r--", linewidth=1)
            ax.set_title(f"{name}\nR²={r['R2']:.3f}, MAE={r['MAE']/1000:.0f}k PLN")
            ax.set_xlabel("Rzeczywista cena (tys.)")
            ax.set_ylabel("Przewidywana cena (tys.)")
        fig.suptitle("Rzeczywista vs przewidywana cena", fontsize=13, y=1.02)
        self._save("09_actual_vs_predicted.png")

    def model_comparison(self, results: dict):
        names = list(results.keys())
        maes = [r["MAE"] / 1000 for r in results.values()]
        r2s = [r["R2"] for r in results.values()]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.bar(names, maes, color=["#EF5350", "#42A5F5", "#66BB6A"])
        ax1.set_title("MAE modeli (tys. PLN)")
        ax1.set_ylabel("MAE (tys. PLN)")

        ax2.bar(names, r2s, color=["#EF5350", "#42A5F5", "#66BB6A"])
        ax2.set_title("R² modeli")
        ax2.set_ylabel("R²")
        ax2.set_ylim(0, 1)
        self._save("10_model_comparison.png")

    def feature_importance_plot(self, importance: pd.Series, model_name: str):
        if importance.empty:
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        importance.plot(kind="bar", ax=ax, color="#1565C0")
        ax.set_title(f"Ważność cech – {model_name}")
        ax.set_ylabel("Importance")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
        self._save("11_feature_importance.png")


def run_ml(df: pd.DataFrame):
    engineer = FeatureEngineer()
    X, y = engineer.prepare(df)
    log.info("Dane do ML: %d próbek, %d cech: %s", len(X), len(X.columns), list(X.columns))

    predictor = PricePredictor()
    results = predictor.train_and_evaluate(X, y)

    visualizer = MLVisualizer()
    visualizer.actual_vs_predicted(results)
    visualizer.model_comparison(results)

    best_name = max(results, key=lambda k: results[k]["R2"])
    best_model = results[best_name]["model"]
    importance = predictor.feature_importance(best_model, list(X.columns))
    visualizer.feature_importance_plot(importance, best_name)

    log.info("Najlepszy model: %s (R²=%.3f)", best_name, results[best_name]["R2"])
    log.info("ML zakończone.")
