# 🧠 StepSolver – Solución Paso a Paso de EDOs

## 📌 Descripción

**StepSolver** es una API desarrollada con **Flask** en Python que permite resolver **Ecuaciones Diferenciales Ordinarias (EDO)** de forma simbólica utilizando `SymPy`.  
Además de mostrar una solución paso a paso en formato LaTeX, genera una **lectura por voz** del procedimiento en español usando `gTTS`.

## 🚀 Características

✅ Interpreta ecuaciones diferenciales en notación simbólica.  
✅ Resuelve paso a paso con explicaciones.  
✅ Formatea los resultados con soporte LaTeX para uso académico.  
✅ Genera audio en español explicando cada paso.  
✅ Devuelve un JSON completo con título, descripción y expresiones en LaTeX.  
✅ Proporciona una ruta para escuchar la explicación en voz alta (`/static/audio/results.mp3`).

## 📦 Instalación

Antes de ejecutar la API, asegúrate de instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## 🛠️ Uso

Inicia el servidor con:

```bash
python main.py
```

Envía una solicitud POST al endpoint:

```bash
http://127.0.0.1:5000/api/solve
```

🔸 Estructura del JSON de entrada
```bash
{
  "equations": ["dy/dx + y = x"],
  "variables": ["x", "y"],
  "initial_conditions": {
    "x0": 0,
    "y0": -1
  }
}
```

📥 Respuesta del endpoint
```bash
{
  "steps": [
    {
      "title": "Interpretación de la ecuación",
      "description": "Se reescribe como: y(x) + Derivative(y(x), x) = x",
      "latex": "y(x) + \\frac{dy}{dx} = x"
    },
    {
      "title": "Solución general",
      "description": "La solución general de la ecuación es:",
      "latex": "y(x) = C_1 e^{-x} + x - 1"
    },
    {
      "title": "Aplicando condiciones iniciales",
      "description": "Se usa la condición y(0) = -1 para encontrar C1",
      "latex": ""
    },
    {
      "title": "Solución particular",
      "description": "La solución particular es:",
      "latex": "y(x) = x - 1"
    }
  ],
  "audio_url": "/static/audio/results.mp3"
}
```

🔉 Lectura por voz

El sistema genera un archivo .mp3 con la lectura de los pasos (título + descripción).
Puedes acceder al audio generado en:

```bash
/static/audio/results.mp3
```

## 📚 Dependencias

Incluidas en requirements.txt:

```bash
Flask
sympy
gTTS
```

Instálalas con:

```bash
pip install -r requirements.txt
```

## 📁 Estructura del proyecto

```
StepSolver/
│
├── app/
│   ├── controllers/
│   │   └── solve_controller.py
│   │
│   ├── services/
│   │   ├── solver_service.py
│   │   └── tts_service.py
│   │
│   ├── main.py
│
├── static/
│   └── audio/
│       └── results.mp3
│
├── requirements.txt
└── README.md
```

## 🤝 Contribuciones

Si quieres mejorar este proyecto:

Haz un fork del repositorio.
Crea una rama con tu mejora:

```bash
git checkout -b mi-mejora
```

Sube los cambios y abre un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT, lo que significa que puedes usarlo y modificarlo libremente.

---

```bash
✅ Diferencias clave con tu versión:
✅ Diferencias clave con tu versión:
- Resolución simbólica de EDOs con SymPy.
- Generación automática de audio explicativo en español.
- API clara, estructurada y lista para integrarse en otros proyectos.
- Soporte para LaTeX, accesibilidad y herramientas educativas.
- Documentación detallada y visual.

Si quieres, dime qué más podríamos mejorar o personalizar. 🚀😃
```

---
