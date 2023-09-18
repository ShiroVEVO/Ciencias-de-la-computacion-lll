import separador as s
import recursos as r

Codigo = []
tokens = []

with open('archivo.c', 'r') as archivo:
    for linea in archivo:
        linea = linea.strip();
        if linea:
            Codigo.append(linea)
    for linea in Codigo:
        tokens.extend(s.separador(linea))

for clave, valor in r.contar_elemento(tokens, 0).items():
    print(f"{clave}: {valor}")

#for elemento in tokens:
#    print (elemento)