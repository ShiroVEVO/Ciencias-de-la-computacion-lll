from Recursos import Recursos as r
from Analizador_Lexico import Separador as s
from Recursos import ArbolSintaxisAbstracta as asa
from Analizador_Sintactico import AnalizadorSintactico as analizadors
from Recursos import Nodo as nodo

#---------------- PRUEBAS ANALIZADOR LEXICO --------------------
"""
tokens = []
codigo = r.leer_archivo('Compilador/archivo.c')
i = 0
for i, elemento in enumerate(codigo):
   print ("Elemento: #", str(i), ", ", elemento)
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

x = asa.crear_asa_programa(codigo)
asa.imprimir_asa(x)
"""


"""
#----------------- 1. Pruebas Operación matematica

tokens = [[['NUMERO ENTERO'], ['aweqwqa']],
         [['OPERADOR MATEMÁTICO'], ['+']],
         [['IDENTIFICADOR'], ['pipipi']]]

x = asa.crear_asa_linea(tokens) 
print("La operación matematica es: ", analizadors.validar_operacion_matematica(x.get_hijos()))
"""

"""
#----------------- 2. Pruebas declaración variable o parametros

tokens = [[['PALABRA RESERVADA'], ['int']],
         [['IDENTIFICADO'], ['a']]]
x = asa.crear_asa_linea(tokens) 
print("La declaración es: ", analizadors.validar_declaracion_variable_parametros(x.get_hijos()))
"""


#----------------- 2. Pruebas comparación
tokens = [[['IDENTIFICADO'], ['pedro']],
         [['OPERADOR COMPARACIÓN'], ['!=']],
         [['IDENTIFICADOR'], ['a']]]
x = asa.crear_asa_linea(tokens) 
print("La declaración es: ", analizadors.validar_comparacion(x.get_hijos()))






