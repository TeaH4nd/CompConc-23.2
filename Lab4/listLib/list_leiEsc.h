#ifndef LEITOR_ESCRITOR
#define LEITOR_ESCRITOR

#include <pthread.h>

// Variáveis globais para o controle de leitores e escritores
extern int leit, escr;
extern pthread_mutex_t mutex;
extern pthread_cond_t cond_leit, cond_escr;

// Funções de controle de acesso
void EntraLeitura();
void SaiLeitura();
void EntraEscrita();
void SaiEscrita();

#endif /* LEITOR_ESCRITOR */
