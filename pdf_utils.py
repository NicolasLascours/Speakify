import PyPDF2
from reportlab.pdfgen import canvas
import io, re

def flatten_pdf(input_pdf, output_pdf):
    """
    Aplana un archivo PDF eliminando capas y contenido no deseado.

    Parameters:
    - input_pdf (str): Ruta del archivo PDF de entrada.
    - output_pdf (str): Ruta del archivo PDF de salida después de la operación de aplanado.

    Returns:
    - output_pdf (str): Ruta del archivo PDF de salida.

    Raises:
    - Exception: Si se produce un error durante la operación de aplanado del PDF.
    """
    try:        
        with open(input_pdf, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()

            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.getPage(page_number)
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=page.cropBox)
                can.showPage()
                can.save()
                packet.seek(0)
                new_pdf = PyPDF2.PdfReader(packet)
                page.mergePage(new_pdf.getPage(0))
                pdf_writer.addPage(page)

            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

            return output_pdf
    except Exception as flatten_error:
        print(f"Error flattening PDF: {flatten_error}")
        raise flatten_error


def remove_page_header(page_text):
    """
    Elimina el encabezado de una página de texto en formato PDF.

    Parameters:
    - page_text (str): Texto de la página que puede contener un encabezado.

    Returns:
    - page_text_without_header (str): Texto de la página después de eliminar el encabezado.

    Raises:
    - Exception: Si se produce un error durante la eliminación del encabezado de la página.
    """
    try:
        header_pattern = re.compile(r'^.*?\n', re.MULTILINE)
        match = re.search(header_pattern, page_text)

        if match:
            start, end = match.span()
            page_text_without_header = page_text[end:]
        else:
            page_text_without_header = page_text

        return page_text_without_header
    except Exception as remove_header_error:
        print(f"Error removing page header: {remove_header_error}")
        raise remove_header_error


