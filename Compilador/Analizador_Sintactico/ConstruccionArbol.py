from Analizador_Sintactico import EstructurasAtomicas as eAtomicas
from Recursos import ArbolSintaxisAbstracta as asa
def construir_cadena(raiz):
    hijos = raiz.get_hijos()
    while True:
        i = 0
        primera_cadena = True
        cadena_encontrada = False
        inicio = -1
        fin = -1

        while i < len(hijos):
            if hijos[i].valor[0][0] == 'LITERAL DE CADENA' and hijos[i].valor[1][0] == '"' and primera_cadena is True:
                inicio = i
                primera_cadena = False
                cadena_encontrada = True
            elif hijos[i].valor[0][0] == 'LITERAL DE CADENA' and hijos[i].valor[1][0] == '"' and primera_cadena is False:
                fin = i
                primera_cadena = True
                cadena_encontrada = True
                if inicio != -1 and fin != -1:
                    raiz = eAtomicas.validar_cadena(raiz, inicio, fin)
                    construir_cadena(raiz)
            i += 1

        if not cadena_encontrada:
            break

    return raiz










