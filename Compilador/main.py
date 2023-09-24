from Recursos import Recursos as r
from Analizador_Lexico import Separador as s
from Recursos import ArbolSintaxisAbstracta as asa
from Analizador_Sintactico import AnalizadorSintactico as analizadors
from Recursos import Nodo as nodo

#---------------- PRUEBAS ANALIZADOR LEXICO --------------------
tokens = []
codigo = r.leer_archivo('Compilador/archivo.c')
i = 0

"""for i, elemento in enumerate(codigo):
    print ("Elemento: #" + str(i) +", " + elemento)



for clave, valor in r.contar_elemento(tokens, 0).items():
   print(f"{clave}: {valor}")

for linea in codigo:
      tokens.extend(s.separador(linea))
for elemento in tokens:
   print (elemento)"""

#-------------- PRUEBAS ANALIZADOR SINTACTICO ------------------
"""
x = analizadors.validar_bloque(codigo,12,"}")
print("---- pila ----", "\n")
for elemento in x:
     print(elemento)
"""
#x = asa.crear_asa_programa(codigo)
#asa.imprimir_asa(x)


tokens =[[['IDENTIFICADOR'], ['aweqwqa']]]
raiz = asa.crear_asa_linea(tokens)
print(analizadors.validar_declaracion_variable(raiz))

