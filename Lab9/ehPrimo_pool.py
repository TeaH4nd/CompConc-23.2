#exemplo de uso de futuros em Python

import concurrent.futures
import sys
import time

#funcao que sera executada de forma assincrona
def ehPrimo(n):
    if (n <= 1):
        return 0
    if (n == 2):
        return 1
    if (n % 2 == 0):
        return 0
    for i in range(3, int(n**0.5) + 1, 2):
        if (n % i == 0):
            return 0
    return 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso correto: python3 ehPrimo_pool.py <Valor de N>")
        sys.exit(1)
    else:
        start = time.time()
        N = int(sys.argv[1])

        #cria um pool de threads OU de processos com no maximo 5 intancias 
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures = []
            
            #submete a tarefa para execucao assincrona
            for aux in range(N+1):
                futures.append(executor.submit(ehPrimo, aux))
            #recebe os resultados
            total = 0
            for future in futures:
                result = future.result()
                total += result
                # print(result)
        end = time.time()
        print('\nTotal de primos entre 0 e {} = {}'.format(N, total))
        print('\twork took {} seconds'.format(end - start))
