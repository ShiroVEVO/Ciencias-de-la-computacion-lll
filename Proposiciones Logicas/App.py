from flask import Flask, render_template, request, jsonify
import calculadora


class Mensaje:
    message = ''
    records = []    


# inicializacion
app = Flask(__name__)


# routes
@app.route('/calculadora-logica')
@app.route('/')
def Index():      
    return render_template('index.html')

@app.route('/solvePreposition', methods=['POST'])
def solvePreposition():    
    if request.method == 'POST':
        print("hey")
        preposicion = request.form['prep']
        print("preposición: " + preposicion)
        resultados = calculadora.mostrar_resultado(preposicion)
        print(resultados)
        return jsonify(resultados)
    return jsonify(message = 'Error en add')



# inicio de la app
if __name__ == "__main__":
    app.run(port=8080, debug=True)
