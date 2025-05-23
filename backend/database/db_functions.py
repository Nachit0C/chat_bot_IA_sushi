from database.db import Pedido, PedidoNuevo, OrderItem
from bson import ObjectId
from datetime import datetime

def mongo_to_dict(document):
    if document is None:
        return None
    
    def clean_bson(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: clean_bson(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_bson(i) for i in obj]
        else:
            return obj
    
    raw = document.to_mongo()
    return clean_bson(raw)

def create_pedido(direccion, orden, precioFinal, status):
    try:
        items = [OrderItem(**item) for item in orden]
        new_order = Pedido(
            direccion=direccion,
            orden=items,
            precioFinal=precioFinal,
            status = status
        )
        new_order.save()
        return mongo_to_dict(new_order)
    except Exception as e:
        print(f"Error al crear la orden: {e}")
        return None

def update_pedido(numeroPedido, update_fields):
    try:
        pedido = Pedido.objects(numeroPedido=numeroPedido).first()
        if not pedido:
            print(f"Pedido con número {numeroPedido} no encontrado.")
            return None

        if "direccion" in update_fields:
            pedido.direccion = update_fields["direccion"]

        if "orden" in update_fields:
            pedido.orden = [OrderItem(**item) for item in update_fields["orden"]]

        if "precioFinal" in update_fields:
            pedido.precioFinal = update_fields["precioFinal"]

        if "status" in update_fields:
            pedido.status = update_fields["status"]

        pedido.save()
        return mongo_to_dict(pedido)

    except Exception as e:
        print(f"Error al actualizar la orden: {e}")
        return None

def limpiar_pedido_nuevo():
    try:
        pedido = PedidoNuevo.objects().first()
        if pedido:
            pedido.direccion = ""
            pedido.orden = []
            pedido.precioFinal = 0
            pedido.status = "BIENVENIDA"
            pedido.save()
    except Exception as e:
        print(f"Error al limpiar pedido en curso: {e}")

def create_pedido_nuevo():
    try:
        pedido_existente = PedidoNuevo.objects().first()
        if pedido_existente:
            limpiar_pedido_nuevo()
            return pedido_existente 

        nuevo = PedidoNuevo( direccion= "", orden = [], precioFinal = 0 ,status="BIENVENIDA")
        nuevo.save()
        return mongo_to_dict(nuevo)
    except Exception as e:
        print(f"Error al crear pedido en curso: {e}")
        return None

def update_pedido_nuevo(**update_fields):
    try:
        pedido = PedidoNuevo.objects().first()
        if not pedido:
            print("No hay pedido en curso para actualizar.")
            return None

        if "status" in update_fields:
            pedido.status = update_fields["status"]
        if "direccion" in update_fields:
            pedido.direccion = update_fields["direccion"]
        if "orden" in update_fields:
            pedido.orden = [OrderItem(**item) for item in update_fields["orden"]]
        if "precioFinal" in update_fields:
            pedido.precioFinal = update_fields["precioFinal"]

        pedido.save()
        return mongo_to_dict(pedido)
    except Exception as e:
        print(f"Error al actualizar pedido en curso: {e}")
        return None

def get_pedido_nuevo():
    try:
        pedido = PedidoNuevo.objects().first()
        return mongo_to_dict(pedido)
    except Exception as e:
        print(f"Error al obtener pedido en curso: {e}")
        return None

def delete_pedido_nuevo():
    try:
        PedidoNuevo.objects().delete()
        print(f'Exito al eliminar PedidoNuevo')
    except Exception as e:
        print(f"Error al eliminar pedido en curso: {e}")

def get_data():
    try:
        pedidos = Pedido.objects()
        return [mongo_to_dict(p) for p in pedidos]
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return []
