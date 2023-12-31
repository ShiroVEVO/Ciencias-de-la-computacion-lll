from Analizador_Lexico import Separador as s
from Recursos import Pila as pila
from Recursos import Nodo as nodo
from Recursos import ArbolSintaxisAbstracta as asa
from Analizador_Sintactico import EstructurasAtomicas as eAtomica
from Analizador_Sintactico import ConstruccionArbol as cArbol

"""
- METODO DE SIMPLIFICACIÓN DE LINEA

Las lineas pueden ser: 
- (HECHO A) asignación
- (HECHO A) declaracion
- (HECHO A) importe
- (HECHO) declaracion de funcion
- (HECHO) llamado de funcion 
- (HECHO A) retorno
- (HECHO A) Comentario de una linea
- Comentario Multilinea
- while
- if
- else
- case
- do
- for
- switch

Cada una de estas debe ser un metodo, pero primero deberia simplificarse la linea o el arbol mediante los atomicos.
"""

################
def simplificar_op_matematica(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'OPERADOR MATEMÁTICO':
            aux = eAtomica.validar_operacion_matematica(linea,i-1,i+1)
            if aux != None:
                nueva_linea = simplificar_op_matematica(aux)
        i += 1
    return nueva_linea

def simplificar_declaracion(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'PALABRA RESERVADA':
            aux = eAtomica.validar_declaracion_variable_parametros(nueva_linea, i, i+1)
            if aux != None:
                nueva_linea = simplificar_declaracion(aux)
        i += 1
    return nueva_linea

def simplificar_comparacion(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'OPERADOR COMPARACIÓN':
            aux = eAtomica.validar_comparacion(nueva_linea,i-1,i+1)
            if aux != None:
                asa.imprimir_asa(aux)
                nueva_linea = simplificar_comparacion(aux)
        i += 1
    return nueva_linea

def simplificar_incremental_decremental(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'CARÁCTER INC-DEC':
            aux = eAtomica.validar_incremental_decremental(nueva_linea,i-1,i)
            if aux != None:
                nueva_linea = simplificar_incremental_decremental(aux)
        i += 1
    return nueva_linea

def simplificar_literal_cadena(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'LITERAL DE CADENA':
            aux = cArbol.construir_cadena(nueva_linea)
            if aux != None:
                nueva_linea = simplificar_literal_cadena(aux)
        i += 1
    return nueva_linea

def simplificar_condicion(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos)-1:
        if hijos[i].valor[0][0] == 'OPERADOR LÓGICO':
            aux = eAtomica.validar_condicion(nueva_linea,i-1,i+1)
            if aux != None:
                asa.imprimir_asa(aux)
                nueva_linea = simplificar_condicion(aux)
        i += 1
    return nueva_linea

def simplificar_argumentos_parametros(linea):
    hijos = linea.get_hijos()
    nueva_linea = linea
    i = 0
    while i <= len(hijos) - 1:
        if hijos[i].valor[0][0] == 'SÍMBOLO ESPECIAL' and hijos[i].valor[1][0] == '(':
            aux = eAtomica.validar_parametro(linea, i+1, i+3) or eAtomica.validar_argumento(linea, i+1, i+3) \
                  or eAtomica.validar_argumento_printf(linea, i+1, i+3)
            if aux != None:
                nueva_linea = simplificar_linea(aux)
        i += 1
    return nueva_linea

def simplificar_linea(linea):

    nueva_linea = simplificar_op_matematica(linea)
    nueva_linea = simplificar_declaracion(nueva_linea)
    nueva_linea = simplificar_comparacion(nueva_linea)
    nueva_linea = simplificar_incremental_decremental(nueva_linea)
    nueva_linea = simplificar_literal_cadena(nueva_linea)
    nueva_linea = simplificar_condicion(nueva_linea)
    nueva_linea = simplificar_argumentos_parametros(nueva_linea)
    return nueva_linea

def validar_linea_importe(linea):
    hijos = linea.get_hijos()
    es_valido = True
    i = 0
    estructura = [['SÍMBOLO ESPECIAL','#'],
                  ['PALABRA RESERVADA','include'],
                  ['OPERADOR COMPARACIÓN','<'],
                  ['IDENTIFICADOR',''],
                  ['CARÁCTER PUNTUACIÓN','.'],
                  ['IDENTIFICADOR',''],
                  ['OPERADOR COMPARACIÓN','>']]
    
    for hijo in hijos:
        if not eAtomica.validar_estructura(estructura,hijos):
            return not es_valido
        elif hijo.valor[1][0] != estructura[i][1] and hijo.valor[0][0] != 'IDENTIFICADOR':
            return not es_valido
        i += 1
    return es_valido

def validar_linea_retorno(raiz):
    hijos = raiz.get_hijos()
    es_valido = True
    estructura = [['PALABRA RESERVADA'],
                  ['IDENTIFICADOR','OPERACIÓN MATEMATICA','CONDICIÓN']] #Falta incluir llamado a funciones por tanto esa funcion debe reescribir su papa
    if not eAtomica.validar_estructura(estructura,hijos):
        return not es_valido
    elif not eAtomica.validar_caracter(raiz,';'):
        return not es_valido
    else: 
        return es_valido

def validar_linea_asignacion(raiz):
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

"""validar_declaracion_funcion"""
def validar_linea_declaracion_funcion(raiz):
    hijos = raiz.get_hijos()
    es_valido = True
    estructura = [['DECLARACIÓN VARIABLE/PARAMETROS'],
                  ['SÍMBOLO ESPECIAL'],
                  ['PARAMETRO', 'DECLARACIÓN VARIABLE/PARAMETROS'],
                  ['SÍMBOLO ESPECIAL'],
                  ['SÍMBOLO ESPECIAL']]
    estructura2 = [['DECLARACIÓN VARIABLE/PARAMETROS'],
                   ['SÍMBOLO ESPECIAL'],
                   ['PARAMETRO', 'DECLARACIÓN VARIABLE/PARAMETROS'],
                   ['SÍMBOLO ESPECIAL']]
    estructura3 = [['DECLARACIÓN VARIABLE/PARAMETROS'],
                   ['SÍMBOLO ESPECIAL'],
                   ['SÍMBOLO ESPECIAL']]
    estructura4 = [['DECLARACIÓN VARIABLE/PARAMETROS'],
                   ['SÍMBOLO ESPECIAL'],
                   ['SÍMBOLO ESPECIAL'],
                   ['SÍMBOLO ESPECIAL']]

    if eAtomica.validar_estructura(estructura, hijos) or eAtomica.validar_estructura(estructura2, hijos)\
            or eAtomica.validar_estructura(estructura3, hijos) or eAtomica.validar_estructura(estructura4, hijos):
        if not hijos[1].valor[1][0] == '(' and not hijos[3].valor[1][0] == ')':
            return not es_valido
        else:
            return es_valido
    else:
        return not es_valido

def validar_linea_printf(raiz):
    hijos = raiz.get_hijos()
    es_valido = True
    estructura = [['IDENTIFICADOR'],
                  ['SÍMBOLO ESPECIAL'],
                  ['ARGUMENTO', 'CADENA', 'IDENTIFICADOR', 'OPERACIÓN MATEMATICA', 'NUMERO ENTERO', 'NUMERO FLOTANTE',],
                  ['SÍMBOLO ESPECIAL'],
                  ['CARÁCTER PUNTUACIÓN']]

    if eAtomica.validar_estructura(estructura, hijos):
        if not hijos[0].valor[1][0] == 'printf' and not hijos[1].valor[1][0] == '(' and not hijos[3].valor[1][0] == ')' and not hijos[4].valor[1][0] == ';':
            return not es_valido
        else:
            return es_valido
    else:
        return not es_valido

def validar_comentario_linea(raiz):
    es_valido = True
    hijos = raiz.get_hijos()
    if hijos[0].valor[1][0] == '//':
        return es_valido
    else:
        return not es_valido
    
def validar_linea_declaración(raiz):
    es_valido = True
    hijos = raiz.get_hijos()
    estructura = [['DECLARACIÓN VARIABLE/PARAMETROS'],
                  ['CARÁCTER PUNTUACIÓN']]
    if eAtomica.validar_estructura(estructura,hijos) and eAtomica.validar_caracter(raiz,';'):
        return es_valido
    else: 
        return not es_valido

# HASTA ACA LLEGA LO UTIL

def validar_if(raiz):
    es_valido = True
    hijos = raiz.get_hijos()
    estructura = [['PALABRA RESERVADA'],
                  ['SÍMBOLO ESPECIAL'],
                  ['CONDICIÓN'],
                  ['SÍMBOLO ESPECIAL'],
                  ['SÍMBOLO ESPECIAL']]
    return None

def validar_else(raiz):
    return None



def validar_for(raiz):
    return None

def validar_while(raiz):
    return None




def validar_case(raiz):
    return None

def validar_do(raiz):
    return None



def validar_switch(raiz):
    return None

def validar_comentario_multilinea(codigo,num_linea):
    """raiz = asa.crear_asa_linea(s.separador(codigo[num_linea]))
    hijos = raiz.get_hijos()
    if hijos[0].valor[1][0] == '/*':
        pi = eAtomica.validar_bloque(codigo,num_linea,'*/')
        if pi != None:
            return pi.tamano()-1
        else: 
            return None
    else:
    """
    return None



