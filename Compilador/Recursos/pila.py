class Pila:
    def __init__(self):
        self.items = []

    def __iter__(self):
        self.n = len(self.items)
        return self

    def __next__(self):
        if self.n > 0:
            self.n -= 1
            return self.items[self.n]
        else:
            raise StopIteration
        
    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("pila vacia")

    def elemento_cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        else:
            raise IndexError("pila vacia")

    def tamano(self):
        return len(self.items)
    
    def vaciar(self):
        self.items = []