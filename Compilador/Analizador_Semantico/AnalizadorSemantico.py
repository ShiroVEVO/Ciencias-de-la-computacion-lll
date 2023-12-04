from Analizador_Semantico.TablaDeSimbolos import Elemento

class AnalizadorSemantico:

    def __init__(self):
        self.tabla = {}         # tabla de simbolos
        self.alcance = []       # pila de alcances
        self.lineas = ([])      # vector de lineas del codigo
        self.errores = []       # variables de apoyo del metodo leerLinea
        self.LINEA = 1          # contador de linea actual
        self.PALABRA = ''       # string para carga al leer
        self.PALABRAS = ([])    # vector para guadar las palabras

    #   Metodo encardo de imprimir las lineas de codigo y los errores recopilados
    def mostrarAnalisis(self):
        if len(self.errores) == 0:
            print("No hay errores semanticos en el analisis!")
        else:
            for x in self.errores:
                print(x)

    #   Metodo encargado del analisis de cada una de la lineas recuperadas
    def analizar(self, codigo):
        self.lineas = codigo
        for i in range(len(self.lineas)):
            self.LINEA = i + 1
            self.analizarLinea(self.lineas[i])
        self.mostrarAnalisis()

    #   Metodo encargado del analisis especifico de una linea
    def analizarLinea(self, linea):
        #   cada vez que empiezo un linea nueva, limpio las variables a utilizar
        self.PALABRA =""
        self.PALABRAS = ([])
        i = 0
        while i < len(linea):
            #   se forma una palabara, luego cae a los otros if para ser clasificada
            if self.esPalabra(linea[i]):
                self.PALABRA += linea[i]

            #   si se llega a leer una '}'
            elif self.esLlaveFinal(linea[i]):
                if len(self.alcance) != 0:
                    self.alcance.pop()
            
            #   si se lee un '(' se procede a recuperar el o los parametros
            elif self.esParametro(linea[i]):
                i = self.formarParametro(linea, i)
                
            #   si se lee un '=' y dos palabaras en la pila, se procede a formar una variable
            elif self.esVariable(linea[i], ):
                i = self.formarVariable(linea, i)                

            # si se lee un '=' y solo hay una palabara en la pila, se procede a actulizar los datos de la variable
            # leida
            elif self.esAsignacionVariable(linea[i]):
                i = self.formarAsignacion(linea, i)

            # si la palabra anterior que se leyo es un 'return', se procede a evaluar su retorno
            elif self.PALABRA == "return":
                i = self.analizarReturn(linea,i)

            # si la palabra anterior que se leyo es un 'void', se procede formar el metodo
            elif self.PALABRA == 'void':
                i = self.formarMetodoVoid(linea, i)

            # si la palabra anterior que se leyo no es un 'void' y no es una varible, se procede a formar el metodo
            elif self.PALABRA == "int" or self.PALABRA == "float" or self.PALABRA == "string":
                self.formarMetodoX(linea, i)

            # si la palabra anterior que se leyo es un condicional, se procede a  analizar la sentencia
            elif self.PALABRA == "while" or self.PALABRA == "if":
                i = self.analizarWhileoIf(linea, i)

            # sino entra en los if anteriores entonces es una palabra y se agrega al vector  de palabras
            else:
                self.PALABRAS.append(self.PALABRA)
                self.PALABRA = ""
                
            i = i + 1

    # Para un mayor entendimiento del los metodos cada uno tiene un nombre significtivo
    def esPalabra(self, caracter):
        return caracter != ' ' and caracter != '=' and caracter != '(' and caracter != ';' and caracter != '}'

    def esLlaveFinal(self, caracter):
        return caracter == '}'

    def esParametro(self, caracter):
        return caracter == '(' and self.PALABRA != "if" and self.PALABRA != "while"

    def esVariable(self, caracter):
        return caracter == "=" and len(self.PALABRAS) == 2

    def esAsignacionVariable(self, caracter):
        return caracter == "=" and len(self.PALABRAS) != 2


    #   Metodo encargado de leer y recuperar las variables de los parametros
    def formarParametro(self, linea, i):
        contador = 0
        funcion = None
        if self.existeElemento(self.PALABRA) is True:
            funcion = self.tabla[self.PALABRA]

        self.PALABRA = ""
        bandera = True
        i = i + 1
        while bandera is True:
            if linea[i] == ')':
                bandera = False
            self.PALABRA += linea[i]
            i = i + 1
        i = i - 1
        if self.PALABRA != ')':
            p = self.PALABRA
            parametroStatements = []
            parametroStatement = ""
            for j in range(len(p)):
                if p[j] != ' ' and p[j] != ',' and p[j] != ')':
                    parametroStatement += p[j]
                elif p[j] == ',' or p[j] == ')' :
                    if len(parametroStatements) != 0:
                        elemento = Elemento()
                        elemento.clasificacion = "variable"
                        elemento.nombre = parametroStatement
                        elemento.tipo = parametroStatements[0]
                        elemento.alcance = self.alcance[len(self.alcance) - 1].nombre
                        parametroStatements.pop()
                        parametroStatement = ""
                        self.tabla[elemento.nombre] = elemento
                        if funcion is not None:
                            funcion.Parametros.append(elemento)
                    else:
                        parametro = funcion.Parametros[contador]
                        try:
                            z = int(parametroStatement)
                            # es entero
                            if parametro.tipo != "int":
                                error = "Error - Linea " + str(self.LINEA) + ": el parametro "+parametroStatement+" es int,se espera un "+parametro.tipo
                                self.errores.append(error)
                        except:

                            try:
                                z = float(parametroStatement)
                                if parametroStatement.find('.') != -1:
                                    if parametro.tipo != "float":
                                        error = "Error - Linea " + str(
                                            self.LINEA) + ": el parametro " + parametroStatement + " es float,se espera un " + parametro.tipo
                                        self.errores.append(error)
                            except:
                                if parametro.tipo != "string":
                                    error = "Error - Linea " + str(
                                        self.LINEA) + ": el parametro " + parametroStatement + " es string,se espera un " + parametro.tipo
                                    self.errores.append(error)
                        #validar
                        contador = contador + 1
                        parametroStatement = ""
                elif p[j] == ' ' and p[j - 1] == ',':
                    j = j
                else:
                    parametroStatements.append(parametroStatement)
                    parametroStatement = ""
        self.PALABRA = ""
        return i


    #   Metodo encargo de analizar y crear las variables
    def formarVariable(self, linea, i):
        banderaError = True
        if len(self.alcance) == 0:
            elemento = Elemento()
            elemento.clasificacion = "variable"
            elemento.nombre = self.PALABRAS[1]
            elemento.tipo = self.PALABRAS[0]
            elemento.alcance = "Global"
            self.PALABRA = ""
            bandera = True
            i = i + 2
            try:
                while bandera is True:
                    self.PALABRA += linea[i]
                    i = i + 1
                    if linea[i] == ';':
                        bandera = False
                i = i - 1
            except:
                print(f"Error en la línea {self.LINEA}")
            
            elemento.valor = self.PALABRA
        else:
            elemento = Elemento()
            elemento.nombre = self.PALABRAS[1]
            elemento.tipo = self.PALABRAS[0]
            elemento.alcance = self.alcance[len(self.alcance) - 1].nombre
            self.PALABRA = ""
            bandera = True
            i = i + 1
            try:
                while bandera is True:
                    if linea[i] == ';':
                        bandera = False
                    self.PALABRA += linea[i]
                    i = i + 1
                i = i - 1
            except:
                print(f"Error en la línea {self.LINEA}")
            elemento.valor = self.PALABRA

        #vemos si la variable que se crea ya existe
        elemento.valor = elemento.valor.replace(';','')
        elemento.valor = elemento.valor.replace(' ','')

        if self.existeElemento(elemento.nombre) is True:
            error = "Error - Linea " + str(self.LINEA) + ": la variable " + elemento.nombre + " ya esta declarada."
            self.errores.append(error)
            banderaError = False

        #evaluamos a lo que se esta igualando
        #es numero
        try:
            j = int(elemento.valor)
            # es entero
            if elemento.tipo != "int":
                error = "Error - Linea " + str(self.LINEA) + ": Asignación incorrecta de un int a un " + elemento.tipo
                self.errores.append(error)
                banderaError = False
        except:
            try:
                j = float(elemento.valor)
                if elemento.valor.find('.') != -1:
                    if elemento.tipo != "float":
                        error = "Error - Linea " + str(self.LINEA) + ": Asignación incorrecta de un float a un " + elemento.tipo
                        self.errores.append(error)
                        banderaError = False
            except:

                if elemento.valor.find('"') == -1:
                    m = elemento.valor
                    palabra = ""
                    banderaMetodo = True
                    e = 0
                    if m.find('(') != -1 and m.find(')') != -1:
                        # es metodo
                        while banderaMetodo is True:
                            palabra += m[e]
                            e = e +1
                            if m[e] == '(':
                                banderaMetodo = False

                        #verifico que el metodo exista
                        if self.existeElemento(palabra) is False:
                            error = "Error - Linea " + str(self.LINEA) + ": el metodo " + palabra + " no esta declarado."
                            self.errores.append(error)
                        else:
                        #verifico si son del mimo tipo
                            if self.tabla[palabra].tipo != elemento.tipo:
                                error = "Error - Linea " + str(self.LINEA) + ": Asignación incorrecta de un " + self.tabla[palabra].tipo + " a un " + elemento.tipo
                                self.errores.append(error)
                        #-------------------------------------------------------------------
                        #verificamos los parametros
                        palabra = ""
                        banderaMetodo = True
                        e = e + 1
                        while banderaMetodo is True:
                            if m[e] == ')':
                                banderaMetodo = False
                            palabra += m[e]
                            e = e + 1
                        e = e - 1

                        if palabra != ')':
                            p = palabra
                            #parametroStatements = []
                            parametroStatement = ""
                            for j in range(len(p)):
                                if p[j] != ' ' and p[j] != ',' and p[j] != ')':
                                    parametroStatement += p[j]
                                elif p[j] == ',' or p[j] == ')':
                                    #if len(parametroStatements) != 0:
                                        if self.existeElemento(parametroStatement) is False:
                                            error = "Error - Linea " + str( self.LINEA) + ": el parametro " + parametroStatement + " no esta definido."
                                            self.errores.append(error)
                                        else:
                                            if elemento.alcance != self.tabla[parametroStatement].alcance:
                                                error = "Error - Linea " + str(self.LINEA) + ": el parametro " + parametroStatement + " no esta definido."
                                                self.errores.append(error)
                                        #parametroStatements.pop()
                                elif p[j] == ' ' and p[j - 1] == ',':
                                    j = j
                                else:
                                    #parametroStatements.append(parametroStatement)
                                    parametroStatement = ""
                        # -------------------------------------------------------------------

                    else:
                        # es variable
                        try:
                            x = self.tabla[elemento.valor]
                            if elemento.tipo != x.tipo:
                                error = "Error - Linea " + str(self.LINEA) + ": Asignación incorrecta de un " + x.tipo + " a un " + elemento.tipo
                                self.errores.append(error)
                                banderaError = False
                        except KeyError:
                                error = "Error - Linea " + str(self.LINEA) + ": la variable " + elemento.valor + " no esta declarada."
                                self.errores.append(error)
                                banderaError = False
                else:
                    # es string
                    if elemento.tipo != "string":
                        error = "Error - Linea " + str(self.LINEA) + ": Asignación incorrecta de un string a un " + elemento.tipo
                        self.errores.append(error)
                        banderaError = False

        if banderaError is True:
            self.tabla[elemento.nombre] = elemento
        return i

    # Busca si existe un elemento en la tabla de simbolos
    def existeElemento(self, nombre):
        try:
            x = self.tabla[nombre]
            return True
        except KeyError:
            return False

    # Metodo encargado de actualizar la verificacion de una variable
    def formarAsignacion(self, linea, i):
        x = self.PALABRAS[0]
        self.PALABRA = ""
        bandera = True
        i = i + 1
        try:
            while bandera is True:
            
                self.PALABRA += linea[i]
                i = i + 1
                if linea[i] == ';':
                    bandera = False
        except:
            print(f"Error en la línea {self.LINEA}")

        if self.existeElemento(x) is False:
            error = "Error - Linea " + str(self.LINEA) + ": la variable " + x + " no esta declarada."
            self.errores.append(error)
        else:
            encontrado = self.tabla[x]
            encontrado.valor = self.PALABRA

        return i

    # Metodo encargado de crear el metodo void, dado que este tipo tiene su caso especial.
    def formarMetodoVoid(self, linea, i):
        elemento = Elemento()
        elemento.clasificacion = "metodo"
        self.PALABRA = ""
        bandera = True
        i = i + 1
        while bandera is True:
            if linea[i] == '(':
                bandera = False

            if linea[i] != '(':
                self.PALABRA += linea[i]
                i = i + 1

        i = i - 1
        elemento.nombre = self.PALABRA
        elemento.alcance = "Global"
        elemento.tipo = "void"
        elemento.valor = "N/A"
        self.alcance.append(elemento)
        #self.PALABRA = ""
        self.tabla[elemento.nombre] = elemento
        return i

    # Metodo encargado de leer la sentecia dentro del if, se verifica que sea valida.
    def analizarWhileoIf(self, linea, i):

        elementoX = Elemento()
        elementoX.nombre = self.PALABRA
        elementoX.tipo = self.alcance[len(self.alcance) - 1].tipo
        elementoX.valor ="N/A"
        elementoX.alcance = self.alcance[len(self.alcance) - 1].nombre
        elementoX.clasificacion = "Condicional"
        self.alcance.append(elementoX)

        vectorContenido = []
        self.PALABRA = ""
        bandera = True
        i = i + 1
        while bandera is True:
            if linea[i] == ')':
                bandera = False
            self.PALABRA += linea[i]
            i = i + 1

        i = i - 1

        if self.PALABRA != ')':
            p = self.PALABRA
            parametroStatements = []
            parametroStatement = ""
            for j in range(len(p)):

                if p[j] != ' ' and p[j] != '<' and p[j] != '>' and p[j] != '=' and p[j] != '!' and p[j] != ')':
                    parametroStatement += p[j]

                elif p[j] == '<' or p[j] == ')'or p[j] == '>'or p[j] == '='or p[j] == '!':
                    try:
                        #caso de que sea numero
                        numero = int(parametroStatement)
                        elemento = Elemento()
                        elemento.clasificacion = "numero"
                        elemento.nombre = numero
                        elemento.tipo = "numero"
                        vectorContenido.append(elemento)
                        parametroStatement = ""

                    except:

                        try:
                            numero = float(parametroStatement)
                            elemento = Elemento()
                            elemento.clasificacion = "numero"
                            elemento.nombre = numero
                            elemento.tipo = "numero"
                            vectorContenido.append(elemento)
                            parametroStatement = ""
                        except:
                            #caso de que no sea numero
                            if parametroStatement != "true" or parametroStatement != "false":

                                if self.existeElemento(parametroStatement) is False :
                                    if  parametroStatement != "":
                                        error = "Error - Linea " + str(self.LINEA) + ": la variable " + parametroStatement + " no esta declarada."
                                        self.errores.append(error)
                                else:
                                    recuperado = self.tabla[parametroStatement]
                                    vectorContenido.append(recuperado)
                                    parametroStatement = ""
            #anilizar vector
            if len(vectorContenido) > 1 :
                objeto1 = vectorContenido[0]
                objeto2 = vectorContenido[1]
                if objeto1.tipo == "numero" and objeto2.tipo == "string" or objeto2.tipo == "numero" and objeto1.tipo == "string":
                    error = "Error - Linea " + str(self.LINEA) + ": variables de diferente tipo."
                    self.errores.append(error)


        self.PALABRA = ""
        return i


    # Metodo encargado de verificar que el return sea valido.
    def analizarReturn(self,linea,i):
        try:
            if len(self.alcance) != 0:
                self.PALABRA = ""
                i =  i + 1
                bandera = True
                while bandera is True:
                    self.PALABRA += linea[i]
                    i = i + 1
                    if linea[i] ==';':
                        bandera = False

                if self.existeElemento(self.PALABRA) is True:
                    hija = self.tabla[self.PALABRA]
                    if hija.alcance != "if" and hija.alcance != "while":

                        try:
                            padre = self.tabla[hija.alcance]
                            if padre.tipo == "void":
                                error = "Error - Linea " + str(self.LINEA) + ": la funcion es void."
                                self.errores.append(error)
                            elif padre.tipo != hija.tipo and hija.tipo != self.alcance[len(self.alcance) - 1].tipo:
                                error = "Error - Linea " + str(self.LINEA) + ": el valor de retorno no coincide."
                                self.errores.append(error)
                            elif hija.tipo != self.alcance[len(self.alcance) - 1].tipo:
                                error = "Error - Linea " + str(self.LINEA) + ": el valor de retorno no coincide."
                                self.errores.append(error)
                        except KeyError:
                            a = 'll'
                else:
                    try:
                        j = int(self.PALABRA)
                        #es entero
                        if self.alcance[len(self.alcance) - 1].tipo != "int":
                            error = "Error - Linea " + str(self.LINEA) + ": el valor de retorno no coincide."
                            self.errores.append(error)
                    except:

                        try:
                            j = float(self.PALABRA)
                            if self.PALABRA.find('.') != -1:
                                if self.alcance[len(self.alcance) - 1].tipo != "float":
                                    # es un float
                                    error = "Error - Linea " + str(self.LINEA) + ": el valor de retorno no coincide."
                                    self.errores.append(error)
                        except:
                            if self.alcance[len(self.alcance) - 1].tipo != "string":
                                error = "Error - Linea " + str(self.LINEA) + ": el valor de retorno no coincide."
                                self.errores.append(error)

            else:
                error = "Error - Linea " + str(self.LINEA) + ": return fuera de ningun alcance."
                self.errores.append(error)
        except:
            print(f"Error en la línea {self.LINEA}")
        return i


    # Metodo encargdo de formar cualquier metodo que no sea void.
    def formarMetodoX(self,linea,i):
        tipo = self.PALABRA
        banderaMetodo = True
        banderaPila = True
        j = i
        j = j + 1
        self.PALABRA = ""
        while banderaPila is True:
            if linea[j] != '=' and linea[j] != ' ' and linea[j] != '(':
                self.PALABRA += linea[j]
            if linea[j] == '=':
                banderaPila = False
                banderaMetodo = False
            if linea[j] == '(':
                banderaPila = False
                banderaMetodo = True
            j = j + 1

        if banderaMetodo is True:
            elemento = Elemento()
            elemento.tipo = tipo
            elemento.nombre = self.PALABRA
            elemento.alcance = "Global"
            elemento.valor = "N/A"
            elemento.clasificacion = "Metodo"
            self.PALABRA = ""
            self.tabla[elemento.nombre] = elemento
            self.alcance.append(elemento)
        else:
            self.PALABRAS.append(tipo)
            self.PALABRA = ""