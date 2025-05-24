from flask import Flask, jsonify, request
from flask_cors import CORS
import os 
from dotenv import load_dotenv

from routes.pedidos_routes import pedidos_bp
from database.db_functions import get_data
from database.db_functions import create_pedido_nuevo

load_dotenv()

PORT = os.getenv("PORT", 500)

app = Flask(__name__)
CORS(app)

app.register_blueprint(pedidos_bp, url_prefix='/')

@app.route('/')
def home():
    return jsonify('Bienvenido al servidor.')

@app.route('/pedidos')
def pedidos():
    try:
        result = get_data()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"error": "Hubo un problema en el servidor"}), 500

create_pedido_nuevo()

if __name__ == '__main__':
    app.run(port=PORT)
