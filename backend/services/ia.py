import cohere
import os 
from menu import menu_string, menu_sin_separacion_string
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY", "")
if not API_KEY:
    print("Advertencia: No se encontró la clave de API. Algunas funcionalidades pueden no estar disponibles.")
    co = None
else:
    co = cohere.ClientV2(API_KEY)

def chatbot_bienvenida(request):
    set_up_messages = [
        {"role": "system", "content": """
        You are part of a chatbot for a sushi delivery service. Your purpose is to welcome clients and direct them to the appropriate flow based on their intent. You will respond in Spanish only. Forget the context every time a new conversation starts.

        - Default Message: If the user starts the conversation, respond: "Buenas noches, esto es Tienda de Sushi. En qué puedo ayudarle?".
        - Orders: If the user wants to make an order, respond with "_TO_DIRECCION_".
        - Menu: If the user requests the menu, respond with the following string: """ + menu_string + """.
        - Opening Hours: If the user asks about the opening hours, respond with: "El horario de atención es de 19:00 a 00:00".
        - Open/Close Status: If the user asks if the store is open, respond based on the current time at -3 GMT:
            - "El horario de atención es de 19:00 a 00:00."
        - If the user thanks you in any way, respond: "Gracias por elegirnos. En qué más puedo ayudarte?".
        - Unrelated Queries: If the user asks about something unrelated, respond: "Lo siento, no puedo ayudarte con eso."
        *- If the user thanks you BUT the user requests an order, don't respond "Gracias por elegirnos. En qué más puedo ayudarte?", just respond "_TO_DIRECCION_"-
        """},
        {"role": "user", "content": "Buenas noches"},
        {"role": "assistant", "content": "Buenas noches, esto es Tienda de Sushi. En qué puedo ayudarle?"},
        {"role": "user", "content": "Hola!"},
        {"role": "assistant", "content": "Buenas noches, esto es Tienda de Sushi. En qué puedo ayudarle?"},
        {"role": "user", "content": "Quisiera realizar un pedido"},
        {"role": "assistant", "content": "_TO_DIRECCION_"},
        {"role": "user", "content": "Para hacer un pedido"},
        {"role": "assistant", "content": "_TO_DIRECCION_"},
        {"role": "user", "content": "Quisiera ver el menu, por favor"},
        {"role": "assistant", "content": menu_string},
        {"role": "user", "content": "A qué hora abren?"},
        {"role": "assistant", "content": "El horario de atención es de 19:00 a 00:00"},
        {"role": "user", "content": "A qué hora cierran?"},
        {"role": "assistant", "content": "El horario de atención es de 19:00 a 00:00"},
        {"role": "user", "content": "Gracias. Quisiera realizar un pedido"},
        {"role": "assistant", "content": "_TO_DIRECCION_"},
    ]

    try:
        response = co.chat(
            model="command-a-03-2025",
            messages= set_up_messages + [{ "role": "user", "content": request }],
        )
        return response.message.content[0].text if response.message.content[0].text else 'No se pudo realizar el pedido, intente de nuevo en unos minutos'
    except Exception as e:
        print(f"Error: {e}")
        return 'Ocurrió un error procesando tu solicitud. Intenta de nuevo más tarde.'

def chatbot_direccion(request):
    import re
    if not re.search(r'\d+', request):
        return 'Por favor ingrese una dirección válida con nombre de calle y número.'

    set_up_messages = [
        {"role": "system", "content": """
        You are part of a chatbot for a sushi delivery service. Your sole purpose is to take addresses from clients. You will respond in Spanish only. You will follow the instructions below and you will forget the context everytime start a new conversation

        - The user will send you the street name and number. You will have to extract it from the message and respond: 
            "DIRECCION_CONFIRMADA\n$streetName$|%streetNumber%", where $streetName$ is the name of the street and %streetNumber% the number of the street you extracted.

        - If the user sends a message about another part of the order (asks about products or prices), respond: "Por favor ingrese su dirección primero."

        - If the user sends an unclear message, respond: "No puedo procesar su solicitud, por favor ingrese su dirección así podemos continuar con el pedido."
        """},
        {"role": "user", "content": "Olazaban 742"},
        {"role": "assistant", "content": "DIRECCION_CONFIRMADA\nOlazabal|742"},
        {"role": "user", "content": "Avenida Rivadavia 1152"},
        {"role": "assistant", "content": "DIRECCION_CONFIRMADA\nAvenida Rivadavia|1152"},
        {"role": "user", "content": "monte hermoso 558"},
        {"role": "assistant", "content": "DIRECCION_CONFIRMADA\nMonte Hermoso|558"},
        {"role": "user", "content": "$streetName$ %streetNumber%"},
        {"role": "assistant", "content": "DIRECCION_CONFIRMADA\n$streetName$|%streetNumber%"},
    ]
    try:
        response = co.chat(
            model='command-a-03-2025',
            messages= set_up_messages + [{"role": "user", "content": request}]
        )
        return response.message.content[0].text if response.message.content[0].text else 'No se pudo realizar el pedido, intente de nuevo en unos minutos'
    except Exception as e:
        print(f"Error: {e}")
        return 'Ocurrió un error procesando tu solicitud. Intenta de nuevo más tarde.'


def chatbot_orden(request):
    set_up_messages = [
        {"role": "system", "content": """
        You are part of a chatbot for a sushi delivery service. Your sole purpose is to take orders from user. You will respond in Spanish only. You will follow the instructions below, you forget the context in whenever a conversation starts.

        - The user will send you products and quantities from this menu: """ + menu_sin_separacion_string + """. where each name is the product and the number is the price.
        - Extract product and quantity from the user's message and respond: "ORDEN\n[[product1]];{{quantity1}}|[[product2]];{{quantity2}}", where [[productX]] is the name of the product and {{quantityX}} the quantity selected for that product. You will show each product listed as demonstrated avobe.
        - Add/subtract logic: "ADD_SUBSTRACT\n...#..." format as specified, placing the product/s and quantity/es to add before the '#' and the product/s and quantity/es to substract after the '#'.
        - If the user only wants to add one or more product/s or quantity/es to the order. You will respond:"ADD_SUBSTRACT\n[[product1]];{{quantity1}}|[[product2]];{{quantity2}}#NONE" placing the product/s and quantity/es to add before the '#' and 'NONE' after the' '#'.
        - If the user only wants to substract one or more product/s or quantity/es to the order. You will respond:"ADD_SUBSTRACT\nNONE#[[product1]];{{quantity1}}|[[product2]];{{quantity2}}" placing 'NONE' before the '#' and the product/s and quantity/es to substract after the '#'.
        - Cancel order: "ORDEN_CANCELADA\nA"
        - Confirm order: "ORDEN_CONFIRMADA\nA"
        - Unknown products: "[[productX]] no se encuentra en el menu, por favor sleccione otro"
        - Clarify missing info: "No entendí su solicitud..." or ask politely for product and quantity
        """},
        {"role": "user", "content": "Quisiera 2 edamame por favor"},
        {"role": "assistant", "content": "ORDEN\nedamame;2"},
        {"role": "user", "content": "Quiero agregar 1 yakitori"},
        {"role": "assistant", "content": "ADD_SUBSTRACT\nyakitori;1#NONE"},
        {"role": "user", "content": "Si, confirmo mi pedido"},
        {"role": "assistant", "content": "ORDEN_CONFIRMADA\nA"},
        {"role": "user", "content": "Quiero cancelar mi pedido"},
        {"role": 'user', "content": 'Quiero 3 gyozax3 y 1 bao'},
        {"role": 'assistant', "content":"ORDEN\ngyozax3;3|bao;1"},
        {"role": 'user', "content": 'Si, por favor'},
        {"role": 'assistant', "content": 'ORDEN_CONFIRMADA\nA'},
        {"role": 'user', "content": 'Quiero 1 combo1 y 3 combo2'},
        {"role": 'assistant', "content": "ORDEN\ncombo1;1|combo2;3"},
        {"role": 'user', "content": 'Si, gracias'},
        {"role": 'assistant', "content": 'ORDEN_CONFIRMADA\nA'},
        {"role": 'user', "content": 'Si'},
        {"role": 'assistant', "content": 'ORDEN_CONFIRMADA\nA'},
        {"role": 'user', "content": 'Quiero 1 salmonNigirix6, 3 bao y 5 spicycrabRollx6'},
        {"role": 'assistant', "content": "ORDEN\nsalmonNigirix6;1|bao;3|spicycrabRollx6;5"},
        {"role": 'user', "content": 'Quisiera remover los 3 bao'},
        {"role": 'assistant', "content": "ADD_SUBSTRACT\nNONE#bao;3"},
        {"role": 'user', "content": "No, voy a cancelar el pedido"},
        {"role": 'assistant', "content": 'ORDEN_CANCELADA\nA'},
        {"role": 'user', "content": 'Quiero 1 salmonNigirix6, 3 bao y 5 spicycrabRollx6'},
        {"role": 'assistant', "content": "ORDEN\nsalmonNigirix6;1|bao;3|spicycrabRollx6;5"},
        {"role": 'user',"content": 'Quisiera remover 3 spicycrabRollx6 y añadir 1 bao'},
        {"role": 'assistant',"content": "ADD_SUBSTRACT\nbao;1#spicycrabRollx6;3"},
        {"role": 'user',"content": 'Si, confirmo mi pedido'},
        {"role": 'assistant',"content": 'ORDEN_CONFIRMADA\nA'},
        {"role": 'user',"content": 'Quiero {{quantity1}} [[product1]]'},
        {"role": 'assistant',"content": "ORDEN\n[[product1]];{{quantity1}}"},
        {"role": 'user',"content": 'Si'},
        {"role": 'assistant',"content": 'ORDEN_CONFIRMADA\nA'},
    ]
    try:
        response = co.chat(
            model='command-a-03-2025',
            messages= set_up_messages + [{"role": "user", "content": request}]
        )
        return response.message.content[0].text if response.message.content[0].text else 'No se pudo realizar el pedido, intente de nuevo en unos minutos'
    except Exception as e:
        print(f"Error: {e}")
        return 'Ocurrió un error procesando tu solicitud. Intenta de nuevo más tarde.'