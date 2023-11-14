import pyttsx3
import PyPDF2
from docx import Document
import libretranslate


def read_pdf(pdf_file):
    with open(pdf_file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page_number in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_number)
            text += page.extractText()
        return text 

def read_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_txt(txt_file):
    with open(txt_file, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def translate_text(text, target_lang='es'):
    # Configura el servidor de LibreTranslate
    server_url = 'https://libretranslate.de'  # Puedes usar el servidor público de LibreTranslate o configurar el tuyo propio

    # Crea una instancia del cliente de LibreTranslate
    translator = libretranslate.(server_url=server_url)
    
    # Traduce el texto
    translation = translator.translate(text, target_lang)
    return translation


def text_to_audio(text, output_file):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)  # Velocidad de habla 
    engine.setProperty('volume', 1.0)  # Volumen de habla 
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\VoicesTokens\es-MX-GonzaloM')
    
    engine.save_to_file(text, output_file)
    engine.runAndWait()
