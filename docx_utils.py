from docx import Document

def clean_docx_text(raw_text):
    """
    Limpia el texto extraído de un documento DOCX eliminando tabulaciones.

    Parameters:
    - raw_text (str): Texto sin procesar extraído de un documento DOCX.

    Returns:
    - cleaned_text (str): Texto procesado sin tabulaciones.

    Raises:
    - Exception: Si se produce un error durante la limpieza del texto DOCX.
    """
    try:
        cleaned_text = raw_text.replace('\t', ' ')
        return cleaned_text
    except Exception as clean_docx_error:
        print(f"Error cleaning DOCX text: {clean_docx_error}")
        raise clean_docx_error


def read_docx(docx_file):
    """
    Lee el contenido de un archivo DOCX y devuelve el texto limpio.

    Parameters:
    - docx_file (str): Ruta del archivo DOCX.

    Returns:
    - text (str): Texto contenido en el archivo DOCX después de la limpieza.

    Raises:
    - Exception: Si se produce un error durante la lectura del archivo DOCX.
    """
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
