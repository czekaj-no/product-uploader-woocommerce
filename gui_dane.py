import os
from dotenv import load_dotenv

# Wczytanie zmiennych z pliku .env
load_dotenv()

# Przypisanie zmiennych do zmiennych w Pythonie
API_URL = os.getenv("WC_API_URL")
API_KEY = os.getenv("WC_API_KEY")
API_SECRET = os.getenv("WC_API_SECRET")

#Sprawdzenie, czy zmienne ładują sie poprawnie
print("🔐 WC_API_URL:", API_URL)
print("🔑 WC_API_KEY:", API_KEY)
print("🧷 WC_API_SECRET:", API_SECRET)

PRODUCTS_FOLDER = "product_images"

#Wybieramy dane

import tkinter as tk
from tkinter import messagebox, ttk

# Kategorie i przypisane szablony opisów
szablony_opisow = {
    "plakaty": "Plakat {nazwa} to wyjątkowa dekoracja, która doda charakteru Twojemu wnętrzu. Motyw: {nazwa}, dostępny w wielu formatach.",
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

def zaktualizuj_opis(*args):
    wybrana = selected_kategoria.get()
    opis = szablony_opisow.get(wybrana, "")
    text_opis.config(state="normal")
    text_opis.delete("1.0", tk.END)
    text_opis.insert(tk.END, opis)
    text_opis.config(state="disabled")

def zatwierdz_dane():
    kategoria = selected_kategoria.get()
    opis_szablon = text_opis.get("1.0", tk.END).strip()

    if not kategoria or not opis_szablon:
        messagebox.showerror("Błąd", "Uzupełnij wszystkie pola.")
        return

    warianty = {}
    for wariant, entry in pola_wariantow.items():
        cena = entry.get().strip()
        if not cena:
            messagebox.showerror("Błąd", f"Uzupełnij cenę dla wariantu: {wariant}")
            return
        warianty[wariant] = cena

    dane = {
        "kategoria": kategoria,
        "opis_szablon": opis_szablon,
        "warianty": warianty
    }

    print("\n✅ DANE WPISANE PRZEZ UŻYTKOWNIKA:")
    print(dane)

    root.destroy()

# GUI
root = tk.Tk()
root.title("Dane produktów, które wgrywasz")


# Kategoria
tk.Label(root, text="Kategoria produktu:").grid(row=0, column=0, sticky="w")
selected_kategoria = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=selected_kategoria, values=list(szablony_opisow.keys()), state="readonly", width=40)
dropdown.grid(row=0, column=1, pady=5)
dropdown.set(list(szablony_opisow.keys())[0])
selected_kategoria.trace("w", zaktualizuj_opis)

# Opis (readonly)
tk.Label(root, text="Opis produktu (szablon):").grid(row=1, column=0, sticky="nw")
text_opis = tk.Text(root, height=5, width=60, state="disabled", wrap="word")
text_opis.grid(row=1, column=1, pady=5)

# Warianty i ceny
tk.Label(root, text="Warianty i ceny:").grid(row=2, column=0, sticky="nw", pady=(10, 0))
pola_wariantow = {}
for i, wariant in enumerate(warianty_stale):
    tk.Label(root, text=f"{wariant}").grid(row=3 + i, column=0, sticky="e")
    entry = tk.Entry(root, width=10)
    entry.grid(row=3 + i, column=1, sticky="w")
    pola_wariantow[wariant] = entry

# Przycisk zatwierdzający
tk.Button(root, text="Zatwierdź dane", command=zatwierdz_dane).grid(row=9, column=0, columnspan=2, pady=15)

# Start GUI
zaktualizuj_opis()
root.mainloop()
