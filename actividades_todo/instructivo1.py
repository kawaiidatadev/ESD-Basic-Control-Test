from common.__init__ import *
# Ruta al archivo PDF
pdf_instructivo1 = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\Instructivos\N-A-GenK1180v0.pdf'

# Función principal que intenta abrir el PDF
def abrir_pdf(pdf_path=pdf_instructivo1, max_attempts=3):
    # Función interna para mostrar un cuadro de mensaje
    def msgbox(message, title):
        ctypes.windll.user32.MessageBoxW(0, message, title, 1)

    # Función interna para intentar abrir el PDF con el visor predeterminado o Chrome
    def try_open_pdf(method):
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

    # Intentar abrir primero con el visor predeterminado
    if not try_open_pdf("default"):
        # Si falla, intentar con Chrome
        if not try_open_pdf("chrome"):
            # Si todo falla, mostrar un mensaje de error
            msgbox("No se pudo abrir el PDF después de varios intentos.", "Error al abrir PDF")