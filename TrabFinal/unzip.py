import shutil
import time
import os
import argparse

from helpers.concurrent_unzip import concurrent_extraction
from helpers.sequencial_unzip import sequential_extraction

ZIPS_PATH = os.path.join(os.path.dirname(__file__), 'zips')
EXTRACT_PATH = os.path.join(os.path.dirname(__file__), 'extraido')

EXTRCONC_PATH = os.path.join(EXTRACT_PATH, 'concorrente')
EXTRSEQU_PATH = os.path.join(EXTRACT_PATH, 'sequencial')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="unzip")
    parser.add_argument("n_threads", help="Number of threads or processes to use")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--threads", action="store_true", help="Use threads instead of processes")
    group.add_argument("-p", "--process", action="store_true", help="Use processes instead of threads")
    
    args = parser.parse_args()

    N = int(args.n_threads)
    # Ensure the extraction folder exists, create it if necessary
    os.makedirs(EXTRCONC_PATH, exist_ok=True)
    os.makedirs(EXTRSEQU_PATH, exist_ok=True)
    for root, dirs, files in os.walk(ZIPS_PATH):
        for file in files:
            if file.endswith('zip'):
                start_file = time.time()
                extr_dir_conc = os.path.join(EXTRCONC_PATH, file[:-4])
                os.makedirs(extr_dir_conc, exist_ok=True)
                if args.threads:
                    print(f'Usando threads para descomprimir: {file}')   
                    concurrent_extraction(os.path.join(root, file), extr_dir_conc, N, "thread")
                elif args.process:
                    print(f'Usando processos para descomprimir: {file}')
                    concurrent_extraction(os.path.join(root, file), extr_dir_conc, N, "process")
                end_file = time.time()
                if args.threads:
                    print(f'Tempo para descompressao do arquivo: {file} ({N} threads)')
                elif args.process:
                    print(f'Tempo para descompressao do arquivo: {file} ({N} processos)')
                print(f'\t{end_file - start_file} seconds\n')
        for file in files:
            if file.endswith('zip'):
                start_file = time.time()
                extr_dir_seq = os.path.join(EXTRSEQU_PATH, file[:-4])
                os.makedirs(extr_dir_seq, exist_ok=True)
                print(f'Descomprimindo sequencialmente: {file}')
                sequential_extraction(os.path.join(root, file), extr_dir_seq)
                end_file = time.time()
                print(f'Tempo para descompressao do arquivo: {file} (sequencial)')
                print(f'\t{end_file - start_file} seconds\n')

    del_dir = input('Deletar pastas extraidas? (y/N)')
    if not del_dir:
        del_dir = 'n'
    if del_dir == ('y' or 'Y'):
        shutil.rmtree(EXTRACT_PATH)
