#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 8
#define VECTOR_SIZE 10000

int vector[VECTOR_SIZE];

void initializeVector() {
    for (int i = 0; i < VECTOR_SIZE; i++) {
        vector[i] = i + 1;
    }
}

void verifyVector() {
    for (int i = 0; i < VECTOR_SIZE; i++) {
        if (vector[i] != (i + 1) * (i + 1)) {
            printf("Erro! Valor incorreto no índice %d\n", i);
            exit(1);
        }
    }
    printf("Valores corretos em todo o vetor.\n");
}

void *square(void *arg) {
    int thread_id = *((int *)arg);
    int chunk_size = VECTOR_SIZE / NUM_THREADS;
    int start = thread_id * chunk_size;
    int end = (thread_id == NUM_THREADS - 1) ? VECTOR_SIZE : start + chunk_size;

    for (int i = start; i < end; i++) {
        vector[i] = vector[i] * vector[i];
    }

    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    initializeVector();

    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i;
        pthread_create(&threads[i], NULL, square, &thread_ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    verifyVector();

    return 0;
}
