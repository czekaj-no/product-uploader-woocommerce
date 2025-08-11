import tkinter as tk
from tkinter import ttk

def pokaz_demo(produkty):
    demo = tk.Tk()
    demo.title("Tryb testowy – podgląd produktów")
    demo.geometry("1000x700")

    canvas = tk.Canvas(demo)
    scrollbar = ttk.Scrollbar(demo, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    header = ttk.Label(scrollable_frame, text="📋 Podgląd załadowanych produktów", font=("Segoe UI", 14, "bold"))
    header.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

    for i, produkt in enumerate(produkty, start=1):
        frame = ttk.LabelFrame(scrollable_frame, text=f"📦 Produkt {i}: {produkt['nazwa']}", padding=10)
        frame.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
        frame.columnconfigure(0, weight=1)

        opis = produkt['opis']
        kategoria = produkt['kategoria']
        glowne = produkt['glowne_zdjecie']
        galeria = ", ".join(produkt['galeria']) if produkt['galeria'] else "Brak"
        warianty = produkt['warianty']

        seo_title = produkt.get('seo_title', 'brak')
        seo_description = produkt.get('seo_description', 'brak')
        fraza = produkt.get('fraza_kluczowa', 'brak')
        alt = produkt.get('alt', 'brak')

        ttk.Label(frame, text=f"📝 Opis: {opis}", wraplength=900, justify="left").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"📂 Kategoria: {kategoria}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"🖼️ Główne zdjęcie: {glowne}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"🖼️ Galeria: {galeria}").pack(anchor="w", pady=2)

        ttk.Label(frame, text=f"🔑 Fraza kluczowa: {fraza}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"🔖 SEO title: {seo_title}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"📄 SEO opis: {seo_description}", wraplength=900, justify="left").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"🖼️ ALT zdjęcia: {alt}").pack(anchor="w", pady=2)

        ttk.Label(frame, text="💰 Warianty:").pack(anchor="w", pady=(10, 0))
        for wariant, cena in warianty.items():
            ttk.Label(frame, text=f"   - {wariant}: {cena} zł").pack(anchor="w")

    demo.mainloop()
