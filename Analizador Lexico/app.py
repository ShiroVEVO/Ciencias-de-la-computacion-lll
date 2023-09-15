import separador

Codigo = []

with open('archivo.c', 'r') as archivo:
    for linea in archivo:
        linea = linea.strip();
        if linea:
            Codigo.append(linea)
    for linea in Codigo:

        separador.separadorEspacios()

        #Codigo para palabras reservadas

        #Codigo para Identificadores

        #Codigo para Comentarios

        #Codigo para Numeros enteros

        #Codigo para Numeros flotantes

        #Codigo para Simbolos especiales

        #Codigo para operadores logicos

        #Codigo para operadores matematicos

        #Codigo para operadores de comparacion

        #Codigo para cadenas

        #Codigo para declarar funciones?

        #Codigo para parametros?
        print("linea: " + linea)            