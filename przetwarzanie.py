import os

def stworz_produkty(folder, dane_uzytkownika):
    pliki = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    glowne = [f for f in pliki if "_kompozycja" not in f]
    kompozycje = [f for f in pliki if "_kompozycja" in f]

    produkty = []

    for plik in glowne:
        base_name = os.path.splitext(plik)[0]
        nazwa = base_name.replace("_", " ").title()
        slug = base_name.replace("_", "-").lower()

        base_name_lower = base_name.lower()
        galeria = [f for f in kompozycje if f.lower().startswith(base_name_lower + "_")]

        opis = dane_uzytkownika["opis_szablon"].replace("{nazwa}", nazwa)
        seo_title = dane_uzytkownika["seo_title_template"].replace("{nazwa}", nazwa)
        seo_description = dane_uzytkownika["seo_description_template"].replace("{nazwa}", nazwa)

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
