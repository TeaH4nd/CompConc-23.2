# Análise Comparativa de Desempenho

Este repositório contém diferentes implementações de um programa concorrente que compartilha uma lista encadeada entre threads. As implementações utilizam mecanismos de sincronização, incluindo mutex, rwlock e uma implementação personalizada do padrão leitores/escritores.

## Compilação

Para compilar cada versão do programa, utilize os seguintes comandos:

### Mutex
```bash
gcc -o main_list main_list.c listLib/list_int.c -lpthread
```

### Rwlock
```bash
gcc -o rwlock main_list_rwlock.c listLib/list_int.c -lpthread -lm
```

### Leitor/Escritor
```bash
gcc -o leiEsc main_leiEsc.c listLib/list_int.c listLib/list_leiEsc.c -lpthread -lm
```

## Execução

Para executar os programas, você pode usar o seguinte comando, substituindo `<num_threads>` pelo número desejado de threads:
```bash
./main_list <num_threads>
./rwlock <num_threads>
./leiEsc <num_threads>
```

## Análise de Desempenho

Realizamos testes de desempenho variando o número de threads e o tamanho da lista. Abaixo estão os resultados médios do tempo de execução para cada implementação:

### Mutex

    1 Thread:
        Lista de tamanho 10^3: Tempo médio = 0,000263 segundos
        Lista de tamanho 10^7: Tempo médio = 1,207319 segundos

    2 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000229 segundos
        Lista de tamanho 10^7: Tempo médio = 3,376018 segundos

    4 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000279 segundos
        Lista de tamanho 10^7: Tempo médio = 4,202026 segundos

### RWLock

    1 Thread:
        Lista de tamanho 10^3: Tempo médio = 0,000246 segundos
        Lista de tamanho 10^7: Tempo médio = 1,219676 segundos

    2 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000337 segundos
        Lista de tamanho 10^7: Tempo médio = 2,852162 segundos

    4 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000240 segundos
        Lista de tamanho 10^7: Tempo médio = 3,220814 segundos

### Leitores/Escritores

    1 Thread:
        Lista de tamanho 10^3: Tempo médio = 0,000289 segundos
        Lista de tamanho 10^7: Tempo médio = 1,365005 segundos

    2 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000269 segundos
        Lista de tamanho 10^7: Tempo médio = 3,170645 segundos

    4 Threads:
        Lista de tamanho 10^3: Tempo médio = 0,000292 segundos
        Lista de tamanho 10^7: Tempo médio = 4,060518 segundos