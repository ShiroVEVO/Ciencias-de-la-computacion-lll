palabras_reservadas = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
                       'double', 'else', 'enum', 'extern', 'float', 'for', 'got', 'if', 'int',
                       'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
                       'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while','include']

oAsignacion = ['=', '+=', '-=', '*=', '/=', '&=']

oMatematico = ['+', '-', '*', '/', '%']

oLogico = ['&&', '||', '!']

oComparacion = ['==', '!=', '<', '>', '<=', '>=']

oIncdec = ['++', '--']

sEspecial = ['(', ')', '[', ']', '#', '{', '}']

comentario = ['//', '/*', '*/']

lCadena = ['"']

puntuador = ['.', ';', ',', ':']

'''Obtiene como párametro las listas de palabras de cada linea y compara con la lista de palabras reservada'''
def obtener_pReservadas(cadena, i):
    j = i
    while j < len(cadena) and (cadena[j].isalpha() or cadena[j].isdigit()):
        j += 1
    for elemento in palabras_reservadas:
        if elemento == cadena[i:j]:
            return j, [['PALABRA RESERVADA'], [cadena[i:j]]]
    return obtener_identificador(cadena, i)

'''Obtiene una cadena la cual sigue recorriendo desde el párametro enviado i hasta que ya no se cumplan
las condiciones (solo cadenas-números-_)'''
def obtener_identificador(cadena, i):
    j = i
    while j < len(cadena) and (cadena[j].isalpha() or cadena[j].isdigit() or cadena[j] == '_'):
        j += 1
    return j, [['IDENTIFICADOR'], [cadena[i:j]]]

#Solo distingue entre entero y flotante
def obtener_numero(cadena, i):
    j = i
    punto_decimal = False
    parte_decimal = False

    while j < len(cadena):
        if cadena[j].isdigit():
            parte_decimal = True
        elif cadena[j] == '.' and not punto_decimal and parte_decimal:
            punto_decimal = True
        else:
            break
        j += 1

    if punto_decimal and parte_decimal:
        return j, [['NUMERO FLOTANTE'], [cadena[i:j]]]
    else:
        return j, [['NUMERO ENTERO'], [cadena[i:j]]]

#Un método que puede clasificar cada uno de los operadores diferente
def obtener_operador(cadena, nlista, i):
    j = i + 1
    if nlista == 0:
        return j, [['OPERADOR ASIGNACIÓN'], [cadena]]
    elif nlista == 1:
        return j, [['OPERADOR MATEMÁTICO'], [cadena]]
    elif nlista == 2:
        return j, [['OPERADOR LÓGICO'], [cadena]]
    elif nlista == 3:
        return j, [['OPERADOR COMPARACIÓN'], [cadena]]
    elif nlista == 4:
        return j, [['SÍMBOLO ESPECIAL'], [cadena]]
    elif nlista == 5:
        return j, [['COMENTARIO'], [cadena]]
    elif nlista == 6:
        return j, [['LITERAL DE CADENA'], [cadena]]
    elif nlista == 7:
        return j, [['CARÁCTER PUNTUACIÓN'], [cadena]]
    else:
        return j, [['CARÁCTER INC-DEC'], [cadena]]

'''Recibe la cadena y la va comparando con cada lista de tokens'''
def obtener_categoria_operador(cadena, i):
    operadores = [oAsignacion, oMatematico, oLogico, oComparacion, sEspecial, comentario, lCadena, puntuador, oIncdec]
    for nlista, lista in enumerate(operadores):
        if cadena in lista:
            return obtener_operador(cadena, nlista, i)
    return i+1, [['NO ES TOKEN'], [cadena]]




