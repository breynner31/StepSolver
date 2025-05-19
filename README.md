# 🧠 StepSolver – Solución Paso a Paso de EDOs

## 📌 Descripción

**StepSolver** es una plataforma web desarrollada con **React**(frontend) y **Python**(backend) que permite resolver **Ecuaciones Diferenciales Ordinarias (EDO)** de forma simbólica utilizando `SymPy`.  
Además de mostrar una solución paso a paso en formato LaTeX, genera una **lectura por voz** del procedimiento en español usando `gTTS` y ofrece modos de contraste para mejorar la accesibilidad visual.
![Normal](https://github.com/user-attachments/assets/39428700-baf6-45c6-b66b-b8c0f94d0451)

## 🚀 Características

✅ Interfaz de usuario intuitiva desarrollada en React
✅ Características de accesibilidad (modos de contraste y tooltips informativos)
✅ Interpreta ecuaciones diferenciales en notación simbólica
✅ Resuelve paso a paso con explicaciones detalladas
✅ Formatea los resultados con soporte LaTeX para uso académico
✅ Genera audio en español explicando cada paso
✅ API completa que devuelve JSON con título, descripción y expresiones en LaTeX
✅ Proporciona una ruta para escuchar la explicación en voz alta (/static/audio/results.mp3)

## 📦 Instalación

Antes de ejecutar el servidor, asegúrate de instalar las dependencias necesarias:

```bash
cd backend
pip install -r requirements.txt
```

Antes de ejecutar el frontend, asegúrate de instalar las dependencias necesarias:
```bash
cd frontend
npm install
```

## 🛠️ Uso

Inicia el servidor con:

```bash
cd backend
python main.py
```

Inicia el frontend con:
```bash
cd frontend
npm run start
```

**Uso de la API directamente**
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

## 🌈 Accesibilidad

-La plataforma incluye:
-Múltiples modos de contraste para mejorar la visibilidad
-Tooltips informativos que guían al usuario sobre cada elemento y función de la plataforma
-Audio descriptivo para explicaciones paso a paso

## 🌓 Modos de contraste

-**Amarillo sobre negro (Alto contraste):**
![Amarillo sobre negro (Alto contraste) ](https://github.com/user-attachments/assets/22107dcd-8c4c-422d-bce2-2f30cee499e6)

-**Azul oscuro sobre blanco:**
![Azul oscuro sobre blanco](https://github.com/user-attachments/assets/00535e10-a904-4d13-a57c-2e22fdb20171)

-**Rosa sobre gris oscuro:**
![Rosa sobre gris oscuro](https://github.com/user-attachments/assets/1db13710-371e-4924-9ff8-f89ce495d5b2)

-**Verde sobre negro:**
![Verde sobre negro](https://github.com/user-attachments/assets/b10b6cc8-bff0-48f5-a64b-63bd726f00ff)

## 📚 Dependencias

Backend (incluidas en requirements.txt):

```bash
Flask
sympy
gTTS
```

Instálalas con:

```bash
pip install -r requirements.txt
```

Frontend:

```bash
katex
react-katex
```

Instálalas con:

```bash
npm install
```

## 📁 Estructura del proyecto

```
📁 StepSolver/
    📄 README.md
    📁 backend/
        📁 app/
            📄 __init__.py
            📁 controllers/
                📄 solve_controller.py
            📁 services/
                📄 solver_service.py
                📄 tts_service.py
        📁 assets/
            📄 image.png
        📄 main.py
        📁 static/
            📁 audio/
                📄 results.mp3
    📁 frontend/
        📄 README.md
        📄 package.json
        📁 public/
            📄 favicon.ico
            📄 index.html
            📄 logo192.png
            📄 logo512.png
            📄 manifest.json
            📄 robots.txt
        📁 src/
            📄 App.css
            📄 App.js
            📁 components/
                📄 AudioPlayer.js
                📄 SolverForm.js
                📄 StepsDisplay.js
                📄 Tooltip.js
            📄 index.css
            📄 index.js
    📄 requirements.txt
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
✅ Diferencias clave con versiones anteriores:
- Plataforma completa con frontend en React y backend en Python
- Características de accesibilidad avanzadas (modos de contraste y tooltips informativos)
- Interfaz de usuario intuitiva para interactuar con las ecuaciones
- Resolución simbólica de EDOs con SymPy
- Generación automática de audio explicativo en español
- API clara, estructurada y lista para integrarse en otros proyectos
- Soporte para LaTeX, accesibilidad y herramientas educativas
- Documentación detallada y visual

Si quieres, dime qué más podríamos mejorar o personalizar. 🚀😃
```

---
