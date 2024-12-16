import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

# === Wczytanie modelu ===
try:
    model = tf.keras.models.load_model('model.keras')
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    class_names = ["acer_campestre", "acer_ginnala", "acer_negundo", "aesculus_glabra", "albizia_julibrissin", "amelanchier_arborea", "betula_nigra", "carya_cordiformis", "catalpa_speciosa", "corylus_colurna", "ficus_carica", "gleditsia_triacanthos", "koelreuteria_paniculata", "magnolia_stellata", "quercus_velutina"]  # Nazwy klas
except Exception as e:
    messagebox.showerror("Błąd", f"Nie udało się załadować modelu: {str(e)}")
    model = None


# === Funkcje aplikacji ===
def load_image():
    """
    Funkcja do ładowania obrazu i wyświetlania go w aplikacji.
    """
    try:
        # Otworzenie okna dialogowego do wyboru pliku
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("JPEG Files", "*.jpg"),
                ("JPEG Files", "*.jpeg"),
                ("PNG Files", "*.png"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return  # Użytkownik anulował wybór

        # Wczytaj obraz i zmień jego rozmiar
        global loaded_img  # Przechowuj oryginalny obraz
        loaded_img = Image.open(file_path)

        display_img = loaded_img.resize((200, 200))  # Dopasowanie do wyświetlania
        display_img = ImageTk.PhotoImage(display_img)

        # Wyświetl obraz w oknie
        panel.configure(image=display_img)
        panel.image = display_img
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
        print(f"Wymiary załadowanego obrazu: {img.size}")
        img = np.array(img) / 255.0  # Normalizacja pikseli (0-1)
        print(f"Zakres pikseli po normalizacji: min={np.min(img)}, max={np.max(img)}")
        img = np.expand_dims(img, axis=0)  # Dodanie wymiaru batch

        # Przewidywanie klasy za pomocą modelu
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = predictions[0][predicted_class] * 100

        result = f"Przewidywany gatunek: {class_names[predicted_class]}\nPewność: {confidence:.2f}%"
    except Exception as e:
        result = f"Błąd przewidywania: {str(e)}"

    # Wyświetl wynik w polu tekstowym
    result_text.configure(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("end", result)
    result_text.configure(state="disabled")


# === Funkcje obsługi efektów hover ===
def on_hover(event):
    event.widget.configure(bg="black", fg="white")


def on_leave(event):
    event.widget.configure(bg=event.widget.default_bg, fg=event.widget.default_fg)


# === Konfiguracja kolorów ===
bg_color = "#4f4f4f"
panel_bg_color = "#5e5e5e"
button_fg_color = "#000000"
text_fg_color = "#000000"
button_style = {
    "font": ("Helvetica", 14, "bold"),
    "bd": 1,
    "relief": "solid",
    "highlightbackground": "#000000",
    "highlightthickness": 1,
}


# === Główna konfiguracja GUI ===
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("550x750")
root.configure(bg=bg_color)

# === Logo aplikacji ===
logo_path = os.path.join(os.getcwd(), "images", "logo.png")
try:
    logo = Image.open(logo_path)
    logo = logo.resize((300, 300))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo, bg=bg_color)
    logo_label.image = logo
    logo_label.pack(pady=10)
except FileNotFoundError:
    tk.Label(
        root,
        text="Nie znaleziono logo!",
        font=("Helvetica", 18, "bold"),
        bg=bg_color,
        fg="red"
    ).pack(pady=10)

# === Ramka na tytuł i przyciski ===
frame = tk.Frame(root, bg=bg_color)
frame.pack(pady=10)

title_label = tk.Label(
    frame,
    text="Załaduj zdjęcie rośliny",
    font=("Helvetica", 18, "bold"),
    bg=bg_color,
    fg=text_fg_color
)
title_label.pack(pady=5)

# === Panel do wyświetlania obrazu ===
panel = tk.Label(root, bg=bg_color)
panel.pack(padx=5, pady=5)

# === Przyciski ===
# Wybierz zdjęcie
load_button = tk.Button(
    frame,
    text="Wybierz zdjęcie",
    command=load_image,
    bg="#6BBF59",
    fg=button_fg_color,
    **button_style
)
load_button.default_bg = "#6BBF59"
load_button.default_fg = button_fg_color
load_button.pack(pady=5)
load_button.bind("<Enter>", on_hover)
load_button.bind("<Leave>", on_leave)

# Rozpoznaj roślinę
predict_button = tk.Button(
    root,
    text="Rozpoznaj roślinę",
    command=predict_plant,
    bg="#4682B4",
    fg=button_fg_color,
    **button_style
)
predict_button.default_bg = "#4682B4"
predict_button.default_fg = button_fg_color
predict_button.pack(pady=10)
predict_button.bind("<Enter>", on_hover)
predict_button.bind("<Leave>", on_leave)

# === Obszar tekstowy na wyniki ===
result_text = tk.Text(
    root,
    height=2,
    width=50,
    wrap="word",
    font=("Helvetica", 12),
    bg=panel_bg_color,
    fg=text_fg_color,
    relief="solid",
    borderwidth=2
)
result_text.pack(pady=5)
result_text.insert("end", "Wyniki rozpoznawania pojawią się tutaj.")
result_text.configure(state="disabled")

# === Główna pętla aplikacji ===
root.mainloop()
