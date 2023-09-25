from Analizador_Sintactico import EstructurasAtomicas as eAtomicas

def construir_variables_parametros(raiz):
    i = 0
    hijos = raiz.get_hijos()
    while i < len(hijos):
        if hijos[i].valor[0][0] == 'PALABRA RESERVADA' and hijos[i + 1].valor[0][0] == 'IDENTIFICADOR':
            raiz = eAtomicas.validar_declaracion_variable_parametros(raiz, i, i + 1)
            if raiz is None:
                return raiz
            else:
                hijos = raiz.get_hijos()
                i = 0
        else:
            i += 1
    return raiz


def construir_argumento(raiz):
    i = 0
    hijos = raiz.get_hijos()
    while i < len(hijos):
        if hijos[i].valor[0][0] == 'SÍMBOLO ESPECIAL' and hijos[i].valor[1][0] == '(':
            j = i + 1
            while not (hijos[j].valor[0][0] == 'SÍMBOLO ESPECIAL' and hijos[j].valor[1][0] == ')'):
                if hijos[j].valor[0][0] == 'DECLARACIÓN VARIABLE/PARAMETROS':
                    raiz = eAtomicas.validar_argumento(raiz, j, j + 1) or eAtomicas.validar_argumento(raiz, j, j)
                    if raiz is None:
                        return raiz
                    else:
                        hijos = raiz.get_hijos()
                        i = 0
                else:
                    j += 1
            return raiz
        else:
            i += 1
    return raiz


def construir_argumentos(raiz):
    i = 0
    hijos = raiz.get_hijos()
    while i < len(hijos):
        if hijos[i].valor[0][0] == 'SÍMBOLO ESPECIAL' and hijos[i].valor[1][0] == '(':
            inicio = i + 1
            i += 1
        elif hijos[i].valor[0][0] == 'SÍMBOLO ESPECIAL' and hijos[i].valor[1][0] == ')':
            fin = i - 1
            i += 1
        else:
            i += 1
    return eAtomicas.validar_argumentos(raiz, inicio, fin)