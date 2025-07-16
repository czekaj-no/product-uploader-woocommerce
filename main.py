from gui_dane import uruchom_gui
from przetwarzanie import stworz_produkty
from demo import pokaz_demo
from send_products import wyslij_produkty  # Jeśli masz osobny plik od wysyłania

def main():
    dane_uzytkownika = uruchom_gui()

    if not dane_uzytkownika:
        print("❌ Brak danych od użytkownika.")
        return

    produkty = stworz_produkty(dane_uzytkownika["folder"], dane_uzytkownika)

    if not produkty:
        print("❌ Nie znaleziono żadnych produktów.")
        return

    if dane_uzytkownika["tryb"] == "test":
        print("🔍 Tryb TEST – wyświetlamy demo.")
        pokaz_demo(produkty)
    else:
        print("🚀 Tryb LIVE – wysyłamy produkty do WooCommerce.")
        wyslij_produkty(produkty)  # zakładamy, że ta funkcja obsługuje wysyłkę

    for p in produkty:
        print(f"\n📦 {p['nazwa']}")

if __name__ == "__main__":
    main()
