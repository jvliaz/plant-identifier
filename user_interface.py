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
        img = img.resize((128, 128))  # Dopasowanie do wymaganego rozmiaru
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


# === Główna konfiguracja GUI ===
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("650x800")  # Wymiary okna
root.configure(bg="#f0f0f0")

# === Logo aplikacji ===
logo_path = os.path.join(os.getcwd(), "images", "logo.png")
try:
    logo = Image.open(logo_path)
    logo = logo.resize((300, 300))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo, bg="#f0f0f0")
    logo_label.image = logo
    logo_label.pack(pady=10)
except FileNotFoundError:
    tk.Label(
        root,
        text="Nie znaleziono logo!",
        font=("Helvetica", 18, "bold"),
        bg="#f0f0f0",
        fg="red"
    ).pack(pady=10)

# === Ramka na tytuł i przyciski ===
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

label = tk.Label(
    frame,
    text="Załaduj zdjęcie rośliny",
    font=("Helvetica", 18, "bold"),
    bg="#f0f0f0",
    fg="#333333"
)
label.pack(pady=10)

# === Panel do wyświetlania obrazu ===
panel = tk.Label(root, bg="#ffffff", relief="solid", borderwidth=2)
panel.pack(padx=10, pady=10)

# === Przycisk do załadowania zdjęcia ===
button = tk.Button(
    frame,
    text="Wybierz zdjęcie",
    command=load_image,
    font=("Helvetica", 14, "bold"),
    bg="#4CAF50",
    fg="white"
)
button.pack(pady=10)

# === Przycisk do przewidywania gatunku rośliny ===
predict_button = tk.Button(
    root,
    text="Rozpoznaj roślinę",
    command=lambda: messagebox.showinfo("Wynik", "Przewidywany gatunek: Brak modelu"),
    font=("Helvetica", 14, "bold"),
    bg="#2196F3",
    fg="white"
)
predict_button.pack(pady=10)

# === Obszar tekstowy na wyniki ===
result_text = tk.Text(
    root,
    height=5,
    width=50,
    wrap="word",
    font=("Helvetica", 12),
    bg="#f9f9f9",
    fg="#333333"
)
result_text.pack(pady=10)
result_text.insert("end", "Wyniki rozpoznawania pojawią się tutaj.")
result_text.configure(state="disabled")

# === Główna pętla aplikacji ===
root.mainloop()
