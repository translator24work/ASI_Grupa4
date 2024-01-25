# Dokumentacja Biznesowo-Techniczna Projektu ASI_Grupa4

## Wprowadzenie

Dokumentacja ta ma na celu zapewnienie nowym członkom zespołu, zarówno z technicznym, jak i nietechnicznym tłem, kompleksowego przeglądu naszego projektu. Zawiera informacje o produkcie, jego funkcjonalnościach oraz instrukcje korzystania.

## Opis Produktu

**Ogólny Opis:**

Projekt wykorzystuje techniki uczenia maszynowego do analizy danych i dokonywania predykcji. Jest przeznaczony do dostarczania dokładnych przewidywań opartych na danych zgromadzonych w bazie danych.

**Kluczowe Zalety i Zastosowania:**

Głównymi zaletami produktu są jego zdolność do przetwarzania dużych ilości danych, dokładność przewidywań oraz wszechstronność zastosowań w różnych scenariuszach biznesowych i technicznych.

## Jak Korzystać z Produktu

**Instalacja i Konfiguracja:**

Sklonuj repozytorium na komputer lokalny:
````
git clone https://github.com/translator24work/ASI_Grupa4.git
````

**Zainstaluj Condę:**
````
https://conda.io/projects/conda/en/latest/user-guide/install/index.html
````

**Utwórz środowisko Conda:**
````
conda create --name kedro-environment python=3.10 -y
conda activate kedro-environment
conda install -c conda-forge kedro
conda install -c conda-forge kedro-viz
conda activate kedro-environment
````

**Zainstaluj zależności Kedro:**
````
cd kedro-asi/
pip install -r src/requirements.txt
````

**Zainstaluj postgresql na swoim komputerze:**
````
https://www.postgresql.org/download/
````

**Teraz musimy zdefiniować schemat bazy danych i tabelę.**

W repozytorium możesz znaleźć plik o nazwie ````init.sql````, który to zrobi.
Po wykonaniu tego skryptu możesz użyć pliku ````dump.sql````, który wstawi dane z pliku **csv** do tabeli **sql**. Musisz zastąpić znajdującą się w nim ścieżkę ````(/path/to/your/file.csv)```` poprawną ścieżką do lokalnego pliku **cwurData.csv**
Teraz musisz umieścić w ````kedro-asi/conf/local/credentials.yml```` (zamień ````your_username````, ````your_password````, ````your_database```` na właściwą konfigurację **postgresql**):
````
my_postgres_db:
  type: postgres
  host: localhost
  port: 5432
  username: your_username
  password: your_password
  database: your_database
````
**Jeśli chcesz wdrożyć potok za pomocą StreamLit, musisz wykonać:**
````
cd kedro-asi/
streamlit run streamlit.py
````

## Funkcjonalności
### Główne Funkcje

#### Analiza Danych i Predykcja: 
Wykorzystanie technik Machine Learningu do analizy danych i dokonywania predykcji.

#### Interakcja z API: 
Możliwość wysyłania zapytań do API ````(/predict)```` z odpowiednimi danymi, które skutkują dokonaniem predykcji.

#### Proces Przetwarzania Danych: 
System umożliwia przetwarzanie danych, trenowanie modelu, dokonywanie predykcji, wizualizację i śledzenie procesu uczenia maszynowego.

#### Architektura Systemu: 
Składa się z części Frontendowej (Streamlit), gdzie można wysłać zapytanie do API (Fast API) w celu uruchomienia potoku Kedro ````(/run)```` lub dokonać predykcji przez formularz ````(/predict)````. W potoku Kedro następuje połączenie z bazą danych, analiza danych przez Autogluon, tworzenie modelu do predykcji oraz śledzenie i wizualizacja procesu uczenia za pomocą Wandb.



