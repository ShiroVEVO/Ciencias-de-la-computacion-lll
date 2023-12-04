class Elemento:

    def __init__(self):
        self.nombre = ""        #nombre
        self.tipo = ""          #int float,string,void...
        self.valor = ""         #el valor que recibe en caso de ser variable
        self.alcance = ""
        self.clasificacion = "" # si es metodo,variable o condional.
        self.Parametros = ([])  # vector para guadar los parametros