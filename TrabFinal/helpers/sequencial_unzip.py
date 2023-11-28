import zipfile


def sequential_extraction(zip_file_path, extract_folder):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        # print(f"Successfully decompressed '{zip_file_path}' to '{extract_folder}'.")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_file_path}' is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred: {e}")