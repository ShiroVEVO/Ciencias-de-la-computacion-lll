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
    if not eAtomica.validar_caracter(raiz,';'):
        return not es_valido
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

def validar_while(codigo,num_linea):
    i = 2
    es_valido = True
    raiz = asa.crear_asa_linea(s.separador(codigo[num_linea]))
    hijos = raiz.get_hijos()
    estructura = [['PALABRA RESERVADA'],
                  ['SÍMBOLO ESPECIAL'],
                  ['CONDICIÓN'],
                  ['SÍMBOLO ESPECIAL'],
                  ['SÍMBOLO ESPECIAL']]
    pi = eAtomica.validar_bloque(codigo,num_linea,')')
    if pi.esta_vacia():
        return not es_valido
    pi2 = eAtomica.validar_bloque(codigo,num_linea,'}')
    if pi2.esta_vacia():
        return not es_valido

    while i < len(hijos):
        if hijos[i].valor[0][0] == 'OPERADOR COMPARACIÓN':
            raiz = eAtomica.validar_comparacion(raiz, i - 1, i + 1)
            if raiz is None:
                return not es_valido
            else:
                hijos = raiz.get_hijos()
                i = 0
        else:
            i += 1
    i = 0
    while i < len(hijos):
        print("caso[",i,"]: ", hijos[i].valor[0][0])
        if hijos[i].valor[0][0] == 'OPERADOR LÓGICO':
            raiz = eAtomica.validar_condicion(raiz, i - 1, i + 1)
            if raiz is None:
                return not es_valido
            else:
                hijos = raiz.get_hijos()
                i = 0
        else:
            i += 1
    #asa.imprimir_asa(raiz)
    print(".........inicio pila.........")
    pi2.desapilar()
    #while pi2.tamano() > 1:
    for elemento in pi2:
        print(elemento)
        """
        ACA DEBE IR UN MONTON DE CODIGO que aun no tenemos, para que valide todas las estructuras de control
        lineas de asignación, lineas de incremento, return... y no se me ocurre ninguna otra
        """

    print("..........fin pila..........")

    if eAtomica.validar_estructura(estructura,hijos):
        if hijos[0].valor[1][0] == 'while' and hijos[1].valor[1][0] == '(' and hijos[3].valor[1][0] == ')' and hijos[4].valor[1][0] == '{':
            return es_valido
    else:
        return not es_valido



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
