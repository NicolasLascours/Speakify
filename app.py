import os
import re
import time
from conversion import translate_text, text_to_audio, process_file
from flask import Flask, render_template, request, flash, send_file, redirect, url_for, after_this_request

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB

# Directorios
current_directory = os.path.dirname(os.path.abspath(__file__))
downloads_directory = os.path.join(current_directory, 'downloads')

# Configuración de la carpeta estática y la clave secreta
app.static_folder = os.path.abspath("static")
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

                text = process_file(file_path)
                translated_text = translate_text(text, target_lang='es')
                text_with_pauses = re.sub(r'[,;:.\n]', r'\g<0> ', translated_text)

                base_name = os.path.splitext(filename)[0]
                output_file = f"{base_name}.mp3"
                count = 0

                while os.path.exists(output_file):
                    output_file = f"{base_name}_{count}.mp3"
                    count += 1

                text_to_audio(text_with_pauses, output_file)

                # Mueve el archivo a la carpeta downloads 
                download_path = os.path.join(downloads_directory, output_file)
                os.rename(output_file, download_path)
               
                # Mensaje Flash 
                flash("Conversión exitosa.", 'success')
                os.remove(file_path)
                # Redirect to index 
                #return redirect(url_for('index'))

            except FileNotFoundError:
                flash("El archivo especificado no existe.", 'error')
            except ValueError:
                flash("Error al procesar el archivo. Asegúrate de que sea un archivo TXT, PDF o DOCX válido.", 'error')
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                flash("Ocurrió un error inesperado. Por favor, intenta nuevamente.", 'error')

    if output_file:
        return redirect(url_for('download_file', filename=output_file))
    else:
        return render_template("index.html", output_file=output_file)

@app.route("/downloads/<filename>", methods=["GET"])
def download_file(filename):
    try:
        if filename is None:
            raise Exception("Nombre de archivo no válido")

        download_path = os.path.join(downloads_directory, filename)

        if os.path.exists(download_path):
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(download_path)
                except Exception as error:
                    print(f"Error al eliminar el archivo descargado: {error}")
                return response

            return send_file(download_path, as_attachment=True)
        else:
            raise Exception("El archivo no existe en la carpeta de descargas.")

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return "Error al descargar el archivo", 500

if __name__ == "__main__":
    app.run(debug=True)