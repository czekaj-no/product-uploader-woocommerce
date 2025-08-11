import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
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

def klik_odswiez_token():
    try:
        nowy_token = odswiez_token_i_zapisz_do_env()
        messagebox.showinfo("Sukces", "✅ Nowy token został zapisany.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się odświeżyć tokena:\n{e}")


text_seo_title = None
text_seo_description = None
dane_uzytkownika = None  # finalne dane użytkownika
folder_var = None
pola_wariantow = {}

load_dotenv()
API_URL = os.getenv("WC_API_URL")
API_KEY = os.getenv("WC_API_KEY")
API_SECRET = os.getenv("WC_API_SECRET")

cenniki = {

    "BARDZO TANI": {
        "30x40": "39.00",
        "40x50": "45.00",
        "50x70": "55.00",
        "60x90": "65.00",
        "70x100": "79.00",
        "100x140": "129.00"
    },

    "TANI": {
        "30x40": "49.00",
        "40x50": "55.00",
        "50x70": "65.00",
        "60x90": "79.00",
        "70x100": "95.00",
        "100x140": "159.00"
    },
    "NORMALNY": {
        "30x40": "59.00",
        "40x50": "69.00",
        "50x70": "79.00",
        "60x90": "99.00",
        "70x100": "119.00",
        "100x140": "199.00"
    },
    "DROGI": {
        "30x40": "69.00",
        "40x50": "99.00",
        "50x70": "125.00",
        "60x90": "149.00",
        "70x100": "175.00",
        "100x140": "299.00"
    }
}

szablony_opisow = {

    "wybierz kategorię bejbe": """wybierz prawidłową kategorię bejbe!""",
    "plakaty": """<h2>{nazwa}</h2>
     {nazwa} to ciekawy element dekoracyjny od Zacnego Druku. Idealnie sprawdzi się jako ozdoba do Twojego domu lub oryginalny prezent. Łatwy do oprawienia, dostępny w popularnych rozmiarach.<br><br>
     Plakat będzie świetnie wyglądał zarówno solo, jak i w galerii ściennej. Dodaj wyjątkowy akcent, który przyciąga wzrok i tworzy niepowtarzalny klimat w Twoim wnętrzu.<br><br>

     <h3>Doskonała jakość</h3>
     Zacny Druk to połączenie artystycznej finezji z wysoką jakością wykonania. Każdy plakat drukujemy na zamówienie. Korzystamy z nowoczesnych drukarek HP oraz EPSON oraz tylko oryginalnych tuszy. Dzięki temu kolory są intensywne, a detale – wyjątkowo wyraźne.<br><br>
     Drukujemy na sztywnym, eleganckim papierze premium, który zapewnia <strong>trwałość i odporność na upływ czasu.</strong><br><br>
     Więcej o jakości i dostępnych rozmiarach znajdziesz <a href="https://zacnydruk.pl/nasze-plakaty/" target="_blank"><strong>tutaj</strong></a>.<br><br>

     <h3><strong>Szybka i bezpieczna wysyłka</strong></h3>
     Twoje zamówienie spakujemy z troską – jak dla siebie! Plakat zostanie starannie zwinięty i umieszczony w grubej, kartonowej tubie, a dodatkowo zabezpieczony folią. Dzięki temu dotrze do Ciebie w idealnym stanie.<br><br>
     Tak przygotowaną przesyłkę wysyłamy w ciągu 1–2 dni roboczych kurierem lub do wybranego paczkomatu. A przy zakupach <strong>od 149 zł – dostawa gratis!</strong><br><br>

     <h3><strong>Gwarancja satysfakcji</strong></h3>
     Wierzymy, że {nazwa} wzbogaci każde wnętrze. Jeśli jednak nie spełni Twoich oczekiwań, możesz go <strong>zwrócić w ciągu 30 dni</strong> bez podania przyczyny.<br><br>
     Zależy nam na Twojej satysfakcji – kupuj bez ryzyka!""",
    "plakaty personalizowane": "Personalizowany plakat {nazwa} to oryginalny prezent i pamiątka. Dodaj swoje dane i stwórz unikalny projekt dopasowany do Ciebie.",
    "mapy gotowe": "Mapa {nazwa} została zaprojektowana z dbałością o każdy detal. Idealna do biura, salonu lub jako prezent.",
    "mapy nieba / gwiazd": "Mapa nieba z momentu {nazwa} to pamiątka chwili, którą chcesz zatrzymać na zawsze. Niezwykły widok gwiazd w wyjątkowym momencie.",
    "mapy ważnego miejsca": "Mapa miejsca {nazwa} pokazuje najważniejsze dla Ciebie miejsce na świecie. To więcej niż dekoracja – to emocje."
}

warianty_stale = [
    "30x40",
    "40x50",
    "50x70",
    "60x90",
    "70x100",
    "100x140"
]

def ustaw_ceny(typ_cen):
    ceny = cenniki.get(typ_cen)
    if not ceny:
        return

    # Wpisz ceny do pól
    for wariant, entry in pola_wariantow.items():
        if wariant in ceny:
            entry.delete(0, tk.END)
            entry.insert(0, ceny[wariant])

    # Zmień kolory przycisków
    for typ, btn in przyciski_cennika.items():
        if typ == typ_cen:
            btn.config(bg="#b9fbc0")
        else:
            btn.config(bg="SystemButtonFace")  # domyślny kolor


przyciski_cennika = {}

def uruchom_gui():
    global root, text_log, selected_kategoria, text_opis, pola_wariantow, tryb, folder_var
    root = tk.Tk()
    root.title("ZACNY PRODUCTS 3000")
    root.geometry("750x750")
    root.option_add("*Font", "Helvetica 10")

    tryb = tk.StringVar(value="test")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frame, text="ZACNY PRODUCTS 3000", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(frame, text="Tryb:").grid(row=1, column=0, sticky="w")
    tk.Radiobutton(frame, text="TEST", variable=tryb, value="test").grid(row=2, column=0, sticky="w")
    tk.Radiobutton(frame, text="LIVE", variable=tryb, value="live").grid(row=3, column=0, sticky="w")

    tk.Label(frame, text="Kategoria:").grid(row=4, column=0, sticky="w", pady=(10, 0))
    selected_kategoria = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=selected_kategoria, values=list(szablony_opisow.keys()), state="readonly", width=50)
    dropdown.grid(row=4, column=1, pady=5)
    dropdown.set(list(szablony_opisow.keys())[0])
    selected_kategoria.trace("w", zaktualizuj_opis)

    tk.Label(frame, text="Opis:").grid(row=5, column=0, sticky="nw", pady=(10, 0))
    text_opis = tk.Text(frame, height=4, width=50, wrap="word")
    text_opis.grid(row=5, column=1, pady=5)

    tk.Label(frame, text="SEO tytuł:").grid(row=6, column=0, sticky="nw", pady=(10, 0))
    global text_seo_title
    text_seo_title = tk.Text(frame, height=2, width=50, wrap="word")
    text_seo_title.grid(row=6, column=1, pady=5)
    text_seo_title.insert(tk.END, "{nazwa} | Zacny Druk – Stylowe Dekoracje Ścienne")

    tk.Label(frame, text="SEO opis:").grid(row=7, column=0, sticky="nw", pady=(5, 0))
    global text_seo_description
    text_seo_description = tk.Text(frame, height=3, width=50, wrap="word")
    text_seo_description.grid(row=7, column=1, pady=5)
    text_seo_description.insert(tk.END, "Plakaty, mapy i inne zacne wydruki, którymi udekorujesz każde wnętrze. Bogaty wybór motywów i rozmiarów. Zobacz: {nazwa}!")

    tk.Label(frame, text="──────────────────────────────────────────────").grid(row=8, column=0, columnspan=2, pady=(10, 10))

    tk.Label(frame, text="Warianty i ceny:").grid(row=9, column=0, sticky="nw")
    wariant_frame = tk.Frame(frame)
    wariant_frame.grid(row=9, column=1, sticky="w")
    for i, wariant in enumerate(warianty_stale):
        tk.Label(wariant_frame, text=wariant).grid(row=i, column=0, sticky="e", padx=(0, 5), pady=2)
        entry = tk.Entry(wariant_frame, width=10)
        entry.grid(row=i, column=1, pady=2)
        pola_wariantow[wariant] = entry

    przyciski_frame = tk.Frame(wariant_frame)
    przyciski_frame.grid(row=len(warianty_stale), column=0, columnspan=2, pady=(10, 0))

    for typ, label in [
        ("BARDZO TANI", "BARDZO TANI"),
        ("TANI", "TANI"),
        ("NORMALNY", "NORMALNY"),
        ("DROGI", "DROGI")
    ]:
        btn = tk.Button(przyciski_frame, text=label, width=12, command=lambda t=typ: ustaw_ceny(t))
        btn.pack(side="left", padx=5)
        przyciski_cennika[typ] = btn


    tk.Label(frame, text="Folder z obrazkami:").grid(row=10, column=0, sticky="w", pady=(10, 0))
    folder_var = tk.StringVar()
    folder_frame = tk.Frame(frame)
    folder_frame.grid(row=10, column=1, sticky="w", pady=(10, 0))
    folder_entry = tk.Entry(folder_frame, textvariable=folder_var, width=40, state="readonly")
    folder_entry.pack(side="left", padx=(0, 5))
    tk.Button(folder_frame, text="Wybierz...", command=lambda: wybierz_folder(folder_var)).pack(side="left")

    przyciski_frame = tk.Frame(frame)
    przyciski_frame.grid(row=11, column=0, columnspan=2, pady=20, sticky="ew")


    tk.Button(
        przyciski_frame,
        text="🔁 Odśwież token JWT",
        bg="#ffe599",
        command=klik_odswiez_token
    ).pack(side="left", padx=5)

    tk.Button(
        przyciski_frame,
        text="✅ Zatwierdź dane i kontynuuj",
        font=("Helvetica", 11, "bold"),
        bg="#b9fbc0",
        command=zatwierdz_dane
    ).pack(side="right", padx=5)

    tk.Label(frame, text="Log programu:").grid(row=12, column=0, sticky="nw", pady=(0, 5))
    log_frame = tk.Frame(frame)
    log_frame.grid(row=12, column=1, sticky="w")
    text_log = tk.Text(log_frame, height=10, width=60, state="disabled", wrap="word")
    text_log.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(log_frame, command=text_log.yview)
    scrollbar.pack(side="right", fill="y")
    text_log.config(yscrollcommand=scrollbar.set)

    root.mainloop()
    root.destroy()

    return dane_uzytkownika


def zaktualizuj_opis(*args):
    wybrana = selected_kategoria.get()
    opis = szablony_opisow.get(wybrana, "")
    text_opis.config(state="normal")
    text_opis.delete("1.0", tk.END)
    text_opis.insert(tk.END, opis)

def wybierz_folder(var):
    folder_path = filedialog.askdirectory(title="Wybierz folder z obrazkami")
    if folder_path:
        var.set(folder_path)


def zatwierdz_dane():
    global dane_uzytkownika

    kategoria = selected_kategoria.get()
    opis_szablon = text_opis.get("1.0", tk.END).strip()
    seo_title_template = text_seo_title.get("1.0", tk.END).strip()
    seo_description_template = text_seo_description.get("1.0", tk.END).strip()

    if not kategoria or not opis_szablon or not seo_title_template or not seo_description_template:
        messagebox.showerror("Błąd", "Uzupełnij wszystkie wymagane pola.")
        return

    warianty = {}
    for wariant, entry in pola_wariantow.items():
        cena = entry.get().strip()
        if not cena:
            messagebox.showerror("Błąd", f"Uzupełnij cenę dla wariantu: {wariant}")
            return
        warianty[wariant] = cena

    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showerror("Błąd", "Wybierz folder z obrazkami.")
        return

    dane_uzytkownika = {
        "kategoria": kategoria,
        "opis_szablon": opis_szablon,
        "seo_title_template": seo_title_template,
        "seo_description_template": seo_description_template,
        "warianty": warianty,
        "tryb": tryb.get(),
        "folder": folder_path
    }

    if os.path.exists("log.txt"):
        with open("log.txt", "r", encoding="utf-8") as f:
            log_content = f.read()
        text_log.config(state="normal")
        text_log.delete("1.0", tk.END)
        text_log.insert(tk.END, log_content)
        text_log.config(state="disabled")

    root.quit()


if __name__ == "__main__":
    dane = uruchom_gui()
    print("✅ Dane z GUI:", dane)
