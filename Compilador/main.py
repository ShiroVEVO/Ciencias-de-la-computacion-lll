from Recursos import recursos as r
from Analizador_Lexico import separador as s
from Analizador_Sintactico import AnalizadorSintactico as analizadors

#---------------- PRUEBAS ANALIZADOR LEXICO --------------------
tokens = []
codigo = r.leer_archivo('Compilador/archivo.c')
i = 0

"""for i, elemento in enumerate(codigo):
    print ("Elemento: #" + str(i) +", " + elemento)

for linea in codigo:
        tokens.extend(s.separador(linea))

for clave, valor in r.contar_elemento(tokens, 0).items():
   print(f"{clave}: {valor}")

for elemento in tokens:
   print (elemento)"""

#-------------- PRUEBAS ANALIZADOR SINTACTICO ------------------
x = analizadors.validar_bloque(codigo,10,")")
print("---- pila ----", "\n")
for elemento in x:
     print(elemento)