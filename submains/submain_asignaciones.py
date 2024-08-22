from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths y funciones necesarios
from batas_esd_todo.batas import *
from pulseras_esd_todo.pulseras_esd import pulseras_asignaciones
from taloneras_esd_todo.taloneras_esd import taloneras_asignaciones
from evidencias_asignacion_todo.ventana_de_evidencias import evidencias_asignacion

def control_asignaciones(root):
    asignaciones_window = tk.Toplevel()  # Crear una nueva ventana
    root.withdraw() # oculta ventana menu
    configurar_ventana(asignaciones_window, "Control de Asignaciones")

    # Crear botones para "Batas ESD", "Pulseras ESD", "Taloneras ESD", y "Evidencias de Asignación"
    buttons = [
        ("Batas ESD", lambda: batas_asignaciones(asignaciones_window, root)),
        ("Pulseras ESD", lambda: pulseras_asignaciones(asignaciones_window, root)),
        ("Taloneras ESD", lambda: taloneras_asignaciones(asignaciones_window, root)),
        ("Evidencias de Asignación", lambda: evidencias_asignacion(asignaciones_window, root))
    ]

    for text, command in buttons:
        btn = tk.Button(asignaciones_window, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2, width=40)
        btn.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        asignaciones_window.destroy()  # Destruye el objeto
        root.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el botón "Salir"
    btn_salir = tk.Button(asignaciones_window, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

