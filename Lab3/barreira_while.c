#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define MAX_THREADS 100

int N;
pthread_mutex_t mutex;
pthread_cond_t cond_ola;
pthread_cond_t cond_dia;
pthread_cond_t cond_ciao;
int ola_done = 0;
int dia_done = 0;

void *barreira(void *arg) {
    int thread_id = *((int *)arg);

    pthread_mutex_lock(&mutex);
    printf("Olá da thread %d\n", thread_id);
    ola_done++;

    while (ola_done != N) {
        pthread_cond_wait(&cond_ola, &mutex);
    }
    pthread_cond_broadcast(&cond_ola);

    printf("Que dia bonito %d\n", thread_id);
    dia_done++;

    while (dia_done != N) {
        pthread_cond_wait(&cond_dia, &mutex);
    }
    pthread_cond_broadcast(&cond_dia);

    printf("Até breve da thread %d\n", thread_id);

    pthread_mutex_unlock(&mutex);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <N>\n", argv[0]);
        return 1;
    }

    N = atoi(argv[1]);

    if (N <= 0 || N > MAX_THREADS) {
        printf("Número de threads inválido. Deve estar entre 1 e %d.\n", MAX_THREADS);
        return 1;
    }

    pthread_t threads[MAX_THREADS];
    int thread_ids[MAX_THREADS];

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond_ola, NULL);
    pthread_cond_init(&cond_dia, NULL);
    pthread_cond_init(&cond_ciao, NULL);

    for (int i = 0; i < N; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], NULL, barreira, &thread_ids[i]);
    }

    for (int i = 0; i < N; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_ola);
    pthread_cond_destroy(&cond_dia);
    pthread_cond_destroy(&cond_ciao);

    return 0;
}
