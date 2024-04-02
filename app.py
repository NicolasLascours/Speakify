from flask import Flask, render_template, request, flash, send_file, redirect, url_for, session
from utils import clean_downloads_folder, allowed_file
from convertion import translate_and_convert_to_audio
import os

app = Flask(__name__)
PORT = 8000
DEBUG = True
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB
downloads_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

if not os.path.exists(downloads_directory):
    os.makedirs(downloads_directory)

@app.route("/", methods=["GET", "POST"])
def index():
    output_file = None
    error_message = None

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
                error_message = "El archivo especificado no existe."
            except ValueError:
                error_message = "Error al procesar el archivo. Asegúrate de que sea un archivo TXT, PDF o DOCX válido."
            except Exception as e:
                error_message = "Ocurrió un error inesperado. Por favor, intenta nuevamente."
                print(f"Ocurrió un error: {e}")
                
            # Si ocurre un error, establecer el mensaje de error en la sesión
            session['error_message'] = error_message

            # Redirigir a la misma página para evitar que se reenvíe el formulario
            return redirect(url_for('index'))

    # Limpiar los mensajes de error de la sesión
    session.pop('error_message', None)

    clean_downloads_folder(downloads_directory)

    # Obtener el mensaje de error de la sesión
    error_message = session.get('error_message')

    return render_template("index.html", output_file=output_file, error_message=error_message)

if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
