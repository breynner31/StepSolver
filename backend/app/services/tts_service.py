from gtts import gTTS
import os

def generate_audio_from_steps(steps, output_path='static/audio/results.mp3'):
    full_text = ""
    for step in steps:
        title = step.get("title", "")
        description = step.get("description", "")
        full_text += f"{title}: {description}. "

    tts = gTTS(text=full_text, lang='es')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    tts.save(output_path)

    return output_path