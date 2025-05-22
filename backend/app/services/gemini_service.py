from google import generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno")
    genai.configure(api_key=api_key)

def get_cached_explanation(steps_hash):
    cache_file = 'explanations_cache.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            return cache.get(steps_hash)
    return None

def save_to_cache(steps_hash, explanation):
    cache_file = 'explanations_cache.json'
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    
    cache[steps_hash] = explanation
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def generate_audio_explanation(steps):
    init_gemini()
    
    try:
        # Usar el modelo gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt para dictado matemático general
        prompt = """
        Convierte estas ecuaciones matemáticas en un dictado claro y pausado en español.
        Lee cada símbolo de manera explícita y con pausas naturales.
        
        Reglas de dictado:
        - y(x) se lee como "y... abre paréntesis... x... cierra paréntesis"
        - C₁, C₂, etc. se lee como "C mayúscula... subíndice uno", "C mayúscula... subíndice dos"
        - e⁻ˣ se lee como "e... exponencial... menos x"
        - eˣ se lee como "e... exponencial... x"
        - + se lee como "más"
        - - se lee como "menos"
        - = se lee como "igual a"
        - x² se lee como "x... al cuadrado"
        - x³ se lee como "x... al cubo"
        - √x se lee como "raíz cuadrada... de x"
        - dy/dx se lee como "derivada de y... respecto a x"
        - d²y/dx² se lee como "segunda derivada de y... respecto a x"
        - d³y/dx³ se lee como "tercera derivada de y... respecto a x"
        
        Para raíces complejas:
        - CRootOf se lee como "raíz compleja número"
        - re se lee como "parte real de"
        - im se lee como "parte imaginaria de"
        
        IMPORTANTE:
        - Agrega pausas naturales entre cada término
        - Lee cada paso completo, sin omitir nada
        - Dicta cada símbolo matemático de manera clara y pausada
        - Si hay fracciones, dicta "numerador" y "denominador" claramente
        
        Pasos de la solución de la ecuación:
        """
        
        for step in steps:
            prompt += f"\n{step['title']}:\n{step['latex_description']}\n"
            if len(step['latex_description']) > 200:
                prompt += "Esta ecuación es muy larga. Proporciona una explicación simplificada de su estructura:\n"
            else:
                prompt += "Lee esta ecuación completa, término por término, con pausas naturales:\n"
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error al generar explicación: {str(e)}")
        # Si falla, generar una explicación simple
        simple_explanation = "Pasos de la solución de la ecuación:\n"
        for step in steps:
            simple_explanation += f"\n{step['title']}:\n{step['latex_description']}\n"
        return simple_explanation