import pyttsx3
import PyPDF2, re
from nltk.tokenize import sent_tokenize
from langdetect import detect
from docx import Document
from deep_translator import GoogleTranslator


def clean_pdf_text(raw_text):
    # Elimina la numeración seguida de un espacio en los párrafos
    cleaned_text = re.sub(r'\b\d+\s', '', raw_text)
    # Corrige palabras mal divididas por eliminar caracteres no alfanuméricos
    cleaned_text = re.sub(r'(?<=\w)\s+(?=\w)', '', cleaned_text)
    
    return cleaned_text

def split_into_paragraphs(text):
    # Divide el texto en párrafos o frases coherentes
    paragraphs = text.split('\n')
    return paragraphs

def remove_page_header(page_text):
    # Busca el encabezado desde el inicio de la página hasta la primera línea nueva
    header_pattern = re.compile(r'^.*?\n', re.MULTILINE)
    
    # Encuentra la primera coincidencia del encabezado
    match = re.search(header_pattern, page_text)
    
    if match:
        # Elimina el encabezado encontrando su posición y eliminando hasta la primera línea nueva
        start, end = match.span()
        page_text_without_header = page_text[end:]
    else:
        # Si no se encuentra un encabezado, simplemente devuelve el texto original
        page_text_without_header = page_text
    
    return page_text_without_header

def read_pdf(pdf_file):
    try:
        with open(pdf_file, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            text = ""

            for page_number in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_number)
                page_text = page.extractText()

                # Elimina el encabezado de la página
                page_text_without_header = remove_page_header(page_text)

                # Limpieza de Texto
                clean_text = clean_pdf_text(page_text_without_header)

                # División en Párrafos o Frases
                paragraphs = split_into_paragraphs(clean_text)

                # Agrega los párrafos al texto final
                text += " ".join(paragraphs) + "\n"

            return text
    except Exception as pdf_error:
        print(f"Error reading PDF: {pdf_error}")
        raise pdf_error


def clean_docx_text(raw_text):
    cleaned_text = raw_text.replace('\t', ' ')  
    return cleaned_text

def read_docx(docx_file):
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            cleaned_paragraph = clean_docx_text(paragraph.text)
            text += cleaned_paragraph + "\n"
        return text
    except Exception as docx_error:
        print(f"Error reading DOCX: {docx_error}")
        raise docx_error

def clean_txt_text(raw_text):
    cleaned_text = raw_text.replace('\t', ' ')  # Reemplaza tabulaciones con espacios
    return cleaned_text

def read_txt(txt_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as file:
            raw_text = file.read()
            cleaned_text = clean_txt_text(raw_text)
        return cleaned_text
    except Exception as txt_error:
        print(f"Error reading TXT: {txt_error}")
        raise  
    

def translate_text(text, target_lang='es', chunk_size=5000):
    try:
        # Verifica si el texto ya está en español
        if detect(text) == 'es':
            return text

        translator = GoogleTranslator(source='auto', target=target_lang)

        # Divide el texto en oraciones usando nltk.sent_tokenize
        sentences = sent_tokenize(text)

        # Inicializa contenedores
        translations = []
        current_chunk = ''

        for sentence in sentences:
            # Verifica si agregar la oración actual superaría el límite de bytes
            if (len(sentence.encode('utf-8')) + len(current_chunk.encode('utf-8')) < chunk_size):
                current_chunk += ' ' + sentence
            else:
                # Traduce el fragmento actual y agrega a las traducciones
                translations.append(translator.translate(current_chunk))
                # Inicia un nuevo fragmento con la oración actual
                current_chunk = sentence

        # Traduce el último fragmento si hay texto restante
        if current_chunk:
            translations.append(translator.translate(current_chunk))

        # Une todas las traducciones en una sola cadena
        result = ' '.join(translations)

        return result.strip()  # Elimina posibles espacios en blanco al final
    except Exception as translate_error:
        print(f"Error translating text: {translate_error}")
        raise translate_error


def text_to_audio(text, output_file):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 1.0)
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\VoicesTokens\es-MX-GonzaloM')
        engine.save_to_file(text, output_file)
        engine.runAndWait()
    except Exception as audio_error:
        print(f"Error converting text to audio: {audio_error}")
        raise audio_error
