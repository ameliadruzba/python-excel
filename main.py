import pandas as pd

# Walidacja danychs

def waliduj_plik_bazowy(df):
    """Sprawdza, czy plik bazowy ma odpowiednie kolumny i typy danych."""
    wymagane_kolumny = ['ID_pracownika', 'Imie _i_nazwisko', 'Dzial', 'Stawka_godzinowa']
    
    # Sprawdzanie brakujących kolumn
    for kol in wymagane_kolumny:
        if kol not in df.columns:
            raise ValueError(f"BŁĄD WALIDACJI: W pliku bazowym brakuje kolumny '{kol}'!")
            
    # Sprawdzanie czy stawka to na pewno liczba
    if not pd.api.types.is_numeric_dtype(df['Stawka_godzinowa']):
        raise TypeError("BŁĄD WALIDACJI: Kolumna 'Stawka_godzinowa' zawiera wartości inne niż liczby!")

def waliduj_plik_godzin(df, nazwa_pliku):
    """Sprawdza, czy pliki z godzinami są poprawne."""
    wymagane_kolumny = ['ID_pracownika', 'Przepracowane_godziny']
    
    # Sprawdzanie brakujących kolumn
    for kol in wymagane_kolumny:
        if kol not in df.columns:
            raise ValueError(f"BŁĄD WALIDACJI: W pliku {nazwa_pliku} brakuje kolumny '{kol}'!")
            
    # Sprawdzanie czy godziny to na pewno liczby
    if not pd.api.types.is_numeric_dtype(df['Przepracowane_godziny']):
        raise TypeError(f"BŁĄD WALIDACJI: W pliku {nazwa_pliku} kolumna 'Przepracowane_godziny' zawiera tekst zamiast liczb!")

# glowne funkcje programu

def przygotuj_dane(plik_bazy, pliki_godzin):
    # Wczytanie i walidacja bazy
    baza_df = pd.read_excel(plik_bazy)
    waliduj_plik_bazowy(baza_df)
    
    # Wczytanie i walidacja plików z godzinami
    lista_danych = []
    for plik in pliki_godzin:
        df = pd.read_excel(plik)
        waliduj_plik_godzin(df, plik)
        lista_danych.append(df)
        
    godziny_df = pd.concat(lista_danych, ignore_index=True) # Bierzemy wszystkie pliki z poszczególnych miesięcy, sklejamy je w pionie w jedną wielką tabelę i porządkujemy im numery wierszy, żeby łatwiej się na nich dalej pracowało
    return baza_df, godziny_df

def przetwarzaj_dane(baza_df, godziny_df):
    """Scala dane i oblicza wynagrodzenie """
    pelne_dane = pd.merge(godziny_df, baza_df, on='ID_pracownika', how='left')
    # Mnożenie godzin przez stawkę
    pelne_dane['Wynagrodzenie'] = pelne_dane['Przepracowane_godziny'] * pelne_dane['Stawka_godzinowa']
    return pelne_dane

def generuj_raport(pelne_dane_df, nazwa_pliku):
    """Grupuje dane, zapisuje do pliku i automatycznie formatuje szerokość kolumn."""
    podsumowanie_prac = pelne_dane_df.groupby(['ID_pracownika', 'Imie _i_nazwisko'])[['Przepracowane_godziny', 'Wynagrodzenie']].sum().reset_index()
    podsumowanie_dzialy = pelne_dane_df.groupby('Dzial')['Wynagrodzenie'].sum().reset_index()

    with pd.ExcelWriter(nazwa_pliku, engine='openpyxl') as writer:
        pelne_dane_df.to_excel(writer, sheet_name='Szczegolowe_Dane', index=False)
        podsumowanie_prac.to_excel(writer, sheet_name='Podsumowanie_Pracownicy', index=False)
        podsumowanie_dzialy.to_excel(writer, sheet_name='Koszty_Dzialow', index=False)

        # formatowanie
        for sheet_name in writer.book.sheetnames:
            worksheet = writer.book[sheet_name]
            for column_cells in worksheet.columns:
                max_length = 0
                kolumna_litera = column_cells[0].column_letter # np. 'A', 'B', 'C'
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                # ustawia szerokosc na najdluzsze slowo + 2
                worksheet.column_dimensions[kolumna_litera].width = max_length + 2

# Blok główny skryptu
if __name__ == "__main__":
    print("Rozpoczynam walidację i wczytywanie plików...")
    baza, godziny = przygotuj_dane('baza_pracownikow.xlsx', ['godziny_styczen.xlsx', 'godziny_luty.xlsx'])
    
    print("Przetwarzanie i obliczanie wynagrodzeń...")
    wynikowe_dane = przetwarzaj_dane(baza, godziny)
    
    print("Generowanie sformatowanego raportu...")
    generuj_raport(wynikowe_dane, 'raport_koncowy.xlsx')
    
    print("Sukces! Sformatowany raport został zapisany. Walidacja przeszła pomyślnie.")