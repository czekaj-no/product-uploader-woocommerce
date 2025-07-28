from dotenv import load_dotenv
import os
import requests

def odswiez_token_i_zapisz_do_env():
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv("PASSW")
    base_url = os.getenv("URL").rstrip("/")  # bez końcowego "/"
    token_url = f"{base_url}/wp-json/jwt-auth/v1/token"

    response = requests.post(token_url, data={"username": login, "password": password})
    if response.status_code != 200:
        raise Exception(f"❌ Nie udało się pobrać tokena: {response.status_code} {response.text}")

    token = response.json().get("token")
    if not token:
        raise Exception("❌ Brak tokena w odpowiedzi")

    # Nadpisz JWT_TOKEN w .env
    nowa_zawartosc = []
    jwt_found = False
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("JWT_TOKEN="):
                nowa_zawartosc.append(f"JWT_TOKEN={token}\n")
                jwt_found = True
            else:
                nowa_zawartosc.append(line)

    if not jwt_found:
        nowa_zawartosc.append(f"JWT_TOKEN={token}\n")

    with open(".env", "w", encoding="utf-8") as f:
        f.writelines(nowa_zawartosc)

    print("✅ Nowy token zapisany do .env")
    return token
