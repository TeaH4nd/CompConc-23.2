#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <string.h>

#define MAX_BUFFER_SIZE 100
#define MAX_LINE_SIZE   1024

char buffer[MAX_BUFFER_SIZE][MAX_LINE_SIZE];
int buffer_index = 0;
int eof_flag = 0;  // Flag para indicar o fim do arquivo
sem_t mutex, full, empty;

void *produtor(void *param) {
    char item[MAX_LINE_SIZE];
    FILE *file = fopen((char *)param, "r");
    while (fgets(item, sizeof(item), file)) {
        sem_wait(&empty);  // Aguarda espaço vazio no buffer
        sem_wait(&mutex);  // Obtém acesso exclusivo ao buffer
        strcpy(buffer[buffer_index], item);  // Coloca a linha lida no buffer
        buffer_index++;
        sem_post(&mutex);  // Libera o acesso ao buffer
        sem_post(&full);   // Sinaliza que há dados no buffer
    }
    eof_flag = 1;           // Indica que o produtor chegou ao fim do arquivo
    fclose(file);
    sem_post(&full);        // Libera as threads consumidoras bloqueadas
    pthread_exit(NULL);
}

void *consumidor(void *param) {
    int thread_id = *((int *)param);
    while (1) {
        sem_wait(&full);  // Aguarda dados no buffer
        sem_wait(&mutex);  // Obtém acesso exclusivo ao buffer
        if (eof_flag && buffer_index == 0) {
            // Se não há mais dados no buffer e o produtor terminou, termina a thread
            sem_post(&mutex);
            sem_post(&empty);
            pthread_exit(NULL);
        }
        printf("Thread %d: %s", thread_id, buffer[0]);  // Imprime a linha do buffer
        for (int i = 0; i < buffer_index - 1; i++) {
            strcpy(buffer[i], buffer[i + 1]);  // Move as linhas restantes para frente no buffer
        }
        buffer_index--;
        sem_post(&mutex);  // Libera o acesso ao buffer
        sem_post(&empty);  // Sinaliza espaço vazio no buffer
    }
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Uso: %s <nome_do_arquivo> <numero_de_threads>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[2]);

    // Inicializa os semáforos e cria as threads
    sem_init(&mutex, 0, 1);
    sem_init(&full, 0, 0);
    sem_init(&empty, 0, MAX_BUFFER_SIZE);

    pthread_t produtor_thread;
    pthread_create(&produtor_thread, NULL, produtor, (void *)argv[1]);

    pthread_t consumidor_threads[num_threads];
    int thread_ids[num_threads];
    for (int i = 0; i < num_threads; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&consumidor_threads[i], NULL, consumidor, (void *)&thread_ids[i]);
    }

    // Aguarda a conclusão das threads produtor e consumidoras
    pthread_join(produtor_thread, NULL);
    for (int i = 0; i < num_threads; i++) {
        pthread_join(consumidor_threads[i], NULL);
    }

    // Destrói os semáforos
    sem_destroy(&mutex);
    sem_destroy(&full);
    sem_destroy(&empty);

    return 0;
}
