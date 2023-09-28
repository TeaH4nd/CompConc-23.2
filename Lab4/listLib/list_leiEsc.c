#include "list_leiEsc.h"

int leit = 0, escr = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_leit = PTHREAD_COND_INITIALIZER;
pthread_cond_t cond_escr = PTHREAD_COND_INITIALIZER;

void EntraLeitura() {
    pthread_mutex_lock(&mutex);
    while (escr > 0) {
        pthread_cond_wait(&cond_leit, &mutex);
    }
    leit++;
    pthread_mutex_unlock(&mutex);
}

void SaiLeitura() {
    pthread_mutex_lock(&mutex);
    leit--;
    if (leit == 0) {
        pthread_cond_signal(&cond_escr);
    }
    pthread_mutex_unlock(&mutex);
}

void EntraEscrita() {
    pthread_mutex_lock(&mutex);
    while (leit > 0 || escr > 0) {
        pthread_cond_wait(&cond_escr, &mutex);
    }
    escr++;
    pthread_mutex_unlock(&mutex);
}

void SaiEscrita() {
    pthread_mutex_lock(&mutex);
    escr--;
    pthread_cond_signal(&cond_escr);
    pthread_cond_broadcast(&cond_leit);
    pthread_mutex_unlock(&mutex);
}
