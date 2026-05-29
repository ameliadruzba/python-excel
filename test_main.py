import unittest
import pandas as pd
from main import przetwarzaj_dane

class TestPrzetwarzanieDanych(unittest.TestCase):

    def test_obliczanie_wynagrodzenia(self):
        # 1. Przygotowanie małej, zmyślonej paczki danych do testu
        baza_mock = pd.DataFrame({
            'ID_pracownika': [999],
            'Imie _i_nazwisko': ['Testowy Pracownik'],
            'Dzial': ['IT'],
            'Stawka_godzinowa': [50]  # Wymyślamy stawkę 50
        })

        godziny_mock = pd.DataFrame({
            'ID_pracownika': [999],
            'Miesiac': ['Styczeń'],
            'Przepracowane_godziny': [10], # Wymyślamy 10 godzin
            'Data_raportu': ['2026-01-31']
        })

        # 2. Uruchomienie funkcji z naszego głównego pliku skryptu
        wynik = przetwarzaj_dane(baza_mock, godziny_mock)

        # 3. Sprawdzenie wyniku: 10 godzin * 50 PLN stawki = 500
        # Pobieramy obliczone wynagrodzenie z pierwszego wiersza (indeks 0)
        wynagrodzenie_obliczone = wynik.loc[0, 'Wynagrodzenie']
        
        # Test właściwy: czy wynik faktycznie równa się 500?
        self.assertEqual(wynagrodzenie_obliczone, 500, "Błąd: Wynagrodzenie zostało źle obliczone!")

if __name__ == '__main__':
    unittest.main()