import sys
import zipfile
import os
import concurrent.futures

ZIPS_PATH = os.path.join(os.path.dirname(__file__), 'zips')
EXTRCONC_PATH = os.path.join(os.path.dirname(__file__), 'extraido', 'concorrente')
EXTRSEQU_PATH = os.path.join(os.path.dirname(__file__), 'extraido', 'sequencial')

def decompress_zip(zip_file_path, extract_folder):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        print(f"Successfully decompressed '{zip_file_path}' to '{extract_folder}'.")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_file_path}' is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_file(zip_file, file_name, extract_folder):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract(file_name, extract_folder)
        print(f"Successfully extracted '{file_name}' from '{zip_file}' to '{extract_folder}'.")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_file}' is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred while extracting '{file_name}' from '{zip_file}': {e}")

def concurrent_extraction(zip_file, extract_folder, n_threads):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Get the list of files in the ZIP archive
            file_names = zip_ref.namelist()

            # Use ThreadPoolExecutor to extract each file concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
                extraction_tasks = {
                    executor.submit(extract_file, zip_file, file_name, extract_folder): file_name
                    for file_name in file_names
                }

                # Wait for all tasks to complete
                concurrent.futures.wait(extraction_tasks)

    except zipfile.BadZipFile:
        print(f"Error: '{zip_file}' is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred while processing '{zip_file}': {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python3 unzipConcorrente.py <Valor de N>')
        sys.exit(1)
    else:
        N = int(sys.argv[1])
        # Ensure the extraction folder exists, create it if necessary
        os.makedirs(EXTRCONC_PATH, exist_ok=True)
        for root, dirs, files in os.walk(ZIPS_PATH):
            for file in files:
                if file.endswith('zip'):
                    concurrent_extraction(os.path.join(root, file), EXTRCONC_PATH, N)
