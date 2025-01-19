import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import webbrowser


# === Inicjalizacja modelu ===
def load_model():
    """
    Wczytuje model sieci neuronowej.
    """
    try:
        model = tf.keras.models.load_model('model.keras')
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        class_names = [
            "acer_campestre", "acer_ginnala", "acer_negundo", "aesculus_glabra", "albizia_julibrissin",
            "amelanchier_arborea", "betula_nigra", "carya_cordiformis", "catalpa_speciosa", "corylus_colurna",
            "ficus_carica", "gleditsia_triacanthos", "koelreuteria_paniculata", "magnolia_stellata", "quercus_velutina"
        ]
        return model, class_names
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się załadować modelu: {str(e)}")
        return None, []


model, class_names = load_model()


# === Funkcje aplikacji ===
def load_image():
    """
    Funkcja do ładowania obrazu i wyświetlania go w aplikacji.
    """
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"), ("PNG Files", "*.png"), ("All files", "*.*")]
        )
        if not file_path:
            return  # Użytkownik anulował wybór

        global loaded_img  # Przechowuj oryginalny obraz
        loaded_img = Image.open(file_path)

        # Zmiana rozmiaru do wyświetlania
        display_img = loaded_img.resize((300, 300))
        display_img = ImageTk.PhotoImage(display_img)

        # Wyświetl obraz w oknie
        panel.configure(image=display_img)
        panel.image = display_img

        # # Aktywacja przycisku "Rozpoznaj roślinę" po załadowaniu obrazu
        # predict_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się załadować obrazu: {str(e)}")


def predict_plant():
    """
    Funkcja do przewidywania gatunku rośliny na podstawie obrazu.
    """
    if not model:
        messagebox.showerror("Błąd", "Model nie został załadowany.")
        return

    if 'loaded_img' not in globals():
        messagebox.showerror("Błąd", "Nie załadowano żadnego obrazu.")
        return

    try:
        # Dopasowanie obrazu do wymagań modelu
        img = loaded_img.resize((128, 128))  # Dopasowanie do wejścia modelu
        img = np.array(img) / 255.0  # Normalizacja pikseli (0-1)
        img = np.expand_dims(img, axis=0)  # Dodanie wymiaru batch

        # Przewidywanie klasy
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = predictions[0][predicted_class] * 100

        result = f"Przewidywany gatunek: {class_names[predicted_class]}\nPewność: {confidence:.2f}%"
        show_description_and_link(predicted_class)  # Wyświetl opis i link po przewidywaniu
        enable_plant_button(class_names[predicted_class])  # Aktywuj przycisk dla rozpoznanego gatunku

    except Exception as e:
        result = f"Błąd przewidywania: {str(e)}"

    # Wyświetl wynik w polu tekstowym
    result_text.configure(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("end", result)
    result_text.configure(state="disabled")


# === Słownik z opisami roślin ===
plant_descriptions = {
    "acer_campestre": (
        "Klon polny to niewielkie drzewo liściaste, osiągające do 15 metrów wysokości. Ma charakterystyczne, "
        "pięcioklapowe liście i żółte kwiaty, które pojawiają się wiosną. Jest ceniony za odporność na różne warunki "
        "glebowe i często sadzony w parkach oraz w krajobrazie miejskim."
    ),
    "acer_ginnala": (
        "Klon amurski to małe drzewo lub krzew, osiągające wysokość do 10 metrów. Wyróżnia się intensywnie czerwonymi "
        "liśćmi jesienią. Pochodzi z północno-wschodniej Azji, jest odporny na mrozy i ceniony za dekoracyjny wygląd."
    ),
    "acer_negundo": (
        "Klon jesionolistny to szybko rosnące drzewo o wysokości do 20 metrów. Ma złożone liście przypominające liście "
        "jesionu. Jest powszechnie występujący w Ameryce Północnej, zwłaszcza wzdłuż rzek i terenów zalewowych."
    ),
    "aesculus_glabra": (
        "Kasztanowiec gładki to średniej wielkości drzewo dorastające do 25 metrów. Ma dużą, dłoniastozłożoną korę "
        "i żółte kwiatostany. Jest symbolem stanu Ohio w USA, a jego orzechy, po odpowiedniej obróbce, wykorzystywano "
        "w medycynie ludowej."
    ),
    "albizia_julibrissin": (
        "Albicja jedwabista to szybko rosnące drzewo osiągające wysokość do 12 metrów, z pierzastymi liśćmi "
        "i różowymi kwiatami. Pochodzi z Azji i przyciąga motyle oraz pszczoły dzięki swojej egzotycznej urodzie."
    ),
    "amelanchier_arborea": (
        "Świdośliwa kłosowa to małe drzewo dorastające do 12 metrów. Ma białe kwiaty wczesną wiosną oraz jadalne, "
        "ciemnopurpurowe owoce latem. Jest ważnym źródłem pożywienia dla ptaków i owadów zapylających."
    ),
    "betula_nigra": (
        "Brzoza czarna to średniej wielkości drzewo dorastające do 25 metrów. Charakteryzuje się łuszczącą się, "
        "cynamonową korą. Preferuje wilgotne siedliska wzdłuż rzek, jest odporna na choroby i szkodniki."
    ),
    "carya_cordiformis": (
        "Orzesznik gorzki to duże drzewo dorastające do 30 metrów. Ma gładką, szarą korę i złożone liście. Produkuje "
        "gorzkawe orzechy, które są pożywieniem dla dzikich zwierząt. Drewno jest cenione za wytrzymałość."
    ),
    "catalpa_speciosa": (
        "Surmia wielkokwiatowa to szybko rosnące drzewo dorastające do 30 metrów. Ma duże sercowate liście i białe "
        "kwiaty w wiechach. Jest odporna na trudne warunki i często sadzona jako drzewo ozdobne w parkach."
    ),
    "corylus_colurna": (
        "Leszczyna turecka to duże drzewo dorastające do 25 metrów. Ma prosty pień i gęstą koronę. Produkuje "
        "jadalne orzechy, a jej drewno jest cenione w meblarstwie. Jest odporna na zanieczyszczenia i często sadzona "
        "jako drzewo ozdobne."
    ),
    "ficus_carica": (
        "Figowiec pospolity to małe drzewo dorastające do 10 metrów. Ma klapowane liście i jadalne owoce - figi. "
        "Jest jednym z najstarszych roślin uprawnych, cenionym za smak owoców i łatwość uprawy w różnych warunkach."
    ),
    "gleditsia_triacanthos": (
        "Glediczja trójcierniowa to drzewo z rodziny bobowatych, pochodzące z Ameryki Północnej. Rośnie w pobliżu "
        "rzek, tworząc zarośla. Jest uprawiana w Polsce jako roślina ozdobna, ale w niektórych regionach uznawana "
        "za inwazyjną."
    ),
    "koelreuteria_paniculata": (
        "Roztrzeplin wiechowaty to drzewo o wyjątkowym kwitnieniu i dekoracyjnych owocach przypominających lampiony. "
        "Występuje naturalnie w Chinach i Korei, cenione za efektowny wygląd."
    ),
    "magnolia_stellata": (
        "Magnolia gwiaździsta to drzewo lub krzew pochodzący z Japonii. Zachwyca delikatnymi, gwiaździstymi kwiatami. "
        "Często sadzona w ogrodach, w Polsce szczególnie w parkach."
    ),
    "quercus_velutina": (
        "Dąb barwierski to drzewo występujące w Ameryce Północnej. Jego drewno jest cenione w przemyśle, a kora "
        "stanowi źródło barwników. Cechuje się ciemną, chropowatą korą."
    )
}

# === Słownik z linkami do Wikipedii ===
plant_links = {
    "acer_campestre": "https://pl.wikipedia.org/wiki/Klon_polny",
    "acer_ginnala": "https://pl.wikipedia.org/wiki/Klon_ginnala",
    "acer_negundo": "https://pl.wikipedia.org/wiki/Klon_jesionolistny",
    "aesculus_glabra": "https://pl.wikipedia.org/wiki/Kasztanowiec",
    "albizia_julibrissin": "https://pl.wikipedia.org/wiki/Albicja_biało-różowa",
    "amelanchier_arborea": "https://pl.wikipedia.org/wiki/Świdośliwa",
    "betula_nigra": "https://pl.wikipedia.org/wiki/Brzoza_nadrzeczna",
    "carya_cordiformis": "https://pl.wikipedia.org/wiki/Orzesznik_gorzki",
    "catalpa_speciosa": "https://pl.wikipedia.org/wiki/Surmia_wielkokwiatowa",
    "corylus_colurna": "https://pl.wikipedia.org/wiki/Leszczyna_turecka",
    "ficus_carica": "https://pl.wikipedia.org/wiki/Figowiec_pospolity",
    "gleditsia_triacanthos": "https://pl.wikipedia.org/wiki/Glediczja_trójcierniowa",
    "koelreuteria_paniculata": "https://pl.wikipedia.org/wiki/Roztrzeplin_wiechowaty",
    "magnolia_stellata": "https://pl.wikipedia.org/wiki/Magnolia_gwiaździsta",
    "quercus_velutina": "https://pl.wikipedia.org/wiki/Dąb_barwierski"
}


# === Funkcja do wyświetlania opisu i linku ===
def show_description_and_link(predicted_class):
    """
    Pokazuje krótki opis rośliny oraz aktywuje link do Wikipedii po przewidywaniu.
    """
    plant_name = class_names[predicted_class]
    description = plant_descriptions.get(plant_name, "Opis niedostępny.")
    link = plant_links.get(plant_name, "#")  # Domyślnie '#', jeśli brak linku

    # Wyświetl opis w polu tekstowym
    description_text.configure(state="normal")
    description_text.delete("1.0", "end")
    description_text.insert("end", description)
    description_text.configure(state="disabled")

    # Ustaw link do Wikipedii
    link_button.configure(state=tk.NORMAL, command=lambda: open_link(plant_name))


# Funkcja otwierająca link w przeglądarce
def open_link(plant_name):
    url = plant_links.get(plant_name, "#")
    webbrowser.open(url)


# Funkcja do pokazania przycisku tylko dla rozpoznanej rośliny
def enable_plant_button(plant_name):
    """
    Ta funkcja aktywuje przycisk oraz wyświetla odpowiedni opis rośliny.
    """
    link_button.config(state=tk.NORMAL)  # Aktywuje przycisk z linkiem do Wikipedii


def configure_hover_effects(button):
    """
    Dodaje efekty hover do przycisku.
    """
    def on_hover(event):
        event.widget.configure(bg="black", fg="white")

    def on_leave(event):
        event.widget.configure(bg=button.default_bg, fg=button.default_fg)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)


# === Konfiguracja GUI ===
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("900x1200")
root.configure(bg="#4f4f4f")

# === Logo aplikacji ===
logo_path = os.path.join(os.getcwd(), "images", "logo.png")
try:
    logo = Image.open(logo_path).resize((400, 400))
    logo = ImageTk.PhotoImage(logo)
    tk.Label(
        root, image=logo, bg="#4f4f4f"
    ).pack(pady=10)
except FileNotFoundError:
    tk.Label(
        root, text="Nie znaleziono logo!", font=("Comic Sans MS", 14, "bold"), bg="#4f4f4f", fg="red"
    ).pack(pady=10)

# === Tytuł i ramka ===
frame = tk.Frame(root, bg="#4f4f4f")
frame.pack(pady=10)
tk.Label(
    frame, text="ZAŁADUJ ZDJĘCIE ROŚLINY", font=("Gill Sans Ultra Bold", 28), bg="#4f4f4f", fg="black"
).pack(pady=5)

# === Panel obrazu ===
panel = tk.Label(root, bg="#4f4f4f")
panel.pack(padx=5, pady=5)

# === Przyciski ===
load_button = tk.Button(
    frame, text="Wybierz zdjęcie", command=load_image, bg="#1D3E2C", fg="black",
    font=("Gill Sans Ultra Bold", 14, "bold"), bd=1, relief="solid"
)
load_button.default_bg = "#1D3E2C"
load_button.default_fg = "black"
load_button.pack(pady=5)
configure_hover_effects(load_button)

predict_button = tk.Button(
    root, text="Rozpoznaj roślinę", command=predict_plant, bg="#2E512E", fg="black",
    font=("Gill Sans Ultra Bold", 14, "bold"), bd=1, relief="solid"
)
predict_button.default_bg = "#2E512E"
predict_button.default_fg = "black"
predict_button.pack(pady=5)
configure_hover_effects(predict_button)

# === Pole tekstowe na wynik ===
result_text = tk.Text(
    root, height=2, width=60, wrap="word", font=("Gill Sans Ultra Bold", 12), bg="#7B7870", fg="black",
    relief="solid", borderwidth=1
)
result_text.pack(pady=5)
result_text.insert("end", "Wyniki rozpoznawania pojawią się tutaj.")
result_text.configure(state="disabled")

# === Pole tekstowe na opis rośliny ===
description_text = tk.Text(
    root, height=4, width=60, wrap="word", font=("Gill Sans Ultra Bold", 12), bg="#7B7870", fg="black",
    relief="solid", borderwidth=1
)
description_text.pack(pady=5)
description_text.insert("end", "Opis rośliny pojawi się tutaj.")
description_text.configure(state="disabled")

# === Przycisk "Czytaj więcej" ===
link_button = tk.Button(
    root, text="Czytaj więcej", state=tk.DISABLED, bg="#2E512E", fg="black",
    font=("Gill Sans Ultra Bold", 14, "bold"), bd=1, relief="solid"
)
link_button.default_bg = "#2E512E"
link_button.default_fg = "black"
link_button.pack(pady=5)
configure_hover_effects(link_button)

# === Główna pętla aplikacji ===
root.mainloop()
