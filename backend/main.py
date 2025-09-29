from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from app.controllers.solve_controller import solve_equation
from app.config.config import config
import os

# Obtener configuración basada en el entorno
config_name = os.environ.get('FLASK_ENV', 'development')
app = Flask(__name__)
app.config.from_object(config[config_name])

# Configurar SocketIO con configuración dinámica
socketio = SocketIO(
    app, 
    cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'],
    transports=app.config.get('SOCKETIO_TRANSPORTS', ['polling'])
)

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a StepSolver API v1.0"}), 200

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    print("DATA RECIBIDA:", data)
    response = solve_equation(data, socketio)
    return jsonify(response)

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    emit('status', {'message': 'Conectado al servidor de progreso'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)