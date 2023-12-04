from Recursos import Recursos as recurso
from Analizador_Lexico import Separador as lexico
from Analizador_Sintactico import AnalizadorSintactico as sintactico
from Analizador_Semantico import AnalizadorSemantico as semantico
from Generador_Codigo_Intermedio import Codigo_intermedio as codIntermedio
from tabulate import tabulate

archivoALeer = 'Compilador\Archivos_Prueba\Prueba1.c'
codigo = recurso.leerArchivo(archivoALeer)

tokens = []
correcto = True
for linea in codigo:
    tokens.extend(lexico.separador(linea))

for token in tokens:
    if token[0][0] == "NO ES TOKEN":
        print(token)
        correcto = False

if correcto == True:
    print("El código no tiene errores léxicos")

tabla = semantico.AnalizadorSemantico()
tabla.analizar(codigo)

CodigoLine, A_Saltos, A_EsCeros = codIntermedio.GenerarCodigoIntermedio(codigo)
TablaConDirecciones = codIntermedio.AgregarDirecciones(CodigoLine, A_EsCeros, A_Saltos)

print(tabulate(TablaConDirecciones, headers=["Dirrecion", "Operador", "Var1", "Var2", "Resultado"], tablefmt='fancy_grid'))