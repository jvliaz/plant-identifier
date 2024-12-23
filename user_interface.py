import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf


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
            filetypes=[
                ("JPEG Files", "*.jpg"),
                ("JPEG Files", "*.jpeg"),
                ("PNG Files", "*.png"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return  # Użytkownik anulował wybór

        global loaded_img  # Przechowuj oryginalny obraz
        loaded_img = Image.open(file_path)

        # Zmiana rozmiaru do wyświetlania
        display_img = loaded_img.resize((200, 200))
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
        img = np.array(img) / 255.0  # Normalizacja pikseli (0-1)
        img = np.expand_dims(img, axis=0)  # Dodanie wymiaru batch

        # Przewidywanie klasy
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
root.geometry("550x800")
root.configure(bg="#4f4f4f")

# === Logo aplikacji ===
logo_path = os.path.join(os.getcwd(), "images", "logo.png")
try:
    logo = Image.open(logo_path).resize((300, 300))
    logo = ImageTk.PhotoImage(logo)
    tk.Label(root, image=logo, bg="#4f4f4f").pack(pady=10)
except FileNotFoundError:
    tk.Label(root, text="Nie znaleziono logo!", font=("Helvetica", 18, "bold"), bg="#4f4f4f", fg="red").pack(pady=10)

# === Tytuł i ramka ===
frame = tk.Frame(root, bg="#4f4f4f")
frame.pack(pady=10)

tk.Label(
    frame, text="Załaduj zdjęcie rośliny", font=("Helvetica", 18, "bold"), bg="#4f4f4f", fg="black"
).pack(pady=5)

# === Panel obrazu ===
panel = tk.Label(root, bg="#4f4f4f")
panel.pack(padx=5, pady=5)

# === Przyciski ===
load_button = tk.Button(
    frame, text="Wybierz zdjęcie", command=load_image, bg="#6BBF59", fg="black", font=("Helvetica", 14, "bold"),
    bd=1, relief="solid"
)
load_button.default_bg = "#6BBF59"
load_button.default_fg = "black"
load_button.pack(pady=5)
configure_hover_effects(load_button)

predict_button = tk.Button(
    root, text="Rozpoznaj roślinę", command=predict_plant, bg="#4682B4", fg="black", font=("Helvetica", 14, "bold"),
    bd=1, relief="solid"
)
predict_button.default_bg = "#4682B4"
predict_button.default_fg = "black"
predict_button.pack(pady=10)
configure_hover_effects(predict_button)

# === Pole tekstowe na wyniki ===
result_text = tk.Text(
    root, height=2, width=50, wrap="word", font=("Helvetica", 12), bg="#5e5e5e", fg="black",
    relief="solid", borderwidth=2
)
result_text.pack(pady=5)
result_text.insert("end", "Wyniki rozpoznawania pojawią się tutaj.")
result_text.configure(state="disabled")

# === Główna pętla aplikacji ===
root.mainloop()
