import PyPDF4
from reportlab.pdfgen import canvas
import io, re, logging, os

import PyPDF4
from reportlab.pdfgen import canvas
import io, os

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
            pdf_reader = PyPDF4.PdfFileReader(file)
            pdf_writer = PyPDF4.PdfFileWriter()

            for page_number in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_number)
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=page.cropBox)
                can.showPage()
                can.save()
                packet.seek(0)
                new_pdf = PyPDF4.PdfFileReader(packet)
                page.mergePage(new_pdf.getPage(0))
                pdf_writer.addPage(page)

            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

            return output_pdf
    except Exception as flatten_error:
        print(f"Error flattening PDF: {flatten_error}")
        raise flatten_error


def remove_page_header(page_text):
    try:
        # Lista de patrones de expresiones regulares para identificar encabezados
        header_patterns = [r'^.*?\n', r'^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}.*?\n']

        # Encuentra el índice del primer patrón que coincide
        matches = [re.search(re.compile(pattern, re.MULTILINE), page_text) for pattern in header_patterns]
        matches = [match for match in matches if match is not None]

        if not matches:
            return page_text

        start_index = min(match.end() for match in matches)
        page_text = page_text[start_index:]

        return page_text
    except Exception as remove_header_error:
        print(f"Error removing page header: {remove_header_error}")
        raise remove_header_error

def clean_pdf_text(raw_text):
    try:
        cleaned_text = re.sub(r'\b\d+\s', '', raw_text)
        cleaned_text = re.sub(r'(?<=\w)\s+(?=\w)', '', cleaned_text)
        return cleaned_text
    except Exception as clean_pdf_error:
        print(f"Error cleaning PDF text: {clean_pdf_error}")
        raise clean_pdf_error

def split_into_paragraphs(text):
    try:
        paragraphs = text.split('\n')
        return paragraphs
    except Exception as split_error:
        print(f"Error splitting text into paragraphs: {split_error}")
        raise split_error

def identify_sections(paragraphs):
    try:
        section_indices = {}
        for i, paragraph in enumerate(paragraphs):
            if re.search(r'\b(?:Abstract|Resumen)\b', paragraph):
                section_indices['abstract'] = i
            elif re.search(r'\bBibliografía\b', paragraph):
                section_indices['bibliography'] = i
        return section_indices
    except Exception as identify_sections_error:
        print(f"Error identifying sections: {identify_sections_error}")
        raise identify_sections_error

def read_pdf(pdf_file):
    try:
        flattened_pdf = flatten_pdf(pdf_file, "flattened_output.pdf")  # Flatten the PDF before processing

        with open(flattened_pdf, "rb") as flattened_file:
            pdf_reader = PyPDF4.PdfFileReader(flattened_file)
            text = ""

            for page_number in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_number)
                page_text = page.extractText()

                if not page_text.strip():
                    logging.warning(f"Empty text on page {page_number + 1}")
                    continue

                # Remove the header of the page
                page_text_without_header = remove_page_header(page_text)

                # Text cleaning
                clean_text = clean_pdf_text(page_text_without_header)

                # Split into paragraphs or sentences
                paragraphs = split_into_paragraphs(clean_text)

                # Identify sections
                section_indices = identify_sections(paragraphs)

                # Process sections
                if 'abstract' in section_indices:
                    abstract_start = section_indices['abstract']
                    abstract = " ".join(paragraphs[abstract_start:])
                    text += abstract + "\n"

                # Skip the Bibliography section
                if 'bibliography' in section_indices:
                    continue

                # Add paragraphs to the final text (excluding the Bibliography section)
                text += " ".join(paragraphs[:section_indices.get('bibliography', len(paragraphs))]) + "\n"

            return text
    except Exception as pdf_error:
        logging.error(f"Error reading PDF: {pdf_error}")
        raise pdf_error
    finally:
        # Eliminar el archivo flatten después de usarlo
        try:
            os.remove("flattened_output.pdf")
        except OSError as e:
            logging.warning(f"No se pudo eliminar el archivo flatten: {e}")