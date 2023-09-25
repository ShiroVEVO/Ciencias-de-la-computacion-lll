from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo
from Recursos import ArbolSintaxisAbstracta as asa
import EstructurasAtomicas as eAtomica
import ConstruccionArbol as cArbol

"""
1. (HECHO) SALVO EL...(Como manejamos el !??)
2. (HECHO) atomica incremental decremental ++ -- 
3. (HECHO) Declaración funcion 
4. (HECHO) Asignación 
5. (EN PROCESO) Llamada función
6. Sentencia If
7. (ADRIAN) While

"""

def validar_asignacion(raiz):
    es_valido = True
    i = 0
    hijos = raiz.get_hijos()
    estructura = [['IDENTIFICADOR', 'DECLARACIÓN VARIABLE/PARAMETROS'],
                  ['OPERADOR ASIGNACIÓN'],
                  ['IDENTIFICADOR', 'OPERACIÓN MATEMATICA', 'NUMERO ENTERO', 'NUMERO FLOTANTE', 'CADENA'],
                  ['CARÁCTER PUNTUACIÓN']]

    while i < len(hijos):
        if hijos[i].valor[0][0] == 'OPERADOR MATEMÁTICO':
            raiz = eAtomica.validar_operacion_matematica(raiz, i - 1, i + 1)
            if raiz is None:
                return not es_valido
            else:
                hijos = raiz.get_hijos()
                i = 0
                asa.imprimir_asa(raiz)
        else:
            i += 1
    if hijos[0].valor[0][0] == 'PALABRA RESERVADA':
        return es_valido
    elif hijos[0].valor[0][0] == 'IDENTIFICADOR':
        return es_valido
    else:
        return not es_valido
    """
    posibilidades: 
    Declaracion = Operacion matematica/NumeroEntero/Identificador/NumeroFlotante
    Identificador = Operacion matematica/NumeroEntero/Identificador/NumeroFlotante/cadenas
    """


"""validar_declaracion_funcion"""


def validar_declaracion_funcion(raiz):
    filtro1 = cArbol.construir_variables_parametros(raiz)
    filtro2 = cArbol.construir_argumento(filtro1)
    filtro3 = cArbol.construir_argumentos(filtro2)

    hijos = filtro3.get_hijos()

    estructura = [['DECLARACIÓN VARIABLE/PARAMETROS'], ['SÍMBOLO ESPECIAL'], ['ARGUMENTOS'],
                  ['SÍMBOLO ESPECIAL'], ['SÍMBOLO ESPECIAL']]
    estructura2 = [['DECLARACIÓN VARIABLE/PARAMETROS'], ['SÍMBOLO ESPECIAL'], ['ARGUMENTOS'],
                   ['SÍMBOLO ESPECIAL']]

    if eAtomica.validar_estructura(estructura, hijos) or eAtomica.validar_estructura(estructura2, hijos):
        if not hijos[1].valor[1][0] == '(' and not hijos[3].valor[1][0] == ')':
            return None
        else:
            return raiz
    else:
        return None


"""validar_llamada_funcion"""
def validar_llamada_funcion(raiz):
    filtro1 = cArbol.construir_variables_parametros(raiz)
    filtro2 = cArbol.construir_argumento(filtro1)
    filtro3 = cArbol.construir_argumentos(filtro2)

    hijos = filtro3.get_hijos()

    estructura = [['IDENTIFICADOR'], ['SÍMBOLO ESPECIAL'],
                  ['LLAMADA FUNCION', 'ARGUMENTOS', ],
                  ['SÍMBOLO ESPECIAL'], ['CARÁCTER PUNTUACIÓN']]

    if eAtomica.validar_estructura(estructura, hijos):
        if not hijos[1].valor[1][0] == '(' and not hijos[3].valor[1][0] == ')' and not hijos[4].valor[1][0] == ';':
            return None
        else:
            return raiz
    else:
        return None
