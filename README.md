# 🍣 Chatbot de Pedidos de Sushi con IA
Este proyecto es un chatbot conversacional diseñado para facilitar el proceso de pedidos de sushi, desde la bienvenida hasta la confirmación de la orden. Está compuesto por un Backend desarrollado en Python con Flask, que maneja la lógica de negocio y la interacción con la inteligencia artificial, y un Frontend en React, que proporciona la interfaz de usuario para chatear con el bot.

## ✨ Características Principales
Interacción Conversacional: Guía al usuario a través del proceso de pedido de forma natural.
Gestión de Dirección: Captura y confirma la dirección de entrega del cliente.
Gestión de Órdenes: Permite al usuario seleccionar productos y cantidades del menú, así como añadir, eliminar o modificar ítems del pedido.
Confirmación/Cancelación de Pedidos: Proceso claro para confirmar o cancelar una orden.
Persistencia de Pedidos: Almacena los pedidos confirmados y cancelados en una base de datos.
Integración con IA (Cohere): Utiliza un modelo de lenguaje avanzado para interpretar las intenciones del usuario y generar respuestas coherentes.

## 💻 Tecnologías Utilizadas
Backend (Python/Flask)
- Python - Flask - Flask-CORS - python-dotenv - Cohere API - MongoEngine(ORM) - MongoDB
  
Frontend (Node.js/React)
- Node.js - React - Zustand - npm

## Utilización:
El proyecto está deployado en: https://chat-bot-ia-sushi-frontend.vercel.app/
- Puedes preguntarle preguntas frecuentes y que te enseñe el menu (Todavía no hay implementado un menú para verlo de mejor manera, pero al menos con eso podrás realizar tu pedido!)
- Podras pedirle realizar un pedido, siguiendo los pasos que te pide
- Podrás confirmar o cancelar el pedido y seguir en la conversación
  
## 🚀 Instalación y Uso Local
Este proyecto requiere que tanto el backend como el frontend estén funcionando para una experiencia completa. Sigue los pasos a continuación para configurarlo en tu máquina local.

### ⚙️ Requisitos Previos
Asegúrate de tener instalados los siguientes programas en tu sistema:

- Python 3.9+ (se recomienda la versión LTS)
- pip (gestor de paquetes de Python, suele venir con Python)
- Node.js LTS (se recomienda la versión 18 o superior)
- npm (gestor de paquetes de Node.js, suele venir con Node.js)
- Git (para clonar el repositorio)
- MongoDB: Puedes instalarlo localmente o usar un servicio en la nube como MongoDB Atlas (recomendado para facilidad).
- API Key de [Cohere](https://docs.cohere.com/v2/docs/rate-limits).  

### 🔑 Configuración de Variables de Entorno
El backend utiliza la API de Cohere y se conecta a MongoDB. Necesitarás configurar estas credenciales.

1. Crea un archivo `.env`: En la raíz de la carpeta `backend/`, crea un archivo llamado `.env`.
2. Añade tus variables: Dentro del archivo `.env`, agrega las siguientes líneas, reemplazando `TU_API_KEY_AQUI` y `TU_MONGO_URL_AQUI` con tus valores reales:
```
API_KEY="TU_API_KEY_AQUI"
MONGO_URL="TU_MONGO_URL_AQUI" # Ejemplo: mongodb://127.0.0.1:27017/MongoDB1
```

### 📦 Configuración del Backend
1. Clona el repositorio:
```
git clone https://github.com/Nachit0C/chat_bot_IA_sushi.git
cd chat_bot_IA_sushi
```
2. Accede a la carpeta del Backend:
```
cd backend/
```
3. Crea y activa un entorno virtual (muy recomendado):
```
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```
4. Instala las dependencias de Python:
```
pip install -r requirements.txt
```
Ejecuta el Backend:
```
py main.py
```
El backend debería iniciarse y ser accesible en http://127.0.0.1:5000 (o el puerto configurado en tu .env si lo cambiaste). Deberías ver un mensaje en la consola indicando que Flask está corriendo.
### 🖥️ Configuración del Frontend
1. Abre una nueva terminal (mantén el backend ejecutándose en la anterior).
2. Accede a la carpeta del Frontend:
```
cd frontend/
```
Instala las dependencias de Node.js:
```
npm install
```
Ejecuta el Frontend:
```
npm run dev
```
El frontend debería abrirse automáticamente en tu navegador predeterminado en http://localhost:3000.
## 💬 Uso del Chatbot
Una vez que tanto el Backend como el Frontend estén ejecutándose (en sus respectivas terminales), puedes abrir tu navegador y navegar a `http://localhost:3000`

Comienza a interactuar con el chatbot escribiendo mensajes en el campo de texto. El chatbot te guiará a través del proceso de bienvenida, solicitud de dirección y toma de pedidos, permitiéndote agregar, modificar o cancelar productos.

## Próximos objetivos:
- Ampliar la base de datos para control de stock
- Ampliar el backend para la gestion de stock de la base de datos
- Implementación visual de un menu para ofrecerle al usuario
- Mejora de la IA para mayor cantidad de interacciones y respuestas a preguntas frecuentes
- Ampliar el proyecto para ser utilizado por multiples usuarios en paralelo
