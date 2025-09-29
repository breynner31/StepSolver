from app.services.solver_service import solve_step_by_step
from app.services.tts_service import generate_audio_from_steps

def solve_equation(data, socketio=None):
    equations = data.get("equations", [])
    variables = data.get("variables", [])
    initial_conditions = data.get("initial_conditions", {})

    # Enviar progreso inicial
    if socketio:
        socketio.emit('progress', {
            'step': 1,
            'total': 4,
            'message': 'Iniciando análisis de la ecuación...',
            'percentage': 25
        })

    # Obtener los pasos de solución
    steps = solve_step_by_step(equations, variables, initial_conditions, socketio)

    # Enviar progreso de generación de audio
    if socketio:
        socketio.emit('progress', {
            'step': 3,
            'total': 4,
            'message': 'Generando explicación de audio...',
            'percentage': 75
        })

    # Generar audio usando Gemini
    audio_path = generate_audio_from_steps(steps, socketio)

    # Enviar progreso final
    if socketio:
        socketio.emit('progress', {
            'step': 4,
            'total': 4,
            'message': 'Proceso completado exitosamente',
            'percentage': 100
        })

    return {
        "steps": steps,  # Mantenemos los pasos originales
        "audio_url": "/static/audio/results.mp3"
    }