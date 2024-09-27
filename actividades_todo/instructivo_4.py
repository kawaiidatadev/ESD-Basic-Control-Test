from common.__init__ import *
import fnmatch

# Ruta al directorio donde se buscarán los archivos PDF
pdf_directory = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\Instructivos'
av_code = '1194'

# Función principal para encontrar y abrir un PDF con "1180" en el nombre
def abrir_pdf4(max_attempts=3):
    # Función interna para mostrar un cuadro de mensaje
    def msgbox(message, title):
        ctypes.windll.user32.MessageBoxW(0, message, title, 1)

    # Buscar el primer archivo PDF que contenga "1180" en su nombre
    def encontrar_pdf(contenido=av_code):
        for root, dirs, files in os.walk(pdf_directory):
            for filename in fnmatch.filter(files, f"*{contenido}*.pdf"):
                return os.path.join(root, filename)
        return None

    # Función interna para intentar abrir el PDF con el visor predeterminado o Chrome
    def try_open_pdf(pdf_path, method):
        attempt = 0
        while attempt < max_attempts:
            try:
                if method == "default":
                    subprocess.Popen([pdf_path], shell=True)
                elif method == "chrome":
                    subprocess.Popen(["chrome", pdf_path])
                return True
            except Exception as e:
                attempt += 1
                time.sleep(2)  # Esperar 2 segundos antes de reintentar
        return False

    # Buscar el archivo PDF que contenga av_code
    pdf_encontrado = encontrar_pdf(av_code)

    if pdf_encontrado:
        # Intentar abrir primero con el visor predeterminado
        if not try_open_pdf(pdf_encontrado, "default"):
            # Si falla, intentar con Chrome
            if not try_open_pdf(pdf_encontrado, "chrome"):
                msgbox(f"No se pudo abrir el PDF '{pdf_encontrado}' después de varios intentos.", "Error al abrir PDF")
    else:
        # Mostrar un mensaje si no se encuentra el PDF
        msgbox(f"No se encontró ningún PDF que contenga {av_code} en su nombre.", "PDF no encontrado")
