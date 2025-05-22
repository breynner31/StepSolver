from google import generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    print("Modelos disponibles:")
    for model in genai.list_models():
        print(f"- {model.name}")
        print(f"  Métodos soportados: {model.supported_generation_methods}")

if __name__ == "__main__":
    list_available_models() 