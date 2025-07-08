from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

# Dicionário para armazenar os links encurtados
url_mapping = {}

def generate_short_id(length=6):
    """Gera um ID curto aleatório."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    return "Bem-vindo ao Encurtador de Links! Use a rota /shorten para encurtar URLs."

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Encurta uma URL."""
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_id = generate_short_id()
    url_mapping[short_id] = original_url
    short_url = request.host_url + short_id
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    """Redireciona para a URL original."""
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
