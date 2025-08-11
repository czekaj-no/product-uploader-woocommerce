import os
import requests
from dotenv import load_dotenv
import unidecode

load_dotenv()

REQUIRED_ENV_VARS = ["API_URL", "API_KEY", "API_SECRET"]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    print("❌ Brakuje poniższych zmiennych środowiskowych w pliku .env:")
    for var in missing_vars:
        print(f"   - {var}")
    print("📁 Upewnij się, że plik .env znajduje się w tym samym folderze co main.py i zawiera wszystkie wymagane wpisy.")
    exit(1)

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
MEDIA_ENDPOINT = os.getenv("MEDIA_ENDPOINT")
JWT_TOKEN = os.getenv("JWT_TOKEN")

LOG_FILE = "log.txt"
dry_run = False



def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(msg + "\n")


def upload_image(file_path):
    file_name = os.path.basename(file_path)
    safe_file_name = unidecode.unidecode(file_name)  # usunięcie polskich znaków
    title = os.path.splitext(safe_file_name)[0].replace("_", " ").title()

    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Disposition": f"attachment; filename={safe_file_name}"
    }

    with open(file_path, "rb") as f:
        res = requests.post(
            MEDIA_ENDPOINT,
            headers=headers,
            files={"file": (safe_file_name, f, "image/jpeg")},
            data={
                "title": title,
                "alt_text": title
            }
        )

    if res.status_code == 201:
        image_id = res.json().get("id")
        log(f"📷 Zdjęcie wysłane: {file_name} (ID: {image_id})")
        return image_id
    else:
        log(f"❌ Błąd przy wysyłaniu zdjęcia {file_name}: {res.status_code} - {res.text}")
        return None


def wyslij_produkty(produkty, folder):
    for produkt in produkty:
        log(f"\n🚀 Wysyłam produkt: {produkt['nazwa']}")

        glowne_zdjecie_path = os.path.join(folder, produkt["glowne_zdjecie"])
        if not os.path.exists(glowne_zdjecie_path):
            log(f"⛔ Brakuje głównego zdjęcia: {glowne_zdjecie_path}. Pomijam produkt.")
            continue

        glowne_zdjecie_id = upload_image(glowne_zdjecie_path)
        if not glowne_zdjecie_id:
            log("⛔ Nie udało się załadować głównego zdjęcia. Pomijam produkt.")
            continue

        glowne_alt_text = os.path.splitext(produkt["glowne_zdjecie"])[0].replace("_", " ").title()

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

        rozmiary = list(produkt["warianty"].keys())

        payload = {
            "name": produkt["nazwa"],
            "slug": produkt["slug"],
            "type": "variable",
            "status": "publish",
            "description": produkt["opis"],
            "categories": [{"id": 73}],
            "images": [{"id": glowne_zdjecie_id, "alt": glowne_alt_text}] + galeria_media,
            "attributes": [
                {
                    "name": "Rozmiar plakatu",
                    "visible": False,
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
