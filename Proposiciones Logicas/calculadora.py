import ttg


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
        var = variables(prep)
        table = ttg.Truths(var, [aux])
        return {"tabla": table.as_tabulate(table_format="html", index=False), "valoracion": table.valuation()}
    except BaseException:
        print('Entrada invalida')
