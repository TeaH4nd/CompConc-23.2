import os
import zipfile
import concurrent.futures
import threading  # Added for thread identification

def extract_file(zip_file, file_name, extract_folder, type):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract(file_name, extract_folder)
        if type == 'thread':
            print(f"Thread {threading.current_thread().name}: Finished extracting '{file_name}'.")
        elif type == 'process':
            print(f"Process {os.getpid()}: Finished extracting '{file_name}'.")
        # print(f"Thread {threading.current_thread().name} successfully extracted '{file_name}' from '{zip_file}' to '{extract_folder}'.")
    except zipfile.BadZipFile:
        print(f"Thread {threading.current_thread().name}: Error: '{zip_file}' is not a valid ZIP file.")
    except Exception as e:
        print(f"Thread {threading.current_thread().name}: An error occurred while extracting '{file_name}' from '{zip_file}': {e}")

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

            # Use the selected executor to extract each file simultaneously
            with executor_class(max_workers=n_threads) as executor:
                # Create an iterator to get the next file name
                file_iterator = iter(file_names)

                # Submit initial batch of tasks
                extraction_tasks = [executor.submit(extract_file, zip_file, file_name, extract_folder, executor_type) for file_name in file_iterator]

                for future in extraction_tasks:
                    future.result()

    except zipfile.BadZipFile:
        print(f"Thread {threading.current_thread().name}: Error: '{zip_file}' is not a valid ZIP file.")
    except Exception as e:
        print(f"Thread {threading.current_thread().name}: An error occurred while processing '{zip_file}': {e}")
