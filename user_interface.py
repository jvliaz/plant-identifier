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


# Główne okno
root = tk.Tk()
root.title("Rozpoznawanie Roślin")
root.geometry("500x600")  # Wymiary okna
root.configure(bg="#f0f0f0")

# Logo aplikacji
logo = Image.open("images/logo.png")
logo = logo.resize((300, 300))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image=logo, bg="#f0f0f0")
logo_label.image = logo
logo_label.pack(pady=10)

# Ramka i etykiety
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

label = tk.Label(frame, text="Załaduj zdjęcie rośliny", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333333")
label.pack(pady=10)

# Panel do wyświetlania obrazu
# panel = tk.Label(root, bg="#ffffff", relief="solid", borderwidth=2)
# panel.pack(padx=10, pady=10)

# Przycisk do załadowania zdjęcia
button = tk.Button(frame, text="Wybierz zdjęcie", command=load_image, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white")
button.pack(pady=10)

# Przycisk do przewidywania gatunku rośliny (tymczasowo tylko dla testów)
predict_button = tk.Button(root, text="Rozpoznaj roślinę",
                           command=lambda: messagebox.showinfo("Wynik", "Przewidywany gatunek: Brak modelu"),
                           font=("Helvetica", 14, "bold"), bg="#2196F3", fg="white")
predict_button.pack(pady=10)

# Obszar tekstowy
result_text = tk.Text(root, height=5, width=50, wrap="word", font=("Helvetica", 12), bg="#f9f9f9", fg="#333333")
result_text.pack(pady=10)
result_text.insert("end", "Wyniki rozpoznawania pojawią się tutaj.")
result_text.configure(state="disabled")

# Uruchomienie głównej pętli aplikacji
root.mainloop()