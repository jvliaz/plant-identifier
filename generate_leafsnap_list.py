import os

# Ustalenie lokalizacji głównego folderu z danymi
images_base_dir = 'data/leafsnap-dataset/images'  # Ścieżka do folderu z obrazami
segmented_base_dir = 'data/leafsnap-dataset/segmented'  # Ścieżka do folderu z segmentowanymi obrazami
output_file = 'data/leafsnap-dataset/leafsnap-dataset-images.txt'


# Otworzenie pliku wyjściowego do zapisu
with open(output_file, 'w') as f:
    # Zapisanie nagłówka
    f.write("file_id\timage_path\tsegmented_path\tspecies\tsource\tset\n")

    file_id = 1  # Inicjalizacja unikalnego id dla plików

    # Iterowanie przez foldery zbiorów (train, validation, test)
    for source in ['lab', 'field']:
            source_dir = os.path.join(images_base_dir, source)
            segmented_source_dir = os.path.join(segmented_base_dir, source)

            # Sprawdzenie, czy foldery źródłowe istnieją
            if os.path.exists(source_dir) and os.path.exists(segmented_source_dir):
                print(f"Przetwarzanie zbioru w: {source}")

                # Iterowanie przez foldery gatunków
                for species in os.listdir(source_dir):
                    species_dir = os.path.join(source_dir, species)
                    segmented_species_dir = os.path.join(segmented_source_dir, species)

                    # Sprawdzenie, czy to foldery
                    if os.path.isdir(species_dir) and os.path.isdir(segmented_species_dir):
                        print(f"  Przetwarzanie gatunku: {species}")

                        # Iterowanie przez pliki w folderze gatunku
                        for image in os.listdir(species_dir):
                            if image.lower().endswith(('.png', '.jpg', '.jpeg')):  # Filtrowanie tylko plików graficznych
                                image_path = os.path.join('dataset/images', source, species, image)
                                segmented_image_path = os.path.join('dataset/segmented', source, species, os.path.splitext(image)[0] + '.png')

                                # Zapisanie danych do pliku
                                f.write(f"{file_id}\t{image_path}\t{segmented_image_path}\t{species}\t{source}\n")
                                file_id += 1  # Zwiększenie unikalnego id

print(f"Plik {output_file} został utworzony.")