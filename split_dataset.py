import os
import random
import shutil


def split_dataset(base_dir, output_dir, train_ratio=0.7, validation_ratio=0.15, test_ratio=0.15):
    """
    Funkcja dzieląca zbiór danych na trzy podzbiory: train, validation, test.

    :param base_dir: Ścieżka do głównego folderu z danymi (folder zawierający 'field' i 'lab').
    :param output_dir: Folder docelowy, gdzie zostaną zapisane podzielone dane.
    :param train_ratio: Proporcja danych do zbioru treningowego (domyślnie 70%).
    :param validation_ratio: Proporcja danych do zbioru walidacyjnego (domyślnie 15%).
    :param test_ratio: Proporcja danych do zbioru testowego (domyślnie 15%).
    """
    # Sprawdzenie, czy folder wyjściowy już istnieje
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tworzymy główne foldery "images" w folderze docelowym
    images_output_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_output_dir, exist_ok=True)

    # Iterowanie przez foldery 'field' i 'lab'
    for source in ['field', 'lab']:
        source_dir = os.path.join(base_dir, source)

        for species in os.listdir(source_dir):
            species_dir = os.path.join(source_dir, species)

            # Sprawdzenie, że to folder, a nie plik
            if os.path.isdir(species_dir):
                # Utworzenie odpowiednich folderów w docelowym katalogu
                train_dir = os.path.join(images_output_dir, 'train', source, species)
                validation_dir = os.path.join(images_output_dir, 'validation', source, species)
                test_dir = os.path.join(images_output_dir, 'test', source, species)

                # Tworzenie odpowiedniej struktury folderów
                os.makedirs(train_dir, exist_ok=True)
                os.makedirs(validation_dir, exist_ok=True)
                os.makedirs(test_dir, exist_ok=True)

                # Uzyskanie listy plików w folderze gatunku
                images = os.listdir(species_dir)
                random.shuffle(images)  # Losowo przetasowanie listy

                # Obliczenie ilości zdjęć do podziału
                total_images = len(images)
                train_count = int(total_images * train_ratio)
                validation_count = int(total_images * validation_ratio)

                # Podzielenie danych
                train_images = images[:train_count]
                validation_images = images[train_count:train_count + validation_count]
                test_images = images[train_count + validation_count:]

                # Kopiowanie plików do odpowiednich folderów
                for image in train_images:
                    shutil.copy(os.path.join(species_dir, image), train_dir)

                for image in validation_images:
                    shutil.copy(os.path.join(species_dir, image), validation_dir)

                for image in test_images:
                    shutil.copy(os.path.join(species_dir, image), test_dir)

    print("Podział danych zakończony.")


# Wywołanie funkcji
base_dir = 'data/leafsnap-dataset/images'
output_dir = 'data/dataset'

# Uruchomienie funkcji
split_dataset(base_dir, output_dir)
