import os
import pyttsx3
from pdf_utils import read_pdf
from docx_utils import read_docx
from text_utils import read_txt, detect_language, split_text_into_sentences, translate_sentence

def translate_text(text, target_lang='es', chunk_size=4999):
    try:
        # Verificar si el texto no está vacío después de eliminar espacios en blanco
        if not text.strip():
            return text  # Devolver el texto original si está vacío

        source_lang = detect_language(text)

        if source_lang == target_lang:
            return text  # El texto ya está en el idioma deseado

        sentences = split_text_into_sentences(text)
        translations = []
        current_chunk = ''

        for sentence in sentences:
            if (len(sentence.encode('utf-8')) + len(current_chunk.encode('utf-8')) < chunk_size):
                current_chunk += ' ' + sentence
            else:
                translations.append(translate_sentence(current_chunk, target_lang))
                current_chunk = sentence

        if current_chunk:
            translations.append(translate_sentence(current_chunk, target_lang))

        result = ' '.join(translations)
        return result.strip()

    except Exception as translate_text_error:
        print(f"Error translating text: {translate_text_error}")
        raise translate_text_error

def text_to_audio(text, output_file):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 1.0)
        # Comprueba si la voz está disponible antes de establecerla
        available_voices = engine.getProperty('voices')
        if available_voices:
            engine.setProperty('voice', available_voices[0].id)  # Usar la primera voz disponible
            engine.save_to_file(text, output_file)
            engine.runAndWait()
        else:
            print("No se encontraron voces disponibles.")
    except Exception as audio_error:
        print(f"Error converting text to audio: {audio_error}")
        raise audio_error

def process_file(file_path):
    """
    Procesa el archivo según su extensión y devuelve el texto.
    """
    try:
        extension = os.path.splitext(file_path)[-1].lower()

        if extension == '.pdf':
            return read_pdf(file_path)
        elif extension == '.docx':
            return read_docx(file_path)
        elif extension == '.txt':
            return read_txt(file_path)
        else:
            raise ValueError(f"Formato de archivo no compatible: {extension}")
    except Exception as process_file_error:
        print(f"Error processing file: {process_file_error}")
        raise process_file_error