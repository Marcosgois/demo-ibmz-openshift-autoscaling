from flask import Flask
import math
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Aplicação rodando no OpenShift (IBM Z) - Status: OK\n"

@app.route('/load')
def load():
    # Loop matemático pesado para gerar consumo de CPU e acionar o HPA
    x = 0.0001
    for _ in range(2000000):
        x += math.sqrt(x)
    return "Carga processada com sucesso!\n"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)