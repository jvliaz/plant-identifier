import os


def generate_dataset_list(images_base_dir, output_file):
    """
    Funkcja do generowania pliku listy obrazów w formacie tabulowanym.

    :param images_base_dir: Ścieżka do folderu z obrazami (np. 'data/dataset/images')
    :param output_file: Ścieżka do pliku, w którym zapisane będą wyniki (np. 'data/dataset/dataset-images-list.txt')
    """
    # Ustalenie zbiorów do przetworzenia
    sets = ['train', 'validation', 'test']

    # Otworzenie pliku wyjściowego do zapisu
    with open(output_file, 'w') as f:
        # Zapisanie nagłówka
        f.write("file_id\timage_path\tspecies\tsource\tset\n")

        file_id = 1  # Inicjalizacja unikalnego id dla plików

        # Iterowanie przez foldery zbiorów (train, validation, test)
        for dataset_set in sets:
            for source in ['lab', 'field']:
                source_dir = os.path.join(images_base_dir, dataset_set, source)

                # Sprawdzenie, czy folder źródłowy istnieje
                if os.path.exists(source_dir):
                    print(f"Przetwarzanie zbioru: {dataset_set}, źródła: {source}")

                    # Iterowanie przez foldery gatunków
                    for species in os.listdir(source_dir):
                        species_dir = os.path.join(source_dir, species)

                        # Sprawdzenie, czy to foldery
                        if os.path.isdir(species_dir):
                            print(f"  Przetwarzanie gatunku: {species}")

                            # Iterowanie przez pliki w folderze gatunku
                            for image in os.listdir(species_dir):
                                if image.lower().endswith(
                                        ('.png', '.jpg', '.jpeg')):  # Filtrowanie tylko plików graficznych
                                    image_path = os.path.join('dataset/images', dataset_set, source, species, image)

                                    # Zapisanie danych do pliku
                                    f.write(f"{file_id}\t{image_path}\t{species}\t{source}\t{dataset_set}\n")
                                    file_id += 1  # Zwiększenie unikalnego id

    print(f"Plik {output_file} został utworzony.")


# Wywołanie funkcji
images_base_dir = 'data/dataset/images'  # Ścieżka do folderu z obrazami
output_file = 'data/dataset/dataset-images-list.txt'  # Ścieżka do pliku wynikowego

# Uruchomienie funkcji
generate_dataset_list(images_base_dir, output_file)