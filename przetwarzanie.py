import os

def stworz_produkty(folder, dane_uzytkownika):
    pliki = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    glowne = [f for f in pliki if "_kompozycja" not in f]
    kompozycje = [f for f in pliki if "_kompozycja" in f]

    produkty = []

    for plik in glowne:
        base_name = os.path.splitext(plik)[0]  # bez .jpg
        nazwa = base_name.replace("_", " ").title()  # np. Plakat Zielony Piesek
        slug = base_name.replace("_", "-").lower()

        # dopasuj galerie do tego produktu
        galeria = [f for f in kompozycje if f.startswith(base_name + "_")]

        # opisy i SEO
        opis = dane_uzytkownika["opis_szablon"].replace("{nazwa}", nazwa)
        seo_title = f"{nazwa} | Zacny Druk"
        seo_description = f"Oryginalne plakaty i inne zacne wydruki... Zobacz: {nazwa}!"
        alt = nazwa
        fraza_kluczowa = nazwa

        produkt = {
            "nazwa": nazwa,
            "slug": slug,
            "alt": alt,
            "fraza_kluczowa": fraza_kluczowa,
            "seo_title": seo_title,
            "seo_description": seo_description,
            "glowne_zdjecie": plik,
            "galeria": galeria,
            "opis": opis,
            "kategoria": dane_uzytkownika["kategoria"],
            "warianty": dane_uzytkownika["warianty"]
        }

        produkty.append(produkt)

    return produkty
