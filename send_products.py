import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("WC_API_URL")
API_KEY = os.getenv("WC_API_KEY")
API_SECRET = os.getenv("WC_API_SECRET")

LOG_FILE = "log.txt"
dry_run = False  # Zmień na True, jeśli chcesz testować bez wysyłania do Woo

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(msg + "\n")

def upload_image(file_path):
    file_name = os.path.basename(file_path)
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }

    with open(file_path, "rb") as f:
        if dry_run:
            log(f"🖼️ [DRY RUN] Zdjęcie: {file_name} nie zostało wysłane.")
            return 9999  # fikcyjne ID testowe
        res = requests.post(
            f"{API_URL.replace('/wc/v3', '')}/wp/v2/media",
            auth=(API_KEY, API_SECRET),
            headers=headers,
            files={"file": f}
        )

    if res.status_code == 201:
        image_id = res.json()["id"]
        log(f"📷 Zdjęcie wysłane: {file_name} (ID: {image_id})")
        return image_id
    else:
        log(f"❌ Błąd przy wysyłaniu zdjęcia {file_name}: {res.status_code} - {res.text}")
        return None

def wyslij_produkty(produkty, folder):
    for produkt in produkty:
        log(f"\n🚀 Wysyłam produkt: {produkt['nazwa']}")

        # Główne zdjęcie
        glowne_zdjecie_path = os.path.join(folder, produkt["glowne_zdjecie"])
        if not os.path.exists(glowne_zdjecie_path):
            log(f"⛔ Brakuje głównego zdjęcia: {glowne_zdjecie_path}. Pomijam produkt.")
            continue

        glowne_zdjecie_id = upload_image(glowne_zdjecie_path)
        if not glowne_zdjecie_id:
            log("⛔ Nie udało się załadować głównego zdjęcia. Pomijam produkt.")
            continue

        # ALT do głównego zdjęcia (dynamiczny na podstawie pliku)
        glowne_alt_text = os.path.splitext(produkt["glowne_zdjecie"])[0].replace("_", " ").title()

        # Galeria
        galeria_media = []
        produkt["galeria"].sort()  # sortowanie zdjęć galerii
        for img_name in produkt["galeria"]:
            img_path = os.path.join(folder, img_name)
            if not os.path.exists(img_path):
                log(f"⚠️ Brakuje zdjęcia galerii: {img_path}")
                continue
            image_id = upload_image(img_path)
            if image_id:
                alt_text = os.path.splitext(img_name)[0].replace("_", " ").title()
                galeria_media.append({"id": image_id, "alt": alt_text})

        # Rozmiary (warianty)
        rozmiary = list(produkt["warianty"].keys())

        payload = {
            "name": produkt["nazwa"],
            "slug": produkt["slug"],
            "type": "variable",
            "status": "publish",
            "description": produkt["opis"],
            "short_description": produkt["opis"],
            "categories": [{"name": produkt["kategoria"]}],  # można zamienić na ID
            "images": [{"id": glowne_zdjecie_id, "alt": glowne_alt_text}] + galeria_media,
            "attributes": [
                {
                    "name": "Rozmiar plakatu",
                    "visible": True,
                    "variation": True,
                    "options": rozmiary
                }
            ],
            "meta_data": [
                {"key": "_yoast_wpseo_title", "value": produkt["seo_title"]},
                {"key": "_yoast_wpseo_metadesc", "value": produkt["seo_description"]},
                {"key": "_yoast_wpseo_focuskw", "value": produkt["fraza_kluczowa"]}
            ]
        }

        if dry_run:
            log(f"🧪 [DRY RUN] Produkt: {produkt['nazwa']} (warianty: {produkt['warianty']})")
            continue

        res = requests.post(
            f"{API_URL}/products",
            auth=(API_KEY, API_SECRET),
            json=payload
        )

        if res.status_code == 201:
            product_id = res.json()["id"]
            log(f"✅ Produkt dodany: {produkt['nazwa']} (ID: {product_id})")

            for rozmiar, cena in produkt["warianty"].items():
                variation_payload = {
                    "regular_price": str(cena),
                    "attributes": [
                        {
                            "name": "Rozmiar plakatu",
                            "option": rozmiar
                        }
                    ]
                }

                var_res = requests.post(
                    f"{API_URL}/products/{product_id}/variations",
                    auth=(API_KEY, API_SECRET),
                    json=variation_payload
                )

                if var_res.status_code == 201:
                    log(f"   ➕ Wariant dodany: {rozmiar} - {cena} zł")
                else:
                    log(f"   ⚠️ Błąd wariantu {rozmiar}: {var_res.status_code} - {var_res.text}")

        elif res.status_code == 400 and "slug" in res.text.lower():
            log(f"⚠️ Produkt o slug '{produkt['slug']}' już istnieje. Pomijam.")
        else:
            log(f"❌ Błąd dodawania produktu {produkt['nazwa']}: {res.status_code} - {res.text}")
