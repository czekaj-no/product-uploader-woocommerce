import os
import base64
import mimetypes
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("WC_API_URL")
API_KEY = os.getenv("WC_API_KEY")
API_SECRET = os.getenv("WC_API_SECRET")

def zaladuj_zdjecie_jako_base64(sciezka):
    mime_type, _ = mimetypes.guess_type(sciezka)
    with open(sciezka, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def wyslij_produkty(produkty, folder):
    for produkt in produkty:
        print(f"🚀 Wysyłam produkt: {produkt['nazwa']}")

        # Załaduj główne zdjęcie
        glowne_zdjecie_path = os.path.join(folder, produkt["glowne_zdjecie"])
        glowne_zdjecie_data = zaladuj_zdjecie_jako_base64(glowne_zdjecie_path)

        # Galeria
        galeria_media = []
        for img_name in produkt["galeria"]:
            img_path = os.path.join(folder, img_name)
            galeria_media.append({
                "src": zaladuj_zdjecie_jako_base64(img_path)
            })

        # Podstawowy produkt
        payload = {
            "name": produkt["nazwa"],
            "slug": produkt["slug"],
            "type": "variable",
            "status": "publish",
            "description": produkt["opis"],
            "short_description": produkt["opis"],
            "categories": [{"name": produkt["kategoria"]}],
            "images": [{"src": glowne_zdjecie_data, "alt": produkt["alt"]}] + galeria_media,
            "meta_data": [
                {"key": "_yoast_wpseo_title", "value": produkt["seo_title"]},
                {"key": "_yoast_wpseo_metadesc", "value": produkt["seo_description"]},
                {"key": "_yoast_wpseo_focuskw", "value": produkt["fraza_kluczowa"]}
            ]
        }

        res = requests.post(
            f"{API_URL}/products",
            auth=(API_KEY, API_SECRET),
            json=payload
        )

        if res.status_code == 201:
            product_id = res.json()["id"]
            print(f"✅ Produkt dodany: ID {product_id}")
        else:
            print(f"❌ Błąd przy dodawaniu produktu {produkt['nazwa']}")
            print(res.status_code, res.text)
