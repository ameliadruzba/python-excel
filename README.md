# Automatyzacja obsługi plików Excel - Kadry i Płace

Projekt ma na celu demonstrację automatyzacji procesów biurowych przy użyciu języka Python. Skrypt wczytuje dane bazowe pracowników oraz raporty z przepracowanymi godzinami z wielu plików, dokonuje ich scalenia (merge), oblicza należne wynagrodzenie, a następnie grupuje dane i eksportuje je do gotowego raportu z podziałem na arkusze.

## 1. Jak uruchomić projekt

Do uruchomienia skryptu wymagany jest język Python (wersja 3.x) oraz instalacja zewnętrznych bibliotek do obsługi struktury danych i plików Excel.

**Instalacja wymaganych bibliotek:**
Otwórz terminal/wiersz poleceń i wpisz poniższą komendę:
`pip install pandas openpyxl`

**Uruchomienie skryptu:**
Upewnij się, że plik `main.py` oraz wszystkie pliki `.xlsx` z danymi znajdują się w tym samym folderze. W terminalu uruchom komendę:
`python main.py`

## 2. Struktura plików i kolumn

Projekt operuje na trzech plikach wejściowych. Aby skrypt zadziałał poprawnie, pliki muszą posiadać następujące nagłówki kolumn:

**Plik bazowy (baza_pracownikow.xlsx):**
* `ID_pracownika` - unikalny identyfikator pracownika (klucz do scalania)
* `Imie _i_nazwisko` - dane personalne pracownika
* `Dzial` - dział, do którego przypisany jest pracownik (np. IT, HR)
* `Stawka_godzinowa` - stawka w PLN za jedną godzinę pracy

**Pliki szczegółowe z godzinami (godziny_styczen.xlsx, godziny_luty.xlsx):**
* `ID_pracownika` - identyfikator pracownika
* `Miesiac` - nazwa miesiąca
* `Przepracowane_godziny` - liczba wypracowanych godzin
* `Data_raportu` - data sporządzenia zestawienia

## 3. Przykład użycia i oczekiwany wynik

Po uruchomieniu skryptu `main.py`, program automatycznie zaczyta pliki wejściowe w pętli. 
W terminalu zostanie wyświetlona informacja o pomyślnym połączeniu danych, a w folderze z projektem zostanie wygenerowany nowy plik: **raport_koncowy.xlsx**.

**Oczekiwany wynik w pliku raport_koncowy.xlsx:**
Plik wynikowy zawiera zautomatyzowane formatowanie i składa się z trzech arkuszy:
1. `Szczegolowe_Dane` - pełne, połączone zestawienie wszystkich rekordów (baza + godziny) wraz z wyliczoną nową kolumną `Wynagrodzenie` (Przepracowane_godziny * Stawka_godzinowa).
2. `Podsumowanie_Pracownicy` - pogrupowane dane prezentujące łączną sumę przepracowanych godzin oraz całkowite wynagrodzenie dla każdego pracownika za zbadany okres.
3. `Koszty_Dzialow` - pogrupowane dane prezentujące całkowity koszt wynagrodzeń w podziale na poszczególne działy w firmie.