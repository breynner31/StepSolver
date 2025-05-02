from flask import Flask, request, jsonify
from app.controllers.solve_controller import solve_equation

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a StepSolver API v1.0"}), 200

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    print("DATA RECIBIDA:", data)
    response = solve_equation(data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)