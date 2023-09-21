#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <string.h>

#include "cods-lab2/timer.h"

#define MAX_THREADS 4

long long int N;
int num_threads;
int *is_prime;

// Função para verificar a primalidade de um número
int ehPrimo(long long int n) {
    int i;
    if (n <= 1) return 0;
    if (n == 2) return 1;
    if (n % 2 == 0) return 0;
    for (i = 3; i <= sqrt(n); i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

// Função para contar números primos em uma faixa
void *contarPrimos(void *arg) {
    long long int thread_id = *((long long int *)arg);
    long long int chunk_size = N / num_threads;
    long long int start = thread_id * chunk_size + 1;
    long long int end = (thread_id == num_threads - 1) ? N : start + chunk_size - 1;

    for (long long int i = start; i <= end; i++) {
        if (ehPrimo(i)) {
            is_prime[i] = 1;
        }
    }

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Uso: %s <N> <num_threads>\n", argv[0]);
        return 1;
    }

    N = atoll(argv[1]);
    num_threads = atoi(argv[2]);

    if (num_threads <= 0 || num_threads > MAX_THREADS) {
        printf("Número de threads inválido. Deve estar entre 1 e %d.\n", MAX_THREADS);
        return 1;
    }

    is_prime = (int *)malloc((N + 1) * sizeof(int));
    if (is_prime == NULL) {
        printf("Erro na alocação de memória.\n");
        return 1;
    }

    // Inicializa o vetor is_prime
    memset(is_prime, 0, (N + 1) * sizeof(int));

    double start_time, end_time;
    GET_TIME(start_time);

    pthread_t threads[MAX_THREADS];
    long long int thread_ids[MAX_THREADS];

    for (long long int i = 0; i < num_threads; i++) {
        thread_ids[i] = i;
        pthread_create(&threads[i], NULL, contarPrimos, &thread_ids[i]);
    }

    for (long long int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    GET_TIME(end_time);

    double execution_time = end_time - start_time;

    long long int prime_count = 0;
    for (long long int i = 1; i <= N; i++) {
        if (is_prime[i]) {
            prime_count++;
        }
    }

    printf("Número total de primos em 1-%lld: %lld\n", N, prime_count);
    printf("Tempo de execução: %lf segundos\n", execution_time);

    free(is_prime);

    return 0;
}
