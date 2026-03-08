# Omówienie wyników analizy

> Wykresy: [readme_wyniki.md](readme_wyniki.md)

---

## Lab 6 – Pandas + Matplotlib

### 01. Rozkład cen ogłoszeń
Rozkład jest prawostronnie skośny — większość ogłoszeń skupia się w przedziale 300–900 tys. PLN, a mediana wynosi ok. 610 tys. PLN. Długi ogon po prawej stronie odpowiada nieruchomościom premium (powyżej 2 mln PLN), które zaburzają średnią i stanowią mniejszość rynku.

### 02. Mediana ceny za m² – top 10 miast
Warszawa i największe aglomeracje dominują pod względem ceny za m². Różnice między miastami są znaczące — stolica potrafi być 2–3x droższa od mniejszych ośrodków. Wykres potwierdza silną korelację między wielkością rynku pracy a ceną nieruchomości.

### 03. Powierzchnia a cena
Widoczna liniowa korelacja — większe mieszkania są droższe. Kolor punktów (cena/m²) pokazuje, że małe mieszkania w drogich lokalizacjach mogą być droższe per m² niż duże mieszkania na peryferiach. Rozrzut dla mieszkań powyżej 100 m² jest bardzo duży, co świadczy o silnym wpływie lokalizacji i standardu wykończenia.

### 04. Rozkład liczby pokoi
Zdecydowana dominacja mieszkań 2- i 3-pokojowych, które stanowią łącznie ok. 70% oferty. Kawalerki i mieszkania 4+ pokojowe są wyraźnie rzadsze. To odzwierciedla typową strukturę budownictwa mieszkaniowego w Polsce.

### 05. Cena wg liczby pokoi (box plot)
Mediana ceny rośnie wraz z liczbą pokoi, jednak rozrzut (IQR) jest coraz większy. Mieszkania 3-pokojowe mają największy zakres cenowy — od mieszkań przystępnych po luksusowe apartamenty. Mediany: 1 pokój ~400k, 2 pokoje ~550k, 3 pokoje ~700k, 4 pokoje ~900k PLN.

---

## Lab 5 – Text Mining + Word Cloud

### 06. Word Cloud
Dominujące słowa to *mieszkanie*, *pokoje*, *balkon*, *centrum* i *apartament*. Duża widoczność słów takich jak *prowizji* (bez prowizji) i *ogródek* wskazuje na popularne atrybuty w tytułach. Słowo *nowe* pojawia się często, co sugeruje dużą podaż nowego budownictwa.

### 07. Top 30 słów
Najczęstsze słowo to *mieszkanie* (386 wystąpień) — co naturalne przy scrapiegu mieszkań. Wysoka częstość *balkon* (100), *centrum* (66) i *nowe* (60) potwierdza, że sprzedający eksponują te cechy jako kluczowe atuty. Fraza *bez prowizji* (pośrednio przez *prowizji* — 68) wskazuje na dużą liczbę ofert od prywatnych sprzedających.

### 08. Top 20 bigramów
Najczęstszy bigram to *"pokojowe mieszkanie"* (150 wystąpień), co wynika ze standardowego formatu tytułu (np. "3-pokojowe mieszkanie"). *"Bez prowizji"* (55) potwierdza obserwację z top słów. *"Mieszkanie balkon"* (43) i *"mieszkanie ogródek"* (30) to cechy, które sprzedający szczególnie podkreślają w tytułach.

---

## Lab 4 – Uczenie maszynowe

### 09. Rzeczywista vs przewidywana cena
Wszystkie trzy modele mają tendencję do niedoszacowania cen w segmencie premium (powyżej 1.5 mln PLN) — wynika to z małej liczby takich próbek w zbiorze. Random Forest najlepiej "trzyma się" linii idealnej, szczególnie w przedziale 300k–1.2 mln PLN. Linear Regression wyraźnie odstaje dla tanich i drogich nieruchomości (model liniowy nie radzi sobie z nieliniowymi zależnościami).

### 10. Porównanie modeli

| Model | MAE | R² | Interpretacja |
|---|---|---|---|
| Linear Regression | ~257k PLN | 0.49 | Słabe — model liniowy nie wychwytuje nieliniowych zależności ceny |
| Random Forest | ~178k PLN | 0.69 | Najlepszy — dobrze radzi sobie z interakcjami między cechami |
| Gradient Boosting | ~183k PLN | 0.63 | Dobry, ale na małym zbiorze (956 próbek) przegrywa z RF |

Random Forest jest najlepszym modelem — niższy MAE o ~80k PLN względem regresji liniowej i wyższy R² o 0.20. Relatywnie niskie R² (max 0.69) sugeruje, że duża część zmienności cen zależy od cech których nie scrapeujemy (stan wykończenia, rok budowy, dokładna lokalizacja w mieście).

### 11. Ważność cech (Random Forest)
Dwie cechy dominują: **powierzchnia** i **city_price_level** (mediana ceny/m² w danym mieście). Razem odpowiadają za ok. 85% siły predykcji modelu. Liczba pokoi i piętro mają marginalny wpływ — wynika to z faktu, że te cechy są silnie skorelowane z powierzchnią. Zmienna *is_private* (prywatny vs agencja) ma pomijalny wpływ na cenę.
