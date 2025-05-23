from flask import Blueprint, request, jsonify
from controllers.pedidos_controller import new_message

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/send-message', methods=['POST'])
def send_message():
    return new_message()
