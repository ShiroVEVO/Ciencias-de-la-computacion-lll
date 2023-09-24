class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def __len__(self):
        return len(self.hijos)
    
    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
    
    def get_hijos(self):
        return self.hijos
    
    def ultimo_hijo(self):
        if self.hijos:
            ultimo_hijo = self.hijos[-1]
            return ultimo_hijo
        else:
            return None