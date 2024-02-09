from flask import Flask, render_template, request, flash, send_file
from utils import clean_downloads_folder, allowed_file
from convertion import translate_and_convert_to_audio
import os

app = Flask(__name__)
PORT = 5000
DEBUG = False
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB
downloads_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

@app.route("/", methods=["GET", "POST"])
def index():
    output_file = None

    if request.method == "POST":
        input_file = request.files["file"]
        if input_file and allowed_file(input_file.filename):
            try:
                filename = input_file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                input_file.save(file_path)

                output_file = translate_and_convert_to_audio(file_path, downloads_directory)

                flash("Conversión exitosa.", 'success')

                os.remove(file_path)

                return send_file(os.path.join(downloads_directory, output_file), as_attachment=True)
                
            except FileNotFoundError:
                flash("El archivo especificado no existe.", 'error')
            except ValueError:
                flash("Error al procesar el archivo. Asegúrate de que sea un archivo TXT, PDF o DOCX válido.", 'error')
            except Exception as e:
                flash("Ocurrió un error inesperado. Por favor, intenta nuevamente.", 'error')
                print(f"Ocurrió un error: {e}")

    clean_downloads_folder(downloads_directory)

    return render_template("index.html", output_file=output_file)

if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
