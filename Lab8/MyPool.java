package Lab8;

public class MyPool {
    private static final int NTHREADS = 10;
    private static final int N = 100000;

    public static void main(String[] args) {
        FilaTarefas pool = new FilaTarefas(NTHREADS);

        int numerosPorThread = N / NTHREADS;

        for (int i = 0; i < NTHREADS; i++) {
            long inicio = i * numerosPorThread + 1;
            long fim = (i + 1) * numerosPorThread;
            Runnable r = new VerificaPrimos(inicio, fim, pool);
            pool.execute(r);
        }

        // Aguarda a conclusão de todas as tarefas
        synchronized (pool) {
            try {
                pool.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        pool.shutdown();

        // Obtem a contagem total de números primos usando o novo método
        int totalPrimos = pool.getTotalPrimos();

        System.out.println("Terminou. Total de números primos encontrados: " + totalPrimos);
    }
}
