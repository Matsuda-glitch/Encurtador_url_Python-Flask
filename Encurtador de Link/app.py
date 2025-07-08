from flask import Flask, request, redirect, jsonify
import string
import random
import json
import os

app = Flask(__name__)

URLS_FILE = 'urls.json'

# Carrega as URLs do arquivo JSON, se existir
def load_urls():
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Salva as URLs no arquivo JSON
def save_urls(urls):
    with open(URLS_FILE, 'w') as f:
        json.dump(urls, f)

url_mapping = load_urls()

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def home():
    return "Bem-vindo ao Encurtador de Links! Use a rota /shorten para encurtar URLs."

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_id = generate_short_id()
    url_mapping[short_id] = original_url
    save_urls(url_mapping)
    short_url = request.host_url + short_id
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
