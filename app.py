# frontend/app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='frontend/templates')

# URL do seu backend FastAPI
API_URL = "http://localhost:8000/autenticadores"

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para criar um novo autenticador
@app.route('/create_autenticador', methods=['POST'])
def create_autenticador():
    data = {
        "orgao": request.form['orgao'],
        "status": request.form['status'],
        "chave_autenticacao": request.form['chave_autenticacao'],
        "data_expiracao": request.form.get('data_expiracao')  # Pode ser vazio
    }
    
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Falha ao criar autenticador"}), 400

# Rota para listar autenticadores
@app.route('/list_autenticadores', methods=['GET'])
def list_autenticadores():
    response = requests.get(API_URL)
    return jsonify(response.json()), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
