import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from dotenv import load_dotenv

# 🔽 Globalne zmienne
text_seo_title = None
text_seo_description = None
dane_uzytkownika = None  # finalne dane użytkownika
folder_var = None
pola_wariantow = {}

# 🔽 Wczytanie .env
load_dotenv()
API_URL = os.getenv("WC_API_URL")
API_KEY = os.getenv("WC_API_KEY")
API_SECRET = os.getenv("WC_API_SECRET")

# 🔽 Szablony i dane
szablony_opisow = {
    "plakaty": "{nazwa} to wyjątkowa dekoracja, która doda charakteru Twojemu wnętrzu. Motyw: {nazwa}, dostępny w wielu formatach.",
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


def uruchom_gui():
    global root, text_log, selected_kategoria, text_opis, pola_wariantow, tryb, folder_var
    root = tk.Tk()
    root.title("ZACNY PRODUCTS 3000")
    root.geometry("750x750")
    root.option_add("*Font", "Helvetica 10")

    tryb = tk.StringVar(value="test")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # 🔹 Tytuł
    tk.Label(frame, text="🖼️ ZACNY PRODUCTS 3000", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # 🔹 Tryb działania
    tk.Label(frame, text="Tryb działania:").grid(row=1, column=0, sticky="w")
    tk.Radiobutton(frame, text="TEST (tylko podgląd)", variable=tryb, value="test").grid(row=2, column=0, sticky="w")
    tk.Radiobutton(frame, text="WRZUCAMY PRODUKTY", variable=tryb, value="live").grid(row=3, column=0, sticky="w")

    # 🔹 Kategoria
    tk.Label(frame, text="Kategoria produktu:").grid(row=4, column=0, sticky="w", pady=(10, 0))
    selected_kategoria = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=selected_kategoria, values=list(szablony_opisow.keys()), state="readonly", width=50)
    dropdown.grid(row=4, column=1, pady=5)
    dropdown.set(list(szablony_opisow.keys())[0])
    selected_kategoria.trace("w", zaktualizuj_opis)

    # 🔹 Opis
    tk.Label(frame, text="Opis produktu (szablon):").grid(row=5, column=0, sticky="nw", pady=(10, 0))
    text_opis = tk.Text(frame, height=4, width=50, state="disabled", wrap="word")
    text_opis.grid(row=5, column=1, pady=5)

    # 🔹 SEO tytuł
    tk.Label(frame, text="SEO tytuł (szablon):").grid(row=6, column=0, sticky="nw", pady=(10, 0))
    global text_seo_title
    text_seo_title = tk.Text(frame, height=2, width=50, wrap="word")
    text_seo_title.grid(row=6, column=1, pady=5)
    text_seo_title.insert(tk.END, "Plakat {nazwa} – dekoracja z charakterem | Zacny Druk")

    # 🔹 SEO opis
    tk.Label(frame, text="SEO opis (szablon):").grid(row=7, column=0, sticky="nw", pady=(5, 0))
    global text_seo_description
    text_seo_description = tk.Text(frame, height=3, width=50, wrap="word")
    text_seo_description.grid(row=7, column=1, pady=5)
    text_seo_description.insert(tk.END, "Zobacz wyjątkowy plakat {nazwa}. Idealna ozdoba i pomysł na prezent. Druk na wysokiej jakości papierze.")

    # 🔹 Linia oddzielająca
    tk.Label(frame, text="──────────────────────────────────────────────").grid(row=8, column=0, columnspan=2, pady=(10, 10))

    # 🔹 Warianty
    tk.Label(frame, text="Warianty i ceny:").grid(row=9, column=0, sticky="nw")
    wariant_frame = tk.Frame(frame)
    wariant_frame.grid(row=9, column=1, sticky="w")
    for i, wariant in enumerate(warianty_stale):
        tk.Label(wariant_frame, text=wariant).grid(row=i, column=0, sticky="e", padx=(0, 5), pady=2)
        entry = tk.Entry(wariant_frame, width=10)
        entry.grid(row=i, column=1, pady=2)
        pola_wariantow[wariant] = entry

    # 🔹 Folder
    tk.Label(frame, text="Folder z obrazkami:").grid(row=10, column=0, sticky="w", pady=(10, 0))
    folder_var = tk.StringVar()
    folder_frame = tk.Frame(frame)
    folder_frame.grid(row=10, column=1, sticky="w", pady=(10, 0))
    folder_entry = tk.Entry(folder_frame, textvariable=folder_var, width=40, state="readonly")
    folder_entry.pack(side="left", padx=(0, 5))
    tk.Button(folder_frame, text="Wybierz...", command=lambda: wybierz_folder(folder_var)).pack(side="left")

    # 🔹 Przycisk zatwierdzający
    tk.Button(frame, text="✅ Zatwierdź dane i kontynuuj", font=("Helvetica", 11, "bold"), bg="#b9fbc0", command=zatwierdz_dane).grid(row=11, column=0, columnspan=2, pady=20)

    # 🔹 Log programu
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
    text_opis.config(state="disabled")


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

    # Log
    if os.path.exists("log.txt"):
        with open("log.txt", "r", encoding="utf-8") as f:
            log_content = f.read()
        text_log.config(state="normal")
        text_log.delete("1.0", tk.END)
        text_log.insert(tk.END, log_content)
        text_log.config(state="disabled")

    root.quit()


# 🔹 Główne uruchomienie
if __name__ == "__main__":
    dane = uruchom_gui()
    print("✅ Dane z GUI:", dane)
