import pandas as pd

def przygotuj_dane(plik_bazy, pliki_godzin):
    """Wczytuje i łączy dane z plików Excel."""
    baza_df = pd.read_excel(plik_bazy)
    lista_danych = [pd.read_excel(plik) for plik in pliki_godzin]
    godziny_df = pd.concat(lista_danych, ignore_index=True)
    return baza_df, godziny_df

def przetwarzaj_dane(baza_df, godziny_df):
    """Scala dane i oblicza wynagrodzenie (tę funkcję będziemy testować)."""
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

        # --- FORMATOWANIE: Automatyczne dopasowanie szerokości kolumn ---
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
                # Ustawienie szerokości (najdłuższy tekst + margines)
                worksheet.column_dimensions[kolumna_litera].width = max_length + 2

# Blok główny skryptu
if __name__ == "__main__":
    print("Wczytywanie plików...")
    baza, godziny = przygotuj_dane('baza_pracownikow.xlsx', ['godziny_styczen.xlsx', 'godziny_luty.xlsx'])
    
    print("Przetwarzanie i obliczanie...")
    wynikowe_dane = przetwarzaj_dane(baza, godziny)
    
    print("Generowanie sformatowanego raportu...")
    generuj_raport(wynikowe_dane, 'raport_koncowy.xlsx')
    
    print("Sukces! Sformatowany raport został zapisany.")