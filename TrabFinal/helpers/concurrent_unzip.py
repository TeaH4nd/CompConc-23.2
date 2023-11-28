import zipfile
import concurrent.futures


def extract_file(zip_file, file_name, extract_folder):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract(file_name, extract_folder)
        # print(f"Successfully extracted '{file_name}' from '{zip_file}' to '{extract_folder}'.")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_file}' is not a valid ZIP file.")
    except Exception as e:
        print(f"An error occurred while extracting '{file_name}' from '{zip_file}': {e}")

def concurrent_extraction(zip_file, extract_folder, n_threads, executor_type="thread"):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Get the list of files in the ZIP archive
            file_names = zip_ref.namelist()

            # Choose the executor type based on the provided parameter
            if executor_type == "thread":
                executor_class = concurrent.futures.ThreadPoolExecutor
            elif executor_type == "process":
                executor_class = concurrent.futures.ProcessPoolExecutor
            else:
                raise ValueError("Invalid executor_type. Use 'thread' or 'process'.")

            # Use the selected executor to extract each file concurrently
            with executor_class(max_workers=n_threads) as executor:
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
