import os
import random
import shutil

# Ścieżka do głównego folderu z danymi
base_dir = 'data/leafsnap-dataset/images'
segmented_base_dir = 'data/leafsnap-dataset/segmented'
# Folder docelowy
output_dir = 'data/dataset'

# Ustalenie proporcji do podziału zdjęć
train_ratio = 0.7       # 70%
validation_ratio = 0.15     # 15%
test_ratio = 0.15       # 15%

# Sprawdzenie, czy folder wyjściowy już istnieje
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Tworzymy główne foldery "images" i "segmented" w folderze docelowym
images_output_dir = os.path.join(output_dir, 'images')
segmented_output_dir = os.path.join(output_dir, 'segmented')

os.makedirs(images_output_dir, exist_ok=True)
os.makedirs(segmented_output_dir, exist_ok=True)

# Iterowanie przez foldery 'field' i 'lab'
for source in ['field', 'lab']:
    source_dir = os.path.join(base_dir, source)
    segmented_source_dir = os.path.join(segmented_base_dir, source)

    for species in os.listdir(source_dir):
        species_dir = os.path.join(source_dir, species)
        segmented_species_dir = os.path.join(segmented_source_dir, species)

        # Sprawdzenie, że to folder, a nie plik
        if os.path.isdir(species_dir) and os.path.isdir(segmented_species_dir):
            # Utworzenie odpowiednich folderów w docelowym katalogu
            train_dir = os.path.join(images_output_dir, 'train', source, species)
            validation_dir = os.path.join(images_output_dir, 'validation', source, species)
            test_dir = os.path.join(images_output_dir, 'test', source, species)

            # Tworzenie folderów w folderze 'segmented'
            segmented_train_dir = os.path.join(segmented_output_dir, 'train', source, species)
            segmented_validation_dir = os.path.join(segmented_output_dir, 'validation', source, species)
            segmented_test_dir = os.path.join(segmented_output_dir, 'test', source, species)

            # Tworzenie odpowiedniej struktury folderów
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(validation_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            os.makedirs(segmented_train_dir, exist_ok=True)
            os.makedirs(segmented_validation_dir, exist_ok=True)
            os.makedirs(segmented_test_dir, exist_ok=True)

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
                # Kopiowanie oryginalnego obrazu do folderu 'images'
                shutil.copy(os.path.join(species_dir, image), train_dir)
                # Kopiowanie odpowiadającego obrazu segmentowanego do folderu 'segmented'
                segmented_image_name = image.replace('.jpg', '.png').replace('.jpeg', '.png')
                shutil.copy(os.path.join(segmented_species_dir, segmented_image_name), segmented_train_dir)

            for image in validation_images:
                # Kopiowanie oryginalnego obrazu do folderu 'images'
                shutil.copy(os.path.join(species_dir, image), validation_dir)
                # Kopiowanie odpowiadającego obrazu segmentowanego do folderu 'segmented'
                segmented_image_name = image.replace('.jpg', '.png').replace('.jpeg', '.png')
                shutil.copy(os.path.join(segmented_species_dir, segmented_image_name), segmented_validation_dir)

            for image in test_images:
                # Kopiowanie oryginalnego obrazu do folderu 'images'
                shutil.copy(os.path.join(species_dir, image), test_dir)
                # Kopiowanie odpowiadającego obrazu segmentowanego do folderu 'segmented'
                segmented_image_name = image.replace('.jpg', '.png').replace('.jpeg', '.png')
                shutil.copy(os.path.join(segmented_species_dir, segmented_image_name), segmented_test_dir)

print("Podział danych zakończony.")

