import Analizador_Lexico.tokens as t
import Recursos.recursos as r

def separador(cadena):
    tokens = []
    i = 0
    while i < len(cadena):
        if cadena[i].isalpha():
            i, token = t.obtener_pReservadas(cadena, i)
            tokens.append(token)

        elif cadena[i].isdigit() or (cadena[0] == '-' and len(cadena) > 1 and cadena[1].isdigit()):
            i, token = t.obtener_numero(cadena, i)
            tokens.append(token)

        elif cadena[i] != " ":
            if i+1 < len(cadena) and not (cadena[i+1].isalpha() or cadena[i+1].isdigit()) and cadena[i+1] != " ":
                i, token = t.obtener_categoria_operador(cadena[i:i+2], i)
                if r.buscar_elemento(token, 0, 'NO ES TOKEN'):
                    i -= 1
                    i, token = t.obtener_categoria_operador(cadena[i], i)
                    i -= 1
                i += 1
            else:
                i, token = t.obtener_categoria_operador(cadena[i], i)
            tokens.append(token)
        else:
            i += 1

    return tokens

