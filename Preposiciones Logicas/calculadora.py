import ttg
import re


def proposicion(p):
    aux = ''
    aux = p.replace('^', ' and ', p.count("^"))
    p = aux.replace('v', ' or ', p.count("v"))
    aux = p.replace('→', ' => ', p.count("→"))
    p = aux.replace('↔', ' = ', p.count("↔"))

    return p


def variables(s):
    variables = []
    index = 97
    while index <= 122:
        char = chr(index)
        if char in s and char != "v":
            variables.append(char)
        index += 1
    return variables


def mostrar_resultado(prep):
    try:
        aux = proposicion(prep)
        operadores_a_buscar = ['and', 'or', '=>', '=']
        parentesis = ""
        pila = []
        for caracter in aux:
            if caracter in '([{':
                pila.append(caracter)
            elif caracter in ')]}':
                if not pila:
                    continue
                par_abierto = pila.pop()
                if (caracter == ')' and par_abierto == '(') or \
                    (caracter == ']' and par_abierto == '[') or \
                    (caracter == '}' and par_abierto == '{'):
                    parentesis += par_abierto + caracter + ", "
        aux = aux.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
        var = variables(prep)
        table = ttg.Truths(var, [aux])
        patron_operadores = '|'.join(re.escape(op) for op in operadores_a_buscar)
        coincidencias = re.findall(patron_operadores, aux)
        operadores = ', '.join(coincidencias)
        print(operadores)
        return {"tabla": aux, "variables": var, "parentesis": parentesis, "operadores": operadores, "valoracion": table.valuation()} 
        #return {"tabla": table.as_tabulate(table_format="html", index=False), "valoracion": table.valuation()}
    except BaseException:
        print('valió')
