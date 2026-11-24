# Plan prezentacji — Class 4 (Baseline & Data Check)

**Zakres na kolejne laby:** Slajdy **08–11** w pliku `prezentacja.html`  
**Docelowy czas mówienia:** ok. **2,5 – 3,5 minuty** (idealnie na zajęcia robocze).

---

## Jak czytać ze slajdu, żeby nie było tego widać (3 proste triki)

1. **Wskazuj kursorem lub ręką na wykres / liczbę:** kiedy patrzysz na ekran, żeby pokazać `0.90` albo zieloną linię na wykresie, nikt nie odbiera tego jak „czytanie kartki” — wygląda to jak naturalne omawianie wyników.
2. **Mów po 1 krótkim zdaniu i rób pół sekundy pauzy:** wolniejsze tempo brzmi pewnie i profesjonalnie, nawet przy prostym angielskim.
3. **W tekście poniżej pogrubione fragmenty są dokładnie na slajdzie** — zerkasz na slajd, czytasz kluczowe liczby/hasła, a łączysz je krótkimi, naturalnymi zwrotami (np. *"So here we can see..."*, *"This means..."*, *"Next..."*).

---

## Mini-ściąga wymowy (trudniejsze słowa po polsku)

| Słowo na slajdzie | Jak przeczytać (prosto) |
|---|---|
| `audit` | *odit* |
| `baseline` | *bejslajn* |
| `data leakage` | *dejta likidż* |
| `troponin` | *troponin* |
| `outliers` | *autlajers* |
| `curves` | *kerws* |
| `seeds` | *sids* |
| `variance` | *werians* |
| `confusion matrix` | *konfjużyn mejtriks* |
| `reproducible` | *riprodjusybl* (albo powiedz prościej: *repeatable* — *ripitybl*) |

---

## Szybkie przejście z poprzednich zajęć (opcjonalnie, 10 sekund)

*Jeśli prowadzący powie „pokaż co masz na dzisiaj”, przełącz od razu na **Slajd 8** i zacznij tak:*

> **ENG:** "Hello. Last time I showed my three papers and my experiment plan. Today, for Class 4, I will show my **data audit** and my **working baseline**."
>
> **PL:** *(Cześć. Ostatnio pokazałem 3 artykuły i plan eksperymentu. Dzisiaj na Class 4 pokażę audyt danych i działający baseline.)*

---

## SLAJD 8 — Data Audit: Clean Table, Real Errors & Strong Signal (~45 sek.)

**👁️ Na co patrzysz:** najpierw 4 kafelki na górze → potem lewy wykres (`troponin`) → potem prawy wykres (`11 rows`, `3 rows`) → 3 dolne ramki.

1. **[Górne kafelki]**
   > **ENG:** "First, I checked all **1,319 patients** before training any model. The table has **zero missing values** and **zero duplicates**. About **61%** are positive cases, and I locked **330 rows** as my test set."
   > *(PL: Najpierw sprawdziłem wszystkie 1319 wierszy przed trenowaniem modeli. Nie ma braków ani duplikatów. Ok. 61% to przypadki pozytywne, a 330 wierszy zamroziłem jako zbiór testowy.)*

2. **[Lewy wykres — pokaż niebieski pasek `troponin`]**
   > **ENG:** "On the left chart, we can see which features predict heart attack on the training pool. **`troponin` alone reaches 0.90 ROC-AUC**, while `kcm` is **0.67** and `age` is **0.65**. The other five features are very weak."
   > *(PL: Na lewym wykresie widać, które cechy przewidują zawał na puli treningowej. Sama troponina daje 0.90 ROC-AUC, kcm 0.67, wiek 0.65. Pozostałe 5 cech jest bardzo słabych.)*

3. **[Prawy wykres — pokaż czerwone paski]**
   > **ENG:** "On the right chart, I found real measurement errors. **11 rows** have low blood pressure higher than high pressure, which is impossible. And **3 rows** have heart rate equal to **1111**. All three `1111` errors are in the training pool, and there is **zero overlap** between train and test."
   > *(PL: Na prawym wykresie znalazłem prawdziwe błędy pomiarów. 11 wierszy ma dolne ciśnienie wyższe niż górne, co jest niemożliwe. A 3 wiersze mają tętno 1111. Wszystkie 3 błędy 1111 są w puli treningowej i nie ma żadnego pokrywania między treningiem a testem.)*

---

## SLAJD 9 — Working Baseline & Reproducible Setup (~45 sek.)

**👁️ Na co patrzysz:** lewy górny kafelek → prawy górny kafelek → 2 główne wiersze w tabeli na dole (`118` i `58`).

1. **[Lewy górny kafelek]**
   > **ENG:** "Next, I built my working baseline code in Python with **no data leakage**. The **330 test rows** are saved and locked in a JSON file. At every step, **`StandardScaler` fits only on the labeled rows**, never on the test set. Every run starts with **20 balanced patients** and adds **10 random patients** per step, up to 300."
   > *(PL: Następnie zbudowałem działający kod baseline'u w Pythonie bez wycieku danych. 330 wierszy testowych jest zapisanych w JSON. W każdym kroku StandardScaler uczy się tylko na oetykietowanych danych, nigdy na teście. Każdy bieg startuje od 20 zbalansowanych pacjentów i dodaje po 10 losowych aż do 300.)*

2. **[Prawy górny kafelek]**
   > **ENG:** "I ran the full experiment on **5 fixed random seeds**. On a normal laptop CPU, everything finishes in **28.5 seconds**, and all raw numbers are saved in the `results` folder."
   > *(PL: Cały eksperyment puściłem na 5 stałych seedach. Na zwykłym CPU laptopa całość trwa 28,5 sekundy, a wszystkie surowe wyniki są zapisane w folderze results.)*

3. **[Tabela na dole — wskaż kolumnę po prawej `Labels for 95%`]**
   > **ENG:** "In the table, we have two main targets to beat later. **Logistic Regression** gets **75.4% Macro F1** on all data, and Random Sampling needs **118 labels** on average to reach 95% of that score. **Random Forest** gets **97.5%**, and needs only **58 random labels**. Both easily beat the **Majority Class floor** at **38.1%**."
   > *(PL: W tabeli mamy dwa główne cele do pobicia. Regresja logistyczna ma 75,4% Macro F1 na całych danych, a losowy wybór potrzebuje średnio 118 etykiet na 95% tego wyniku. Random Forest ma 97,5% i potrzebuje tylko 58 etykiet. Oba modele spokojnie biją prosty baseline klasy większościowej 38,1%.)*

---

## SLAJD 10 — Baseline Learning Curves: Random Forest vs. LogReg (~40 sek.)

**👁️ Na co patrzysz:** lewy wykres (`Macro F1`) → zielona krzywa → niebieska krzywa → dwa dolne boksy.

1. **[Ogólny opis wykresów]**
   > **ENG:** "Here are the learning curves from **20 to 300 labels**. The solid lines show the average over **5 seeds**, the shaded area shows the spread, and the dashed lines show the **full-data score** on all 989 rows."
   > *(PL: Tutaj są krzywe uczenia od 20 do 300 etykiet. Ciągłe linie to średnia z 5 seedów, cieniowany obszar to rozrzut/odchylenie, a przerywane linie to wynik na całych 989 wierszach.)*

2. **[Zielona krzywa + lewy dolny boks]**
   > **ENG:** "Look at the green line: **Random Forest learns very fast**. It jumps from **80%** to almost **96%** at 100 labels, and hits its 95% target in about **58 labels**. This happens because decision trees quickly learn the strong **`troponin`** cutoff."
   > *(PL: Spójrzmy na zieloną linię: Random Forest uczy się bardzo szybko. Skacze z 80% do prawie 96% przy 100 etykietach i osiąga cel 95% po ok. 58 etykietach. Dzieje się tak, bo drzewa szybko łapią silny próg troponiny.)*

3. **[Niebieska krzywa + prawy dolny boks]**
   > **ENG:** "The blue line is **Logistic Regression**. It improves much more slowly and needs about **118 labels**. A simple linear model struggles with skewed blood values and extreme errors like **`impluse = 1111`**."
   > *(PL: Niebieska linia to regresja logistyczna. Poprawia się znacznie wolniej i potrzebuje ok. 118 etykiet. Prosty model liniowy ma problem ze skośnymi wynikami krwi i skrajnymi błędami jak tętno 1111.)*

---

## SLAJD 11 — Seed Variance, Error Check & Plan for Class 5 (~45 sek.)

**👁️ Na co patrzysz:** lewy wykres słupkowy (`Seed 100` vs `Seed 2026`) → 2 macierze pomyłek po prawej → pomarańczowy boks (plan na Class 5).

1. **[Lewy wykres słupkowy — wskaż słupek `30` i słupek `230`]**
   > **ENG:** "Finally, I checked each seed separately. On Logistic Regression, one lucky seed needs only **30 labels**, while another seed needs **230 labels**. This confirms the NeurIPS 2024 paper by Werner: **running just 1 seed is not reliable**."
   > *(PL: Na koniec sprawdziłem każdy seed osobno. Dla regresji logistycznej jeden szczęśliwy seed potrzebuje 30 etykiet, a inny aż 230. To potwierdza artykuł Wernera z NeurIPS 2024: jeden seed nie jest wiarygodny.)*

2. **[Środkowa i prawa macierz pomyłek]**
   > **ENG:** "On the right, we see the test errors on **330 patients**. **Random Forest** makes only **8 errors** in total — 6 missed heart attacks and 2 false alarms. **Logistic Regression** makes **77 errors**."
   > *(PL: Po prawej widać błędy na 330 pacjentach testowych. Random Forest robi tylko 8 błędów — 6 przeoczonych zawałów i 2 fałszywe alarmy. Regresja logistyczna robi 77 błędów.)*

3. **[Prawy dolny pomarańczowy boks — zakończenie]**
   > **ENG:** "So now the data audit and reproducible baseline are complete. **Next week, for Class 5**, I will plug **Entropy**, **Margin**, and **Query-By-Committee** into this exact same loop to test if Active Learning saves **30% to 40% of labels**. And later in **Class 6**, I will remove the errors and also test without **`troponin`**. Thank you!"
   > *(PL: Audyt danych i powtarzalny baseline są więc gotowe. W przyszłym tygodniu na Class 5 podepnę Entropy, Margin i QBC do tej samej pętli, żeby sprawdzić, czy Active Learning oszczędza 30–40% etykiet. A na Class 6 usunę błędy i przetestuję bez troponiny. Dziękuję!)*

---

## Koło ratunkowe: możliwe pytania prowadzącego + proste odpowiedzi

**1. Why is Random Forest so much better than Logistic Regression here?** *(Dlaczego RF jest o wiele lepszy od LogReg?)*
> **ENG:** "Because `troponin` and `kcm` are very skewed and have sharp medical thresholds. Trees handle thresholds easily, while a linear model struggles with skewed numbers and outliers."

**2. How do you make sure there is no data leakage?** *(Skąd wiesz, że nie ma wycieku danych?)*
> **ENG:** "I lock 25% of patients once at the beginning, save their indices, and fit `StandardScaler` only on the currently labeled training rows at each step."

**3. Random Forest already reaches 95% in 58 labels — is there still room for Active Learning?** *(RF osiąga 95% już w 58 etykietach — czy jest tu miejsce na Active Learning?)*
> **ENG:** "Yes, in two ways: first, we can test if Active Learning beats 58 labels on Random Forest in the early steps, and beats 118 labels on LogReg. Second, in Class 6 I will remove `troponin` to make the task harder."

**4. Did you remove the `impluse = 1111` errors already?** *(Czy już usunąłeś błędy `impluse = 1111`?)*
> **ENG:** "Not yet. I kept the raw data on purpose for the baseline, so in Class 6 I can compare raw data versus cleaned data and test if outliers trick Active Learning."

**5. Why did you also show the Majority Class baseline?** *(Po co pokazałeś Majority Class Floor?)*
> **ENG:** "Because 61.4% of patients are positive, so predicting 'positive' for everyone already gives 61.5% accuracy, but only 38.1% Macro F1. That is why Macro F1 is my main metric."
