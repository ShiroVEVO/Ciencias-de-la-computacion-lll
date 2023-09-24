from Recursos import Recursos as r
from Analizador_Lexico import Separador as s
from Recursos import ArbolSintaxisAbstracta as asa
from Analizador_Sintactico import AnalizadorSintactico as analizadors
from Recursos import Nodo as nodo

# ---------------- PRUEBAS ANALIZADOR LEXICO --------------------
codigo = r.leer_archivo('Compilador/archivo.c')
tokens = []
i = 0
"""
for i, elemento in enumerate(codigo):
   print ("Elemento: #", str(i), ", ", elemento)
for clave, valor in r.contar_elemento(tokens, 0).items():
   print(f"{clave}: {valor}")

for linea in codigo:
      tokens.extend(s.separador(linea))

for elemento in tokens:
   print (elemento)
"""


#-------------- PRUEBAS ANALIZADOR SINTACTICO ------------------

"""
x = analizadors.validar_bloque(codigo,1,"}")

#print("---- pila ----", "\n")
#for elemento in x:
#     print(elemento)

x = asa.crear_asa_linea(codigo)
asa.imprimir_asa(x)
"""


#----------------- 1. Pruebas Operación matematica
"""
tokens = [[['NUMERO ENTERO'], ['aweqwqa']],
         [['OPERADOR MATEMÁTICO'], ['+']],
         [['IDENTIFICADO'], ['pipipi']]]

x = asa.crear_asa_linea(tokens) 
y = analizadors.validar_operacion_matematica(x,0,2)
if(y != None):
    print("La operación matematica es valida ahora el arbol es: ")
    asa.imprimir_asa(y)
else: 
   print("La operación matematica es invalida")
"""
#----------------- 2. Pruebas declaración variable o parametros

"""
tokens = [[['PALABRA RESERVADA'], ['int']],
         [['IDENTIFICADOR'], ['a']]]
x = asa.crear_asa_linea(tokens) 
y = analizadors.validar_declaracion_variable_parametros(x,0,1)
if(y != None):
    print("La declaración de parametros o variable es valida, ahora el arbol es: ")
    asa.imprimir_asa(y)
else: 
   print("La declaración es invalida.")
"""

#----------------- 3. Pruebas comparación
"""
tokens = [[['IDENTIFICADOR'], ['pedro']],
         [['OPERADOR COMPARACIÓN'], ['==']],
         [['IDENTIFICADOR'], ['a']]]
x = asa.crear_asa_linea(tokens)
y = analizadors.validar_comparacion(x,0,2)
if(y != None):
    print("La comparación es valida, ahora el arbol es: ")
    asa.imprimir_asa(y)
else: 
   print("La declaración es invalida.")
"""
#----------------- 3. Pruebas condición
"""
tokens = [[['IDENTIFICADOR'], ['pedro']],
         [['OPERADOR COMPARACIÓN'], ['==']],
         [['IDENTIFICADOR'], ['a']],
         [['OPERADOR LÓGICO'], ['&&']],
         [['IDENTIFICADOR'], ['juan']],
         [['OPERADOR COMPARACIÓN'], ['==']],
         [['IDENTIFICADOR'], ['abivail']]]
x = asa.crear_asa_linea(tokens)
y = analizadors.validar_comparacion(x,0,2)

y1 = analizadors.validar_comparacion(y,2,5)
y2 = analizadors.validar_condicion(y1,0,2)
if(y2 != None):
    print("La condición es valida, ahora el arbol es: ")
    asa.imprimir_asa(y)
else: 
   print("La condicion es invalida.")
"""

# ----------------- 5. Pruebas argumentos

tokens1 = [[['LITERAL CADENA'], ['"']],
          [['IDENTIFICADO'], ['pedro']],
          [['IDENTIFICADO'], ['pascal']],
          [['LITERAL CADENA'], ['"']],
          [['OPERADOR MATEMÁTICO'], ['+']]]
tokens2 = [[['LITERAL CADENA'], ['"']],
          [['IDENTIFICADO'], ['pedro']],
          [['IDENTIFICADO'], ['pascal']],
          [['LITERAL CADENA'], ['"']]]
tokens3 = [[['LITERAL CADENA'], ['"']],
          [['IDENTIFICADO'], ['pedro']],
          [['IDENTIFICADO'], ['pascal']],
          [['LITERAL CADENA'], ['"']],
          [['OPERADOR MATEMÁTICO'], [',']]]
x = asa.crear_asa_comentario(tokens1)
print("Arbol: ")
asa.imprimir_asa(x)
print("El argumento es: ", analizadors.validar_argumentos(x.get_hijos()))
print("El argumento printf es: ", analizadors.validar_argumentos_printf(x.get_hijos()))
x = asa.crear_asa_comentario(tokens2)
print("El argumento es: ", analizadors.validar_argumentos(x.get_hijos()))
print("El argumento printf es: ", analizadors.validar_argumentos_printf(x.get_hijos()))
x = asa.crear_asa_comentario(tokens3)
print("El argumento es: ", analizadors.validar_argumentos(x.get_hijos()))
print("El argumento printf es: ", analizadors.validar_argumentos_printf(x.get_hijos()))

