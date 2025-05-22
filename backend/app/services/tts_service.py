import os
from gtts import gTTS
from .gemini_service import generate_audio_explanation

def generate_audio_from_steps(steps, output_path='static/audio/results.mp3'):
    try:
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generar explicación usando Gemini
        explanation = generate_audio_explanation(steps)
        
        # Debug: Imprimir la explicación para ver qué está devolviendo Gemini
        print("Explicación generada por Gemini:", explanation)
        
        # Guardar la explicación en un archivo de texto para debug
        text_path = output_path.replace('.mp3', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(explanation)
        
        # Dividir la explicación en partes más pequeñas
        max_length = 4000  # Reducimos el límite para mayor seguridad
        parts = []
        current_part = ""
        
        # Dividir por oraciones para mantener la coherencia
        sentences = explanation.split('. ')
        for sentence in sentences:
            if len(current_part) + len(sentence) < max_length:
                current_part += sentence + '. '
            else:
                parts.append(current_part.strip())
                current_part = sentence + '. '
        
        if current_part:
            parts.append(current_part.strip())
        
        # Generar audio para cada parte
        audio_files = []
        for i, part in enumerate(parts):
            if not part.strip():  # Saltar partes vacías
                continue
                
            temp_path = f"{output_path}.part{i}.mp3"
            print(f"Generando audio para parte {i+1} de {len(parts)}")
            print(f"Longitud del texto: {len(part)} caracteres")
            
            tts = gTTS(text=part, lang='es', slow=False)
            tts.save(temp_path)
            audio_files.append(temp_path)
        
        # Si solo hay una parte, renombrarla al archivo final
        if len(audio_files) == 1:
            os.rename(audio_files[0], output_path)
        else:
            # Si hay múltiples partes, usar el primer archivo como base
            # y agregar el resto al final
            with open(output_path, 'wb') as outfile:
                for audio_file in audio_files:
                    with open(audio_file, 'rb') as infile:
                        outfile.write(infile.read())
            
            # Limpiar archivos temporales
            for temp_file in audio_files:
                os.remove(temp_file)
        
        print(f"Audio generado exitosamente en: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error al generar el audio: {str(e)}")
        return None