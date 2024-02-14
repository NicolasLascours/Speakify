import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_downloads_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Archivo eliminado correctamente: {file_path}")
            except PermissionError as pe:
                print(f"No se pudo eliminar {file_path}: Permiso denegado - {pe}")
            except FileNotFoundError as fnfe:
                print(f"No se pudo encontrar el archivo {file_path} - {fnfe}")
    except Exception as e:
        print(f"Ocurrió un error al limpiar la carpeta de descargas: {e}")