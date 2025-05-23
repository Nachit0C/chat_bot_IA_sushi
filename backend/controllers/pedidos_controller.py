from flask import request, jsonify

from services.ia import chatbot_bienvenida, chatbot_direccion, chatbot_orden
from database.db_functions import update_pedido_nuevo, get_pedido_nuevo, create_pedido, limpiar_pedido_nuevo
from menu import menu_sin_separacion

def update_precio():
    order = get_pedido_nuevo()
    precio = 0
    for item in order["orden"]:
        producto = item["producto"]
        cantidad = item["cantidad"]
        precio_unitario = menu_sin_separacion.get(producto, 0)
        precio += precio_unitario * cantidad
    update_pedido_nuevo(precioFinal=precio)

def order_to_api(action, order):
    if action in ["ORDEN", "ADD_SUBSTRACT"]:
        response = "Su pedido actual es:\n"
        for item in order["orden"]:
            response += f'{item["producto"]} x{item["cantidad"]},\n'
        response += f'Precio parcial: ${order["precioFinal"]}\n'
        response += "Desea agregar o quitar productos a su pedido? O desea confirmarlo?"
        return response

    if action == "ORDEN_CONFIRMADA":
        response = "Pedido confirmado!\nSu pedido es:\n"
        for item in order["orden"]:
            response += f'{item["producto"]} x{item["cantidad"]}\n'
        response += f'Precio total: ${order["precioFinal"]}\n'
        response += "Su pedido está en camino, llegará entre 30 y 45 minutos."
        return response

    if action == "ORDEN_CANCELADA":
        return "Pedido cancelado.\nSi desea realizar un nuevo pedido, indique de nuevo su dirección por favor."

    return ""

def parse_products(payload):
    if payload == "NONE":
        return []
    return [
        {
            "producto": prod.strip(),
            "cantidad": int(cant.strip())
        }
        for prod, cant in (p.split(";") for p in payload.split("|"))
    ]

def add_products_to_order(productos, order):

    for prod in productos:
        existing = next((item for item in order if item["producto"] == prod["producto"]), None)
        if existing:
            existing["cantidad"] += prod["cantidad"]
        else:
            order.append({
                "producto": prod["producto"],
                "cantidad": prod["cantidad"]
            })

    update_pedido_nuevo(orden=order)

def subtract_products_from_order(productos, order):
    for prod in productos:
        for i, item in enumerate(order):
            if item["producto"] == prod["producto"]:
                item["cantidad"] -= prod["cantidad"]
                if item["cantidad"] <= 0:
                    order.pop(i)
                break

    update_pedido_nuevo(orden=order)

def bienvenida_handler(response):
    if response == "_TO_DIRECCION_":
        limpiar_pedido_nuevo()
        update_pedido_nuevo(status="DIRECCION")
        order = get_pedido_nuevo()
        return {"response": "Por favor ingrese el nombre de la calle y el número de su dirección.", "order": order}
    return {"response": response}

def direccion_handler(response):
    if response.startswith("DIRECCION_CONFIRMADA"):
        direccion_nueva = response.split("\n", 1)[1].replace("|", ", ")
        update_pedido_nuevo(direccion= direccion_nueva, orden=[], precioFinal= 0,status="PEDIDO")
        order = get_pedido_nuevo()
        return {"response": "Por favor, nombre los productos que quiere ordenar como aparecen en el menú con sus respectivas cantidades", "order": order}
    return {"response": response}

def order_handler(response):
    action, payload = response.split("\n", 1)
    if action == "ORDEN":
        ordenes = [
            {
                "producto": producto.strip(),
                "cantidad": int(cantidad.strip())
            }
            for producto, cantidad in (item.split(";") for item in payload.split("|"))
        ]
        update_pedido_nuevo(orden=ordenes)
        update_precio()
        order = get_pedido_nuevo()
        return {
            "response": order_to_api(action, order),
            "pedido": order,
            "precioParcial": order["precioFinal"]
        }

    elif action == "ADD_SUBSTRACT":
        pedido = get_pedido_nuevo()
        order = pedido["orden"]
        add_str, sub_str = payload.split("#")
        productos_add = parse_products(add_str)
        productos_sub = parse_products(sub_str)
        add_products_to_order(productos_add, order)
        subtract_products_from_order(productos_sub, order)
        update_precio()
        pedido_res = get_pedido_nuevo()
        return {
            "response": order_to_api(action, pedido_res),
            "pedido": pedido_res
        }

    elif action == "ORDEN_CONFIRMADA":
        order = get_pedido_nuevo()
        pedido_res = create_pedido(direccion=order["direccion"], orden=order["orden"], precioFinal=order["precioFinal"], status="CONFIRMADO")
        limpiar_pedido_nuevo()
        return {
            "response": order_to_api(action, order),
            "pedido": order
        }

    elif action == "ORDEN_CANCELADA":
        order = get_pedido_nuevo()
        pedido_res = create_pedido(direccion=order["direccion"], orden=order["orden"], precioFinal=order["precioFinal"], status="CANCELADO")
        limpiar_pedido_nuevo()
        return {
            "response": order_to_api(action),
            "pedido": order
        }

    else:
        return {"response": response}

def new_message():
    message = request.json.get("message", "")
    try:
        order = get_pedido_nuevo()
        status = order["status"]
        if status == "BIENVENIDA":
            response = chatbot_bienvenida(message)
            return jsonify(bienvenida_handler(response))
        elif status == "DIRECCION":
            response = chatbot_direccion(message)
            return jsonify(direccion_handler(response))
        elif status == "PEDIDO":
            response = chatbot_orden(message)
            return jsonify(order_handler(response))
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500