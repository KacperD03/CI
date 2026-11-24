# Plan Prezentacji i Przewodnik Czytania (Slajd po Slajdzie z Tłumaczeniem PL)

Ten dokument zawiera pełny scenariusz prezentowania zaktualizowanej prezentacji [`prezentacja.html`](file:///c:/Users/kedm2e/OneDrive%20-%20BWI/Pulpit/lab/prezentacja.html).
* Wszystkie formy zostały zmienione na **pojedynczą osobę („I / my / me”)**, ponieważ jest to Twój projekt indywidualny (*Solo Project*).
* Usunięto zapis o AI Disclosure.
* Harmonogram w slajdzie 5 ma neutralny wygląd.
* Slajdy 6 i 7 mają całkowicie **rozdzielone, unikalne teksty** pod tytułem i w pasku Takeaway.
* **Pod każdym zdaniem po angielsku znajduje się dokładne tłumaczenie po polsku**, żebyś dokładnie wiedział, co mówisz.

---

## 💡 Co to jest AULC (Area Under Learning Curve)? — Proste wytłumaczenie

Profesor może Cię zapytać: *„Co to jest AULC i po co to liczysz?”*. Oto prosta, konkretna odpowiedź:

### 1. Skąd się wzięło AULC?
* W klasycznym Machine Learningu trenujesz model na 100% danych i podajesz jedną liczbę: np. *Accuracy = 92%*.
* W **Active Learningu** chodzi o coś zupełnie innego: **jak szybko model uczy się przy jak najmniejszej liczbie oznaczonych próbek**.
* Dlatego w Active Learningu rysujemy **krzywą uczenia (Learning Curve)**:
  * **Oś pozioma (X):** liczba etykiet podanych modelowi (np. start od 20, potem 30, 40, 50... aż do 300).
  * **Oś pionowa (Y):** wynik modelu na zbiorze testowym (np. Macro F1-score od 0.5 do 1.0).

### 2. Co to dokładnie jest to „Area” (Pole)?
* **AULC to dosłownie pole powierzchni pod tą krzywą uczenia** (obliczane matematycznie prostą regułą trapezów i dzielone przez maksymalne możliwe pole, aby wynik wynosił od 0 do 1).
* **Intuicja:**
  * Jeśli metoda jest **sprytna** (np. *Margin Sampling*), wybiera trudne, kluczowe przypadki. Jej wynik natychmiast wystrzeliwuje w górę (np. już przy 80 próbkach ma F1 = 0.90). Krzywa jest wysoka przez cały czas, więc **pole pod nią (AULC) jest duże**.
  * Jeśli metoda jest **głupia/losowa** (*Random Sampling*), wybiera przypadkowe, powtarzające się punkty. Krzywa rośnie powoli i płasko, więc **pole pod nią (AULC) jest małe**.
* **Dlaczego to stosujemy?**
  Zamiast porównywać 29 osobnych liczb dla każdego kroku z osobna, **AULC podsumowuje całą skuteczność metody jedną, elegancką liczbą**. To standardowa metryka rekomendowana w najnowszym benchmarku **Lu et al. (TMLR 2025)**, na który powołujemy się na slajdzie 6 i 7.

---

## 🗣️ Słowniczek wymowy kluczowych pojęć
* **AULC** $\rightarrow$ mów po literach: *[ej – ju – el – si]*
* **Uncertainty Sampling** $\rightarrow$ *[an-ser-tyn-ti sam-pling]*
* **Query-By-Committee (QBC)** $\rightarrow$ mów skrótem: *[kju – bi – si]*
* **Holdout test set** $\rightarrow$ *[hold-ałt test set]* (odłożony, nienaruszony zbiór testowy)
* **StandardScaler** $\rightarrow$ *[standard skejler]*
* **Data leakage** $\rightarrow$ *[dejta li-kidż]* (wyciek danych)
* **Outliers** $\rightarrow$ *[ałt-laj-ers]* (błędy w danych / wartości odstające)
* **Hypothesis** $\rightarrow$ *[haj-po-te-sis]* (hipoteza)

---

# GŁÓWNY SCENARIUSZ: PREZENTACJA NA CLASS 3 (SLAJDY 6 I 7)

Jeśli na zajęciach prezentujesz tylko postęp na **Class 3 (Literature $\rightarrow$ Protocol)**, zaczynasz od razu od Slajdu 6. Wystarczy, że na start powiesz jedno krótkie zdanie wprowadzające.

---

## SLAJD 6: Literature Matrix: 3 Studied Papers

### KROK 1: Wstęp i zdanie pod tytułem (Curated Literature Selection)
> **Powiedz na start (wprowadzenie do Class 3):**
> *"Good morning. For Class 3, I am presenting my Literature Matrix and experimental protocol for my solo project on Active Learning."*  
> *(Dzień dobry. W ramach Class 3 przedstawiam macierz literatury oraz protokół eksperymentalny dla mojego indywidualnego projektu dotyczącego Active Learning.)*
>
> **Przeczytaj zdanie pod głównym tytułem slajdu:**
> *"Literature Selection: I selected 3 peer-reviewed papers spanning theoretical query foundations, multi-seed statistical benchmarks, and recent empirical evidence on tabular data."*  
> *(Dobór literatury: Wybrałem 3 recenzowane artykuły obejmujące teoretyczne podstawy zapytań, statystyczne benchmarki wielo-ziarnowe oraz najnowsze dowody empiryczne dla danych tabelarycznych.)*

### KROK 2: Przejdź przez 3 wiersze tabeli (czytasz kluczowe komórki)
> **Wiersz 1 — Settles (2010) [Anchor Paper]:**  
> *"First is my anchor survey by Burr Settles from 2010. It defines the pool-based loop and the math for Entropy, Margin, and QBC. Its main limitation is that Uncertainty Sampling can accidentally waste budget by picking noisy outliers near the boundary."*  
> *(Pierwszy to mój artykuł bazowy Burra Settlesa z 2010 roku. Definiuje on pętlę pool-based oraz matematykę dla Entropy, Margin i QBC. Jego głównym ograniczeniem jest to, że Uncertainty Sampling może marnować budżet, wybierając zaszumione wartości odstające blisko granicy decyzyjnej.)*
>
> **Wiersz 2 — Werner et al. (NeurIPS 2024):**  
> *"Second is Werner et al. from NeurIPS 2024. They benchmarked active learning across domains and proved that 1-seed runs are completely unreliable. This directly justifies why I run every experiment across 5 random seeds."*  
> *(Drugi to Werner i inni z NeurIPS 2024. Przetestowali active learning w różnych dziedzinach i udowodnili, że testy na 1 ziarnie losowym są całkowicie niewiarygodne. To bezpośrednio uzasadnia, dlaczego każdy eksperyment wykonuję na 5 ziarnach losowych.)*
>
> **Wiersz 3 — Lu et al. (TMLR 2025):**  
> *"Third is Lu et al. from TMLR 2025. They proved that on tabular data, classic Margin and Entropy Sampling consistently outperform complex deep methods. This directly supports my choice of methods, my use of AULC, and my outlier ablation tests."*  
> *(Trzeci to Lu i inni z TMLR 2025. Udowodnili, że na danych tabelarycznych klasyczne Margin i Entropy Sampling konsekwentnie wygrywają ze skomplikowanymi metodami głębokimi. To bezpośrednio potwierdza mój wybór metod, użycie metryki AULC oraz testy usuwania wartości odstających.)*

### KROK 3: FINAŁ SLAJDU 6 — Pasek Takeaway na dole
> **Przeczytaj pasek Takeaway:**
> *"Takeaway: Settles provides my math formulas, Werner proves 1-seed runs are unreliable, and Lu shows Margin Sampling beats complex deep models on tabular datasets."*  
> *(Wniosek: Settles dostarcza mi wzorów matematycznych, Werner dowodzi, że 1 ziarno losowe jest niewiarygodne, a Lu pokazuje, że Margin Sampling wygrywa ze złożonymi modelami głębokimi na zbiorach tabelarycznych.)*

---

## SLAJD 7: Class 3 Protocol: Hypothesis, Splits, Metrics & Comparisons

### KROK 1: Zdanie pod tytułem (Pre-Registered Benchmark)
> **Przeczytaj zdanie pod tytułem slajdu:**
> *"Controlled Benchmark: I lock all experimental parameters before running code — 330 holdout patients, 5 random seeds, zero data leakage, and 2 targeted stress tests."*  
> *(Kontrolowany benchmark: Blokuję wszystkie parametry eksperymentu przed uruchomieniem kodu — 330 odłożonych pacjentów testowych, 5 ziaren losowych, zero wycieku danych i 2 celowane testy warunków skrajnych.)*

### KROK 2: Kafel 1 (Refined Hypotheses) & Kafel 2 (Locked Splits)
> **Przeczytaj z Kafla 1 (lewy górny):**  
> *"In Box 1, my Refined Hypotheses: Main Claim H1 is that Margin, Entropy, and QBC will reach 95% of full-data Macro F1 using 30% to 40% fewer labels than Random Sampling. Outlier Claim H2 is that removing extreme errors like heart rate equals 1111 will improve Uncertainty Sampling in early steps."*  
> *(W ramce 1, moje doprecyzowane hipotezy: Główna hipoteza H1 zakłada, że Margin, Entropy i QBC osiągną 95% pełnego wyniku Macro F1 przy użyciu 30% do 40% mniejszej liczby etykiet niż losowe próbkowanie. Hipoteza H2 o wartościach odstających zakłada, że usunięcie skrajnych błędów, takich jak tętno równe 1111, poprawi działanie Uncertainty Sampling w początkowych krokach.)*
>
> **Przeczytaj z Kafla 2 (prawy górny):**  
> *"In Box 2, Locked Data Splits on 1,319 patients: The locked test set has 25% (330 rows), stratified and never touched during queries. The training pool has 75% (989 rows), starting with 20 balanced samples. Zero Leakage Rule: StandardScaler is fitted strictly on the currently labeled subset at each step."*  
> *(W ramce 2, zablokowany podział danych dla 1319 pacjentów: Zablokowany zbiór testowy to 25% (330 wierszy), stratyfikowany i nigdy niedotykany podczas zapytań. Pula treningowa to 75% (989 wierszy), zaczynając od 20 zbalansowanych próbek. Zasada braku wycieku: StandardScaler jest dopasowywany ściśle tylko na aktualnie oznaczonym podzbiorze w każdym kroku.)*

### KROK 3: Kafel 3 (Metrics & AULC) & Kafel 4 (Comparisons & Stress Tests)
> **Przeczytaj z Kafla 3 (lewy dolny):**  
> *"In Box 3, How I Measure Performance: I plot Learning Curves across 29 steps (from 20 to 300 labels). I calculate AULC as a single summary score of label efficiency, and I report Saved Labels over 5 random seeds."*  
> *(W ramce 3, jak mierzę wyniki: Wykreślam krzywe uczenia na przestrzeni 29 kroków (od 20 do 300 etykiet). Obliczam AULC jako pojedynczy wynik podsumowujący wydajność próbkowania i raportuję zaoszczędzone etykiety dla 5 ziaren losowych.)*
>
> **Przeczytaj z Kafla 4 (prawy dolny):**  
> *"In Box 4, my Comparison Plan: I compare Random Sampling and Full-Data against Entropy, Margin, and QBC. I also planned two stress tests: raw pool versus cleaned pool without impluse 1111, and full features versus removing troponin."*  
> *(W ramce 4, mój plan porównania: Porównuję Random Sampling oraz Full-Data z Entropy, Margin i QBC. Zaplanowałem również dwa testy warunków skrajnych: surowa pula kontra pula oczyszczona bez tętna 1111, oraz pełne cechy kontra usunięcie troponiny.)*

### KROK 4: FINAŁ CAŁEJ PREZENTACJI — Pasek Takeaway na dole
> **Przeczytaj pasek Takeaway na dole:**
> *"Takeaway: By freezing my test split and refitting scalers only on labeled subsets, I prevent data leakage completely and establish a reproducible benchmark for Class 4. Thank you!"*  
> *(Wniosek: Zamrażając zbiór testowy i dopasowując skalery wyłącznie na oznaczonych podzbiorach, całkowicie zapobiegam wyciekowi danych i tworzę w pełni powtarzalny benchmark gotowy do Class 4. Dziękuję!)*

---

# SCENARIUSZ UZUPEŁNIAJĄCY: SLAJDY 1–5 (PITCH)
*(Gdyby profesor poprosił Cię o pokazanie całości od początku)*

---

## SLAJD 1: Candidate Ideas & Selected Research Topic

* **Krok 1 (lewy niebieski kafel):**  
  *"My main topic tests if Active Learning (Uncertainty Sampling and Query-By-Committee) needs fewer labeled patients than passive Random Sampling on the Heart Attack Dataset. Main Goal: Save doctor labels and test if data errors trick the model. Fast Run: Runs on a normal laptop CPU in under 15 seconds."*  
  *(Mój główny temat sprawdza, czy Active Learning potrzebuje mniej oznaczonych pacjentów niż pasywne próbkowanie losowe na zbiorze Heart Attack. Główny cel: zaoszczędzić etykiety od lekarzy i sprawdzić, czy błędy w danych mylą model. Szybkie uruchomienie: działa na procesorze zwykłego laptopa w mniej niż 15 sekund.)*
* **Krok 2 (pasek Takeaway na dole):**  
  *"In short: I choose Active Learning because doctor annotations are expensive, and I want high accuracy with fewer labels."*  
  *(Krótko mówiąc: Wybieram Active Learning, ponieważ adnotacje lekarskie są drogie, a chcę wysokiej dokładności przy mniejszej liczbie etykiet.)*
* **Krok 3 (prawy kafel — My Tasks):**  
  *"My Tasks: Check the dataset, build the active learning loop, test 4 methods across 5 random seeds, and run outlier tests."*  
  *(Moje zadania: Sprawdzić zbiór danych, zbudować pętlę uczenia aktywnego, przetestować 4 metody na 5 ziarnach losowych i przeprowadzić testy wartości odstających.)*
* **Krok 4 (dolne kafle):**  
  *"Candidate 2 is my backup idea: Learning with Noisy Labels. And Candidate 3 — Comparing Optimizers — was discarded."*  
  *(Kandydat 2 to mój pomysł rezerwowy: Uczenie z zaszumionymi etykietami. A kandydat 3 — Porównanie optymalizatorów — został odrzucony.)*
* **Krok 5 (zdanie pod tytułem na górze):**  
  *"Simple comparison: Idea 1 saves expensive medical labels, while Idea 2 (noisy labels) and Idea 3 (optimizers) are less practical for clinical data."*  
  *(Proste porównanie: Pomysł 1 oszczędza drogie etykiety medyczne, podczas gdy pomysł 2 i 3 są mniej praktyczne dla danych klinicznych.)*

---

## SLAJD 2: Research Question, Hypothesis & Motivation

* **Krok 1 (górny niebieski kafel):**  
  *"Research Question: How many labeled examples can I save by using Active Learning (Uncertainty Sampling and Query-By-Committee) compared to passive Random Sampling to reach the same accuracy on heart attack data?"*  
  *(Pytanie badawcze: Ile oznaczonych przykładów mogę zaoszczędzić, stosując Active Learning w porównaniu z pasywnym próbkowaniem losowym, aby osiągnąć tę samą dokładność na danych o zawałach serca?)*
* **Krok 2 (pasek Takeaway na dole):**  
  *"Takeaway: The main goal is not to build a complex model, but to reach the same medical accuracy with much less labeled data."*  
  *(Wniosek: Głównym celem nie jest budowa skomplikowanego modelu, lecz osiągnięcie tej samej dokładności medycznej przy znacznie mniejszej ilości oznaczonych danych.)*
* **Krok 3 (prawy kafel — Motivation):**  
  *"First, High Labeling Cost: Collecting raw blood tests is cheap, but paying doctors to diagnose and label cases is slow and expensive. Second, Smarter Data Choice: Instead of building a bigger model, I let a simple model choose which patients are most useful to label next."*  
  *(Po pierwsze, wysoki koszt etykietowania: Zebranie surowych badań krwi jest tanie, ale płacenie lekarzom za diagnozę i etykietowanie jest powolne i drogie. Po drugie, mądrzejszy wybór danych: Zamiast budować większy model, pozwalam prostemu modelowi wybrać, których pacjentów najbardziej warto oznaczyć w następnej kolejności.)*
* **Krok 4 (lewy kafel — Hypothesis):**  
  *"Hypothesis: I Expect 30% to 40% Saved Labels. If the model picks only the most uncertain patients near the 50/50 boundary, it will reach 95% of full-data score using 30% to 40% fewer labels. When can this fail? If Active Learning picks extreme outliers instead of real borderline patients."*  
  *(Hipoteza: Oczekuję od 30% do 40% zaoszczędzonych etykiet. Jeśli model wybiera tylko najbardziej niepewnych pacjentów blisko granicy 50/50, osiągnie 95% pełnego wyniku przy 30% do 40% mniejszej liczbie etykiet. Kiedy to może zawieść? Jeśli Active Learning wybierze skrajne wartości odstające zamiast prawdziwych pacjentów granicznych.)*
* **Krok 5 (zdanie pod tytułem na górze):**  
  *"Core comparison: Passive learning asks for labels blindly, while Active Learning asks only about the hardest 50/50 borderline cases."*  
  *(Kluczowe porównanie: Pasywne uczenie prosi o etykiety na ślepo, podczas gdy Active Learning pyta tylko o najtrudniejsze, graniczne przypadki 50/50.)*

---

## SLAJD 3: Anchor Paper & Candidate Dataset

* **Krok 1 (lewy niebieski kafel — Anchor Paper):**  
  *"On the left is my anchor paper by Burr Settles (2010). Main Idea: A model reaches high accuracy with much fewer labels if it can choose which unlabeled data points to ask about next. 3 Methods I Take From This Paper: Pool-Based Loop, Uncertainty Sampling, and Query-By-Committee."*  
  *(Po lewej jest mój artykuł bazowy Burra Settlesa z 2010 roku. Główna myśl: Model osiąga wysoką dokładność przy znacznie mniejszej liczbie etykiet, jeśli może sam wybrać, o które nieoznaczone punkty zapytać w następnym kroku. 3 metody, które biorę z tego artykułu: pętla Pool-Based, Uncertainty Sampling oraz Query-By-Committee.)*
* **Krok 2 (prawy kafel — Dataset):**  
  *"On the right is my dataset from Kaggle: 1,319 Patients, 8 Clinical Features (7 numerical and 1 binary gender), and 61.4% Positive Cases with zero missing values. Important finding: The table contains real measurement errors — heart rate equals 1111 in 3 rows — and strong markers like troponin. This lets me test if outliers trick Active Learning!"*  
  *(Po prawej jest mój zbiór danych z Kaggle: 1319 pacjentów, 8 cech klinicznych (7 numerycznych i 1 binarna płeć) oraz 61.4% przypadków pozytywnych przy zerze brakujących wartości. Ważne odkrycie: Tabela zawiera prawdziwe błędy pomiarowe — tętno równe 1111 w 3 wierszach — oraz silne markery, takie jak troponina. To pozwala mi sprawdzić, czy błędy w danych mylą Active Learning!)*
* **Krok 3 (pasek Takeaway na dole):**  
  *"Takeaway: I combine classic Active Learning methods from Settles with a real 1,319-patient dataset that contains both strong signals and noisy outliers."*  
  *(Wniosek: Łączę klasyczne metody Active Learning od Settlesa z prawdziwym zbiorem 1319 pacjentów, który zawiera zarówno silne sygnały, jak i zaszumione wartości odstające.)*
* **Krok 4 (zdanie pod tytułem na górze):**  
  *"Theory vs. Practice: Settles (2010) provides the mathematical query methods, and my 1,319-patient dataset lets me test them on real clinical data."*  
  *(Teoria a praktyka: Settles dostarcza matematycznych metod zapytań, a mój zbiór 1319 pacjentów pozwala mi przetestować je na prawdziwych danych klinicznych.)*

---

## SLAJD 4: Baselines, Active Methods & Fair Protocol

* **Krok 1 (zdanie pod tytułem na górze):**  
  *"Fair comparison: Every method starts with the exact same 20 patients, uses the same models, and is tested on the same locked 330-patient test set."*  
  *(Uczciwe porównanie: Każda metoda zaczyna z dokładnie tymi samymi 20 pacjentami, używa tych samych modeli i jest testowana na tym samym zablokowanym zbiorze 330 pacjentów.)*
* **Krok 2 (Kafel 1 i Kafel 2):**  
  *"Baselines: Random Sampling picks 10 random patients per step. Full-Data trains on 100% of the training pool (989 rows). Active Strategies: Entropy Sampling, Margin Sampling closest to the 50/50 boundary, and QBC where 3 models vote."*  
  *(Punkty odniesienia: Random Sampling wybiera 10 losowych pacjentów na krok. Full-Data trenuje na 100% puli treningowej (989 wierszy). Strategie aktywne: Entropy Sampling, Margin Sampling najbliżej granicy 50/50 oraz QBC, gdzie 3 modele głosują.)*
* **Krok 3 (Kafel 3 & dolne zasady):**  
  *"How I Measure Success: Learning Curves from 20 to 300 labels, Area Under Curve (AULC), and Saved Labels in percent. For fair comparison, I lock 25% test data (330 rows), fit StandardScaler only on labeled data, and repeat across 5 random seeds."*  
  *(Jak mierzę sukces: Krzywe uczenia od 20 do 300 etykiet, pole pod krzywą (AULC) oraz zaoszczędzone etykiety w procentach. Dla uczciwego porównania blokuję 25% danych testowych (330 wierszy), dopasowuję StandardScaler tylko na danych oznaczonych i powtarzam testy na 5 ziarnach losowych.)*
* **Krok 4 (pasek Takeaway na dole):**  
  *"Takeaway: Because I lock the test split and run 5 random seeds, any improvement comes strictly from smarter sample selection, not luck or leakage."*  
  *(Wniosek: Ponieważ blokuję podział testowy i wykonuję próby na 5 ziarnach losowych, każda poprawa wynika ściśle z mądrzejszego doboru próbek, a nie ze szczęścia czy wycieku danych.)*

---

## SLAJD 5: Resources, Risks, Fallback Plan & Schedule

* **Krok 1 (lewy kafel — Resources):**  
  *"Computing Resources: Standard laptop CPU, Python with scikit-learn. Running all 30 steps, 4 strategies, and 5 seeds takes under 15 seconds, so testing is very fast."*  
  *(Zasoby obliczeniowe: Standardowy procesor laptopa, Python z biblioteką scikit-learn. Uruchomienie wszystkich 30 kroków, 4 strategii i 5 ziaren zajmuje poniżej 15 sekund, więc testowanie jest bardzo szybkie.)*
* **Krok 2 (prawy kafel — Risks):**  
  *"What Can Go Wrong & How I Will Fix It: Risk 1 is Outlier Trap (impluse = 1111) — Solution: compare Active Learning before and after filtering outliers. Risk 2 is Task Too Easy due to troponin — Fallback Plan: remove troponin to make the classification harder."*  
  *(Co może pójść nie tak i jak to naprawię: Ryzyko 1 to pułapka wartości odstających (tętno 1111) — rozwiązanie: porównać Active Learning przed i po odfiltrowaniu błędów. Ryzyko 2 to zbyt łatwe zadanie przez troponinę — plan awaryjny: usunąć troponinę, aby klasyfikacja była trudniejsza.)*
* **Krok 3 (dolny harmonogram):**  
  *"Project Schedule: Shows the plan from Class 2 through Class 7, leading to our final results and ablations."*  
  *(Harmonogram projektu: Pokazuje plan od Class 2 do Class 7, prowadzący do końcowych wyników i testów ablacyjnych.)*
* **Krok 4 (pasek Takeaway na dole):**  
  *"Takeaway: Even if Active Learning struggles with raw errors or easy features, my outlier and feature-removal tests turn that into a clear scientific result."*  
  *(Wniosek: Nawet jeśli Active Learning napotka trudności z surowymi błędami lub zbyt łatwymi cechami, moje testy usuwania wartości odstających i cech zamienią to w jednoznaczny wynik naukowy.)*
* **Krok 5 (zdanie pod tytułem na górze):**  
  *"Low risk, high control: The whole experiment runs in 15 seconds on a laptop CPU, with a clear backup plan for data outliers and easy features."*  
  *(Niskie ryzyko, wysoka kontrola: Cały eksperyment wykonuje się w 15 sekund na procesorze laptopa, z jasnym planem awaryjnym dla błędów w danych i łatwych cech.)*

---

## 🎯 3 Gotowe Odpowiedzi na Pytania Profesora

1. **Profesor pyta: *Why did you choose AULC instead of just final Accuracy?***
   > **Twoja odpowiedź:**  
   > *"Because in Active Learning, the final accuracy after 300 labels is not the main goal. The main question is how fast the curve rises in the early steps. AULC measures the total area under that learning curve, summarizing sample efficiency into one clear metric, as recommended by Lu et al. (TMLR 2025)."*  
   > *(Ponieważ w Active Learning końcowa dokładność po 300 etykietach nie jest głównym celem. Głównym pytaniem jest to, jak szybko krzywa rośnie w początkowych krokach. AULC mierzy całkowite pole pod tą krzywą uczenia, podsumowując wydajność próbkowania w jednej czytelnej metryce, zgodnie z zaleceniami Lu i innych z TMLR 2025.)*

2. **Profesor pyta: *Why are 5 random seeds necessary?***
   > **Twoja odpowiedź:**  
   > *"Because the recent NeurIPS 2024 benchmark by Werner et al. showed that tabular active learning has high variance depending on the initial seed of 20 samples. A single seed can give misleading conclusions, so 5 seeds with mean and standard deviation are required for credible results."*  
   > *(Ponieważ najnowszy benchmark z NeurIPS 2024 autorstwa Wernera i innych wykazał, że tabelaryczny active learning ma dużą wariancję w zależności od początkowych 20 próbek. Pojedyncze ziarno może dawać mylące wnioski, dlatego 5 ziaren ze średnią i odchyleniem standardowym jest wymagane do wiarygodnych wyników.)*

3. **Profesor pyta: *How do you guarantee zero data leakage?***
   > **Twoja odpowiedź:**  
   > *"I separate the 330 test patients once at the very beginning before any loop starts. And crucially, the StandardScaler is never fitted on the whole dataset — it is fitted strictly on the currently labeled subset at each step."*  
   > *(Oddzielam 330 pacjentów testowych raz, na samym początku, zanim ruszy jakakolwiek pętla. I co kluczowe, StandardScaler nigdy nie jest dopasowywany na całym zbiorze — jest fitowany ściśle tylko na aktualnie oznaczonym podzbiorze w każdym kroku.)*
