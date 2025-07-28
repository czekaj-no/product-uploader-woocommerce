from gui_data import uruchom_gui
from przetwarzanie import stworz_produkty
from demo import pokaz_demo
from dotenv import load_dotenv
import os
from send_products import wyslij_produkty  # Jeśli masz osobny plik od wysyłania

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


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
        wyslij_produkty(produkty, dane_uzytkownika["folder"])

    # Drukuj nazwę każdego produktu
    for p in produkty:
        print(f"\n📦 {p['nazwa']}")


if __name__ == "__main__":
    main()
