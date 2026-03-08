# Wyniki analizy – opis wykresów

Wszystkie wykresy generowane są do katalogu `plots/` po uruchomieniu `python main.py`.

---

## Lab 6 – Pandas + Matplotlib

### 01_price_distribution.png
Histogram rozkładu cen ogłoszeń (w tys. PLN). Pokazuje, że większość mieszkań wyceniona jest między 300k a 900k PLN, z długim ogonem w stronę droższych nieruchomości.

### 02_price_per_m2_by_city.png
Poziomy wykres słupkowy – mediana ceny za m² dla 10 najdroższych miast w Polsce. Pozwala szybko porównać rynki lokalne.

### 03_area_vs_price.png
Wykres punktowy: powierzchnia (m²) vs cena (tys. PLN). Punkty kolorowane wg ceny za m² (żółty = tani, czerwony = drogi). Widoczna liniowa korelacja z wyraźnym rozrzutem dla lokalizacji premium.

### 04_rooms_distribution.png
Wykres słupkowy liczby ogłoszeń wg liczby pokoi. Dominują mieszkania 2- i 3-pokojowe.

### 05_price_by_rooms.png
Wykres pudełkowy (box plot) ceny wg liczby pokoi (1–4). Obrazuje mediany i rozrzut cen w każdej kategorii bez wartości odstających.

---

## Lab 5 – Text Mining + Word Cloud

### 06_wordcloud.png
Chmura słów wygenerowana z tytułów ogłoszeń po usunięciu stop words. Dominują: *mieszkanie*, *pokoje*, *balkon*, *centrum*, *apartament*.

### 07_top_words.png
Poziomy wykres słupkowy – 30 najczęściej występujących słów w tytułach ogłoszeń.

### 08_top_bigrams.png
20 najczęstszych bigramów (par słów) w tytułach, np. *"pokojowe mieszkanie"*, *"bez prowizji"*, *"mieszkanie balkon"*.

---

## Lab 4 – Uczenie maszynowe

Modele przewidują cenę mieszkania na podstawie cech: powierzchnia, liczba pokoi, piętro, wskaźnik cenowy miasta, prywatny/agencja.

### 09_actual_vs_predicted.png
Trzy wykresy punktowe (jeden na model) porównujące rzeczywistą cenę z przewidywaną. Im bliżej czerwonej linii 45°, tym lepszy model. Widać, że Random Forest radzi sobie najlepiej.

### 10_model_comparison.png
Porównanie trzech modeli (Linear Regression, Random Forest, Gradient Boosting) na dwóch metrykach: MAE (błąd bezwzględny w tys. PLN) oraz R² (dopasowanie modelu, im bliżej 1 tym lepiej).

| Model | MAE | R² |
|---|---|---|
| Linear Regression | ~257k PLN | 0.49 |
| Random Forest | ~178k PLN | 0.69 |
| Gradient Boosting | ~183k PLN | 0.63 |

### 11_feature_importance.png
Ważność cech dla najlepszego modelu (Random Forest). Pokazuje, które zmienne najbardziej wpływają na przewidywaną cenę — dominuje powierzchnia i poziom cenowy miasta.
