from Recursos import Recursos as r
from Analizador_Lexico import Separador as s
from Recursos import ArbolSintaxisAbstracta as asa
from Analizador_Sintactico import AnalizadorSintactico as analizadors
from Recursos import Nodo as nodo

# ---------------- PRUEBAS ANALIZADOR LEXICO --------------------
codigo = r.leer_archivo('../Compilador/archivo.c')
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
tokens2 =[[['OPERADOR LÓGICO'], ['&&']],
         [['IDENTIFICADOR'], ['juan']],
         [['OPERADOR COMPARACIÓN'], ['==']],
         [['IDENTIFICADOR'], ['abivail']]]
x = asa.crear_asa_linea(tokens2)
y = analizadors.validar_comparacion(x,1,3)
y2 = analizadors.validar_condicion(y,0,1)
#y = analizadors.validar_comparacion(x,0,2)
#y1 = analizadors.validar_comparacion(y,2,4)
#y2 = analizadors.validar_condicion(y1,0,2)
if(y2 != None):
    print("La condición es valida, ahora el arbol es: ")
    asa.imprimir_asa(y2)
else: 
   print("La condicion es invalida.")
"""

# ----------------- 5. Pruebas argumentos
"""
tokens1 = [[['LITERAL CADENA'], ['"']],
           [['IDENTIFICADOR'], ['pedro']],
           [['IDENTIFICADOR'], ['pascal']],
           [['LITERAL CADENA'], ['"']],
           [['CARÁCTER PUNTUACIÓN'], [',']],
           [['IDENTIFICADOR'], ['fffff']]]
x = asa.crear_asa_comentario(tokens1)
y = analizadors.validar_argumentos_printf(x, 0, 1)
y1 = analizadors.validar_argumentos_printf(y, 1, 2)
if (y1 != None):
    print("La condición es valida, ahora el arbol es: ")
    asa.imprimir_asa(y1)
else:
    print("La condicion es invalida.")
"""

# ----------------- 5. Pruebas declaración función
tokens1 = [[['PALABRA RESERVADA'], ['int']],
           [['IDENTIFICADOR'], ['pedro']],
           [['SÍMBOLO ESPECIAL'], ['(']],
           [['PALABRA RESERVADA'], ['int']],
           [['IDENTIFICADOR'], ['a']],
           [['CARÁCTER PUNTUACIÓN'], [',']],
           [['PALABRA RESERVADA'], ['int']],
           [['IDENTIFICADOR'], ['b']],
           [['SÍMBOLO ESPECIAL'], [')']],
 #          [['SÍMBOLO ESPECIAL'], ['{']]
             ]
x = asa.crear_asa_linea(tokens1)
m = analizadors.validar_declaracion_funcion(x)
if (m != None):
    print("La declaración de parametros o variable es valida, ahora el arbol es: ")
    asa.imprimir_asa(m)
else:
    print("La declaración es invalida.")

# ------------------ 7. Pruebas Asignacion
"""
arboles = []
for linea in codigo:
      arboles.append(asa.crear_asa_linea(s.separador(linea)))

print(analizadors.validar_asignacion(arboles[20]))
"""
# ------------------ 7. Pruebas if
"""
arboles = []
for linea in codigo:
      arboles.append(asa.crear_asa_linea(s.separador(linea)))

print(analizadors.validar_if(arboles[20]))
"""