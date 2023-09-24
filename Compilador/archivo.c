#include <stdio.h>
int suma(int a,int b){
    return a+b;
}
int maximo(int a, int b){
    if(a > b){
        return a;
    }else{
        return b;
    }
}

void imprimirSerie(int inicio, int fin) {
    for (int i=inicio;i<=fin;i++) {
        printf("%d ",i);
    }
    printf("\n");
}
int main() {
    int num1=5;
    int num2=7;

    // Utilizar la función suma
    int resultado_suma = suma(num1, num2);
    printf("La suma de " + num1 + " y " + num2 + "es " + resultado_suma);

    int max = maximo(num1, num2);
    printf("El máximo entre " + 1 + " y " + num2 + "es " + max);/*
        Se usa la funcion imprimirSerie
        todo dentro de un comentario
        con una inicialización diferente
    */
    printf("Imprimir serie del 1 al 10:\n");
    imprimirSerie(1, 10);

    return 0;
}