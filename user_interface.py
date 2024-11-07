import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


# Funkcja do ładowania obrazu
def load_image():
    # Otworzenie okna dialogowego do wyboru pliku
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((128, 128))  # Zmieniamy rozmiar obrazu do 128x128 (lub rozmiar wymagany przez model)
        img = ImageTk.PhotoImage(img)

        # Wyświetl obraz w oknie
        panel.configure(image=img)
        panel.image = img

        # Możemy później dodać funkcję rozpoznawania roślin
        # np. result = predict_plant(file_path)


# Funkcja do przewidywania (do dodania po załadowaniu modelu)
def predict_plant(img):
    # Tu dodamy kod do przesyłania obrazu do modelu
    img = img.resize((128, 128))  # Dopasowanie obrazu do wymagań modelu
    img = np.array(img)
    img = np.expand_dims(img, axis=0)  # Dodajemy dodatkowy wymiar dla obrazu
    # predicted_class = model.predict(img)  # Tutaj wywołamy funkcję modelu do klasyfikacji
    return "Przewidywany gatunek: "  # Zwracany przykładowy wynik


# Utwórz główne okno aplikacji
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("500x500")  # Wymiary okna

# Dodaj etykietę
label = tk.Label(root, text="Załaduj zdjęcie rośliny", font=("Arial", 16))
label.pack(pady=10)

# Panel do wyświetlania obrazu
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Przycisk do załadowania zdjęcia
button = tk.Button(root, text="Wybierz zdjęcie", command=load_image, font=("Arial", 14))
button.pack(pady=20)

# Przycisk do przewidywania gatunku rośliny (tymczasowo tylko dla testów)
predict_button = tk.Button(root, text="Rozpoznaj roślinę",
                           command=lambda: messagebox.showinfo("Wynik", "Przewidywany gatunek: Brak modelu"),
                           font=("Arial", 14))
predict_button.pack(pady=10)

# Uruchomienie głównej pętli aplikacji
root.mainloop()