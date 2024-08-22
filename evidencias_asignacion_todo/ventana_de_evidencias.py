from common.__init__ import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import db_path

def evidencias_asignacion(asignaciones_window, root):
        ventana_evidencias = tk.Toplevel(asignaciones_window)
        asignaciones_window.withdraw()
        configurar_ventana(ventana_evidencias, "Evidencias de asignaciones")

        # Función para salir de la ventana de asignación
        def salir_evidencias():
            ventana_evidencias.destroy()
            asignaciones_window.deiconify()

        # Crear el botón "Salir"
        btn_salir = tk.Button(ventana_evidencias, text="Salir", command=salir_evidencias, font=("Arial", 14), bg="red",
                              fg="white", height=2, width=15)
        btn_salir.pack(pady=10)