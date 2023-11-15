import os
import re
from conversion import read_pdf, read_docx, read_txt, translate_text, text_to_audio
from flask import Flask, render_template, request, redirect, url_for, flash, send_file


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Especifica la ruta completa de la carpeta estática
app.static_folder = os.path.abspath("statics")

app.secret_key = 'your_secret_key'  # ¿deberia ponerle una clave?

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Procesa el archivo y genera el audio
        input_file = request.files["file"]
        if input_file and allowed_file(input_file.filename):
            try:
                filename = input_file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                input_file.save(file_path)

                # Llama a las funciones de conversión desde conversion.py 
                extension = filename.split('.')[-1].lower()
                if extension == 'pdf':
                    text = read_pdf(file_path)
                elif extension == 'docx':
                    text = read_docx(file_path)
                elif extension == 'txt':
                    text = read_txt(file_path)

                translated_text = translate_text(text, target_lang='es')
                text_with_pauses = re.sub(r'[,;:.\n]', r'\g<0> ', translated_text)
            
                base_name = os.path.splitext(filename)[0]
                output_file = f"{base_name}.mp3"  
                count = 1
                while os.path.exists(output_file):
                    output_file = f"{base_name}_{count}.mp3"
                    count += 1

                text_to_audio(text_with_pauses, output_file)
                
                # Devolver el archivo de audio 
                flash(f"Audio generado a partir de '{filename}' y guardado como '{output_file}'", 'success') if output_file else flash("Error al generar el audio", 'error')
                # Borra el archivo después de descargarlo
                os.remove(file_path)
                
                return send_file(output_file, as_attachment=True)
            except FileNotFoundError:
                flash("El archivo especificado no existe.", 'error')
            except Exception as e:
                 print(f"Ocurrió un error: {e}")
                 flash(f"Ocurrió un error: {e}", 'error')

            return redirect(url_for("index"))
        else:
            flash("Formato de archivo no permitido. Por favor, sube un archivo TXT, PDF o DOCX.", 'error')
            return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)