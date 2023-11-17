package Lab8;

class VerificaPrimos implements Runnable {
    private final long inicio;
    private final long fim;
    private final FilaTarefas pool;

    public VerificaPrimos(long inicio, long fim, FilaTarefas pool) {
        this.inicio = inicio;
        this.fim = fim;
        this.pool = pool;
    }

    @Override
    public void run() {
        for (long i = inicio; i <= fim; i++) {
            if (ehPrimo(i)) {
                pool.incrementCount();
            }
        }
        synchronized (pool) {
            pool.notify(); // Notifica a conclusão da tarefa
        }
    }

    private boolean ehPrimo(long n) {
        if (n <= 1) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        for (long i = 3; i <= Math.sqrt(n) + 1; i += 2)
            if (n % i == 0) return false;
        return true;
    }
}
