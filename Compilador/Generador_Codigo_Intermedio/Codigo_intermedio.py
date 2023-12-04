from pythonds.basic.stack import Stack
from Recursos import Recursos as recurso


# ================================= Convertir a Expresion Postfija ===============================

def GenerarArreglo(cadena):  # Modulo para separar la expresion con espacios
    Arreglo = []
    # Eliminar los espacios en blanco
    cadena = cadena.replace(" ", "")
    Operadores = ["+", "-", "*", "/", "=", "(", ")", ">", "<", "<=", ">=", "!=", "==", "!", "%"]
    # recorrer cada elemento de la cadena
    aux = ""
    i = 0
    while (i < len(cadena)):
        substring = cadena[i]
        # Si el substring no es un operador
        if (substring not in Operadores):
            # Si no es el ultimo elemento seguir adicionando la cadena
            if (i != len(cadena) - 1):
                aux = aux + substring
            # Si es el ultimo elemento agregar al arreglo
            else:
                aux = aux + substring
                Arreglo.append(aux)
        # Caso contrario agregar al arreglo
        else:
            Arreglo.append(aux)
            # Verificar si es un simbolo compuesto
            if (i != len(cadena) - 1 and substring + cadena[i + 1] in Operadores):
                Arreglo.append(substring + cadena[i + 1])
                i = i + 1
            # Se verifica que solo sea un operador no compuesto
            else:
                if substring != ')':
                    Arreglo.append(substring)
            aux = ""
        i += 1
    return " ".join(Arreglo)


# Modulo para clasificar un token(numero o palabra)
def EsUnaLetra(token):
    repuesta = True
    for x in token:
        if (x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or x in "abcdefghijklmnopqrstuvwxyz"):
            respuesta = True
        else:
            respuesta = False
    return respuesta


def EsUnNumero(token):
    repuesta = True
    for x in token:
        if (x in "0123456789"):
            respuesta = True
        else:
            respuesta = False
    return respuesta


# Metodo para transformar una expresion en la notacion postfija
def infixToPostfix(infixexpr):
    prec = {}
    prec["<="] = 0
    prec[">="] = 0
    prec["<"] = 0
    prec[">"] = 0
    prec["=="] = 0
    prec["!="] = 0
    prec["="] = 0
    prec["*"] = 3
    prec["%"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if EsUnaLetra(token) or EsUnNumero(token):
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
                    (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


# =================================================================================================

# ================================ Evaluar expresion postfija ==============================
# Evaluar la expresion postfija
def EvaluarExpresionPostfija(expresion, ArregloTabla, contador, index):
    # Contador variable
    Variable = "R"
    # Convertir a arreglo y crear una pila
    ArrExpresion = expresion.split()
    Pila = Stack()
    Operadores = ["+", "-", "*", "/", "=", "(", ")", "%"]  # ,">","<","<=",">=","!=","==","!","%"]
    Comparadores = [">", "<", "<=", ">=", "!=", "==", "!"]
    # Recorrer toda la expresion
    c = 0
    for elemento in ArrExpresion:
        # Si es un Operando , Agregar a la pila
        if (elemento not in Operadores and elemento not in Comparadores):
            Pila.push(elemento)
        # Si es un Operador, sacar los dos ultimos elementos y reemplazar por una variable
        else:
            Variable = "R" + str(contador)

            elemento1 = Pila.pop()
            elemento2 = Pila.pop()
            Pila.push(Variable)

            # Si es un operador y se encuentra al final
            if (c == len(ArrExpresion) - 1):
                if (elemento in Operadores or elemento in Comparadores):  # Si es un operador
                    if (elemento == "="):
                        ArregloTabla = ArregloTabla + [["&" + str(index), "asignar", elemento1, "λ", elemento2]]
                        index += 1
                    else:
                        ArregloTabla = ArregloTabla + [["&" + str(index), elemento, elemento2, elemento1, Variable]]
                        index += 1
                        contador += 1
                    # index+=1  #Se agrego
                    # contador+=1 #Se agrego
                if (elemento in Comparadores):  # Si es un comparador
                    if (elemento == ">" or elemento == "<" or elemento == ">=" or elemento == "<=" or elemento == "!="):
                        ArregloTabla = ArregloTabla + [["&" + str(index), "EsCero", Variable, "λ", "&dir"]]
                        index += 1
                    if (elemento == "=="):
                        ArregloTabla = ArregloTabla + [["&" + str(index), "EsCero", Variable, "λ", "&dir"]]
                        index += 1
                    # index+=1   #Se agrego
                    # contador+=1  #Se agrego
            else:
                ArregloTabla = ArregloTabla + [["&" + str(index), elemento, elemento2, elemento1, Variable]]
                index += 1  # Se agrego
                contador += 1  # Se agrego
            # index+=1
            # contador+=1
        c = c + 1
    return ArregloTabla, contador, index


# Generar tabla leyendo el archivo de texto:
def GenerarCodigoIntermedio(codigo):
    
    lineas = recurso.formatear_archivo(codigo)

    # Cear la tabla que contendra al codigo intermedio
    Tabla = []
    con = 1  # Para incrementar el indice de las variables
    ind = 0  # Para incrementar el indice de la instruccion(memoria)
    # La pila para guardar las palabras reservadas que hay en el programa IF,ELSE,WHILE,ETC
    PilaReservadas = Stack()
    # Crear arreglos que contengan las direcciones de los saltos y EsCero
    ArrEsCero = []
    ArrSaltos = []

    # Recorrer cada linea:
    for line in lineas:
        # Eliminar los espacios en blanco
        line = line.replace(" ", "")

        # Si la linea empieza con if
        if (line.startswith("if")):
            # Extraer la clausula que esta dentro del if
            sentencia = line[3:len(line) - 1:]
            # Llamar al modulo, evaluar expresion postfija(y se agrega a la tabla resultante)
            Tabla, con, ind = EvaluarExpresionPostfija(infixToPostfix(GenerarArreglo(sentencia)), Tabla, con, ind)
            # Poner la palabra if a la pila de palabras reservadas
            PilaReservadas.push("if")

        elif (line.startswith("else")):
            # No hacer nada y continuar a la linea siguiente
            PilaReservadas.push("else")
        elif (line.startswith("while")):
            # Extraer la clausula que esta dentro del while
            sentencia = line[6:len(line) - 1:]

            # Agregar la posicion inicial de esta linea al ArrSaltos
            ArrSaltos = ["&" + str(ind)] + ArrSaltos

            # Llamar al modulo, evaluar expresion postfija
            Tabla, con, ind = EvaluarExpresionPostfija(infixToPostfix(GenerarArreglo(sentencia)), Tabla, con, ind)
            # Poner la palabra while a la pila de palabras reservadas
            PilaReservadas.push("while")



        else:
            # Si la estructura es SECUENCIAL(no contiene if,else , ni while)
            if (line != "{" and line != "}" and line != ""):
                # evaluar la expresion del tipo secuencial
                Tabla, con, ind = EvaluarExpresionPostfija(infixToPostfix(GenerarArreglo(line)), Tabla, con, ind)


            else:
                if (line == "{"):  # Empieza un simbolo de apertura que pertenezca a una palabra reservada If,WHILE
                    pass

                if (line == "}"):  # Linea contiene al simbolo de cierre

                    # Agregar a la tabla la fila saltar, si es un IF, While
                    reservadaF = PilaReservadas.peek()
                    if (reservadaF == "if" or reservadaF == "while"):
                        Tabla = Tabla + [["&" + str(ind), "Saltar", "λ", "λ", "&Cierre"]]
                        # AGREGADO:
                        # Agregar la posicion inicial de esta linea al ArrSaltos
                        ArrEsCero = ["&" + str(ind + 1)] + ArrEsCero
                        con += 1
                        ind += 1
                        PilaReservadas.pop()
                    else:  # hay un else en la pila
                        PilaReservadas.pop()
                        # Agregado:
                        ArrSaltos = ["&" + str(ind)] + ArrSaltos
    # Agregar una ultima fila a la tabla
    Tabla = Tabla + [["&" + str(ind), " ", " ", " ", " "]]
    return Tabla, ArrSaltos, ArrEsCero


# Modulo para cambiar las direcciones en la tabla
def AgregarDirecciones(Tabla, ArregloEsCero, ArregloSaltos):
    i = 0
    j = 0
    for fila in Tabla:
        if (fila[1] == "EsCero" and i != len(ArregloEsCero)):
            fila[4] = ArregloEsCero[i]
            i += 1
        elif (fila[1] == "Saltar" and j != len(ArregloSaltos)):
            fila[4] = ArregloSaltos[j]
            j += 1
    return Tabla
