# Wyniki analizy – opis wykresów

Wszystkie wykresy generowane są do katalogu `plots/` po uruchomieniu `python main.py`.

---

## Lab 6 – Pandas + Matplotlib

### Rozkład cen ogłoszeń
![price distribution](plots/01_price_distribution.png)
Większość mieszkań wyceniona jest między 300k a 900k PLN, z długim ogonem w stronę droższych nieruchomości.

---

### Mediana ceny za m² – top 10 miast
![price per m2 by city](plots/02_price_per_m2_by_city.png)
Porównanie mediany ceny za m² dla 10 najdroższych rynków lokalnych w Polsce.

---

### Powierzchnia a cena
![area vs price](plots/03_area_vs_price.png)
Wykres punktowy z kolorowaniem wg ceny za m² (żółty = tani, czerwony = drogi). Widoczna liniowa korelacja z rozrzutem dla lokalizacji premium.

---

### Rozkład liczby pokoi
![rooms distribution](plots/04_rooms_distribution.png)
Dominują mieszkania 2- i 3-pokojowe.

---

### Cena wg liczby pokoi (box plot)
![price by rooms](plots/05_price_by_rooms.png)
Mediany i rozrzut cen w każdej kategorii pokoi, bez wartości odstających.

---

## Lab 5 – Text Mining + Word Cloud

### Word Cloud
![wordcloud](plots/06_wordcloud.png)
Chmura słów z tytułów ogłoszeń po usunięciu stop words. Dominują: *mieszkanie*, *pokoje*, *balkon*, *centrum*, *apartament*.

---

### Top 30 słów
![top words](plots/07_top_words.png)
Najczęściej występujące słowa w tytułach ogłoszeń.

---

### Top 20 bigramów
![top bigrams](plots/08_top_bigrams.png)
Najczęstsze pary słów, np. *"pokojowe mieszkanie"*, *"bez prowizji"*, *"mieszkanie balkon"*.

---

## Lab 4 – Uczenie maszynowe

Modele przewidują cenę mieszkania na podstawie: powierzchnia, liczba pokoi, piętro, wskaźnik cenowy miasta, prywatny/agencja.

### Rzeczywista vs przewidywana cena
![actual vs predicted](plots/09_actual_vs_predicted.png)
Im bliżej czerwonej linii 45°, tym lepszy model. Random Forest radzi sobie najlepiej.

---

### Porównanie modeli
![model comparison](plots/10_model_comparison.png)

| Model | MAE | R² |
|---|---|---|
| Linear Regression | ~257k PLN | 0.49 |
| Random Forest | ~178k PLN | 0.69 |
| Gradient Boosting | ~183k PLN | 0.63 |

---

### Ważność cech (Random Forest)
![feature importance](plots/11_feature_importance.png)
Powierzchnia i poziom cenowy miasta mają największy wpływ na przewidywaną cenę.
