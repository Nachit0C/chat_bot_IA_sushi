import os 
from mongoengine import connect, Document, EmbeddedDocument, StringField, IntField, FloatField, EmbeddedDocumentListField
from mongoengine.queryset.visitor import Q
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/MongoDB1")
connect(host=MONGO_URL)

class Counter(Document):
    id = StringField(primary_key=True)
    seq = IntField(default=0)

def get_next_sequence(name):
    counter = Counter.objects(id=name).modify(upsert=True, new=True, inc__seq=1)
    return counter.seq

class OrderItem(EmbeddedDocument):
    producto = StringField(required=True)
    cantidad = IntField(required=True, min_value=1)

class Pedido(Document):
    numeroPedido = IntField()
    direccion = StringField(required=True)
    orden = EmbeddedDocumentListField(OrderItem, required=True)
    precioFinal = FloatField(required=True)
    status = StringField(
        required=True,
        choices=("CANCELADO", "CONFIRMADO")
    )

    def save(self, *args, **kwargs):
        if not self.numeroPedido:
            self.numeroPedido = get_next_sequence("numeroPedido")
        super().save(*args, **kwargs)

    meta = {
        "collection": "Pedidos",
        "ordering": ["-numeroPedido"],
        "strict": False,
    }

class PedidoNuevo(Document):
    status = StringField(
        required=True,
        choices=("BIENVENIDA", "DIRECCION", "PEDIDO", "CONFIRMADO", "CANCELADO")
    )
    direccion = StringField()
    orden = EmbeddedDocumentListField(OrderItem)
    precioFinal = FloatField(default=0)

    meta = {
        "collection": "PedidosNuevos",
        "strict": False,
    }