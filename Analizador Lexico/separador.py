import tokens as t


# Solo distingue entre palabras reservadas, identificadores, operadores y número enteros y flotantes :3
# No tiene en cuenta los espacios
def separador(cadena):
    tokens = []
    i = 0
    while i < len(cadena):
        if cadena[i].isalpha():
            # Aqui separa cada cadena que pueda ser un identificador, pero primero resiva si esta dentro
            # de la palabras claves, no estoy segura si hay casos donde las palabras claves puedan ser validas
            # sin necesidad de un espacio o un parentesis entre otros tokens.
            i, token = t.obtener_pReservadas(cadena, i)
            tokens.append(token)
        elif cadena[i].isdigit() or (cadena[0] == '-' and len(cadena) > 1 and cadena[1].isdigit()):
            # Numeros
            i, token = t.obtener_numero(cadena, i)
            tokens.append(token)
        elif cadena[i] != " ":
            # Todo lo que no sea espacios
            i, token = t.obtener_operador(cadena, i)
            tokens.append(token)
        else:
            i += 1

    return tokens


linea_codigo = "int medusa1=lin555a+roma3;"
linea_codigo = "int   a=-3.3+3"
tokens = separador(linea_codigo)
print(tokens)
