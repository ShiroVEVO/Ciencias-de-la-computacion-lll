import separador as s

Codigo = []
tokens = []

with open('archivo.c', 'r') as archivo:
    for linea in archivo:
        linea = linea.strip();
        if linea:
            Codigo.append(linea)
    for linea in Codigo:

        tokens.extend(s.separador(linea))

        #Codigo para Comentarios

        #Codigo para Simbolos especiales

        #Codigo para operadores logicos

        #Codigo para operadores matematicos

        #Codigo para operadores de comparacion

        #Codigo para cadenas

        #Codigo para declarar funciones?

        #Codigo para parametros?
        #print("linea: " + linea)

print (tokens)