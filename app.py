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

@app.route('/memory-load')
def memory_load():
    # Aloca aproximadamente 50MB de memória por requisição e guarda na lista global
    global memory_hog
    memory_hog.append(' ' * (50 * 1024 * 1024)) 
    return f"Memória alocada! O pod está segurando {len(memory_hog)} bloco(s) de 50MB.\n"

@app.route('/memory-clear')
def memory_clear():
    # Libera a memória alocada
    global memory_hog
    memory_hog = []
    return "Memória liberada com sucesso!\n"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)