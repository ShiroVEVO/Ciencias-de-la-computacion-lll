#include <stdio.h>

int suma(int a, int b) {
    return a + b;
}

int maximo(int a, int b) {
    return (a > b) ? a : b;
}

void imprimirSerie(int inicio, int fin) {
    for (int i = inicio; i <= fin; i++) {
        printf("%d ", i);
    }
    printf("\n");
}

int main() {
    int num1 = 5;
    int num2 = 7;

    // Utilizar la función suma
    int resultado_suma = suma(num1, num2);
    printf("La suma de %d y %d es %d\n", num1, num2, resultado_suma);

    int max = maximo(num1, num2);
    printf("El máximo entre %d y %d es %d\n", num1, num2, max);
    /*
        Se usa la funcion imprimirSerie
        todo dentro de un comentario
        con una inicialización diferente
    */
    printf("Imprimir serie del 1 al 10:\n");
    imprimirSerie(1, 10);

    return 0;
}
