import tokens as t

def encontrar_elemento_igual(lista, valor):
    for elemento in lista:
        if elemento[0] == valor:
            return True
    return False

# Solo distingue entre palabras reservadas, identificadores, operadores y número enteros y flotantes :3
# No tiene en cuenta los espacios
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
                if encontrar_elemento_igual(token, 'NO ES OPERADOR'):
                    print('token')
                    i, token = t.obtener_categoria_operador(cadena[i-1], i)
            else:
                i, token = t.obtener_categoria_operador(cadena[i], i)
            tokens.append(token)
        else:
            i += 1

    return tokens

