from gui_dane import uruchom_gui
from przetwarzanie import stworz_produkty

dane_uzytkownika = uruchom_gui()
produkty = stworz_produkty("product_images", dane_uzytkownika)

for p in produkty:
    print(f"\n📦 {p['nazwa']}")
