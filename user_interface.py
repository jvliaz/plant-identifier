import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


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
        img = Image.open(file_path)
        img = img.resize((200, 200))  # Dopasowanie do wymaganego rozmiaru
        img = ImageTk.PhotoImage(img)

        # Wyświetl obraz w oknie
        panel.configure(image=img)
        panel.image = img
    except Exception as e:
        # Obsługa błędów podczas ładowania obrazu
        messagebox.showerror("Błąd", f"Nie udało się załadować obrazu: {str(e)}")


def predict_plant(img):
    """
    Funkcja do przewidywania gatunku rośliny na podstawie obrazu.
    """
    # Dopasowanie obrazu do wymagań modelu
    img = img.resize((128, 128))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)  # Dodanie wymiaru batch
    # W tym miejscu należy wstawić kod obsługujący model predykcji
    # predicted_class = model.predict(img)
    return "Przewidywany gatunek: "  # Zwracany przykładowy wynik


# === Funkcje obsługi efektów hover ===
def on_hover(event):
    """
    Zmiana koloru przycisku na czarny i tekstu na biały po najechaniu kursorem.
    """
    event.widget.configure(bg="black", fg="white")

def on_leave(event):
    """
    Przywracanie domyślnych kolorów przycisku po opuszczeniu kursora.
    """
    event.widget.configure(bg=event.widget.default_bg, fg=event.widget.default_fg)


# === Konfiguracja kolorów ===
bg_color = "#4f4f4f"  # Jasnoszary
panel_bg_color = "#5e5e5e"  # Nieco jaśniejszy szary dla paneli
button_fg_color = "#000000"  # Czarny tekst dla przycisków
text_fg_color = "#000000"  # Czarny tekst dla innych elementów
button_style = {
    "font": ("Helvetica", 14, "bold"),
    "bd": 1,  # Grubość ramki
    "relief": "solid",  # Styl obramowania
    "highlightbackground": "#000000",  # Kolor obramowania
    "highlightthickness": 1,  # Grubość obramowania
}


# === Główna konfiguracja GUI ===
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("550x750")  # Wymiary okna
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
    command=lambda: messagebox.showinfo("Wynik", "Przewidywany gatunek: Brak modelu"),
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
