Dataset Readme
-----------------------

Zbiór danych Leafsnap (http://leafsnap.com) jest elektronicznym przewodnikiem terenowym do identyfikacji gatunków drzew na podstawie zdjęć ich liści. Został stworzony przez naukowców z Columbia University i University of Maryland oraz botanistów z Smithsonian Institution. Zbiór ten zawiera obrazy liści pochodzące z dwóch głównych źródeł:

Obrazy "Lab" - wysokiej jakości zdjęcia prasowanych liści, wykonane w kontrolowanych warunkach.
Obrazy "Field" - zdjęcia wykonane w warunkach terenowych, zawierające różne elementy takie jak rozmycie czy cienie.
Cele projektu
Celem tego projektu jest wykorzystanie zbioru danych Leafsnap do rozwoju modelu rozpoznawania gatunków drzew na podstawie obrazów liści. Zastosowane metody uczenia maszynowego będą służyły do klasyfikacji gatunków na podstawie dostarczonych obrazów.

Struktura zbioru danych
Dane zostały podzielone na trzy zestawy:

Zbiór treningowy: Używany do nauki modelu.
Zbiór walidacyjny: Używany do strojenia hiperparametrów i oceny wydajności modelu w trakcie jego trenowania.
Zbiór testowy: Używany do ostatecznej oceny wydajności modelu po zakończeniu procesu uczenia.
Podział danych
Dane są zorganizowane w następujący sposób:

Dataset/
├── train/
│   ├── lab/
│   ├── field/
├── validation/
│   ├── lab/
│   ├── field/
├── test/
│   ├── lab/
│   ├── field/

- train/: Zawiera dane treningowe. Obrazy są podzielone na podfoldery lab i field zgodnie z ich źródłem.
- validation/: Zawiera dane walidacyjne. Podobnie jak w przypadku danych treningowych, obrazy są zorganizowane w podfoldery.
- test/: Zawiera dane testowe, zorganizowane w ten sam sposób co pozostałe zbiory.

Plik dataset-images.txt
Zawiera listę wszystkich obrazów w formacie oddzielonym tabulatorami. Pierwsza linia to nagłówek opisujący każdą kolumnę:

file_id    image_path   segmented_path    species    source

Każda linia zawiera informacje o pojedynczym obrazie, składającą się z pięciu pól, oddzielonych tabulatorami:
- file_id: Unikalny identyfikator numeryczny dla każdego obrazu. Nie są one gwarantowane jako kolejne lub w porządku. Nie zmienią się w przyszłych wersjach zbioru danych.
- image_path: Ścieżka do oryginalnego obrazu.
- segmented_path: Ścieżka do wersji segmentowanej obrazu.
- species: Nazwa gatunku przedstawionego na obrazie. Może zawierać spacje i myślniki, oraz występuje w mieszanym formacie (wielkie i małe litery).
- source: Źródło obrazu. Może to być 'lab' lub 'field'.