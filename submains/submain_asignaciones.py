from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths y funciones necesarios
from submains_asignaciones.batas import *

def control_asignaciones(root):
    asignaciones_window = tk.Toplevel()  # Crear una nueva ventana
    root.withdraw() # oculta ventana menu
    configurar_ventana(asignaciones_window, "Control de Asignaciones")

    # Crear botones para "Batas ESD", "Pulseras ESD", "Taloneras ESD", y "Evidencias de Asignación"
    buttons = [
        ("Batas ESD", lambda: batas_asignaciones(asignaciones_window, root)),
        ("Pulseras ESD", manejar_pulseras_esd),
        ("Taloneras ESD", manejar_taloneras_esd),
        ("Evidencias de Asignación", manejar_evidencias_asignacion)
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


def manejar_pulseras_esd():
    messagebox.showinfo("Pulseras ESD", "Funcionalidad para gestionar Pulseras ESD aún no implementada.")

def manejar_taloneras_esd():
    messagebox.showinfo("Taloneras ESD", "Funcionalidad para gestionar Taloneras ESD aún no implementada.")

def manejar_evidencias_asignacion():
    messagebox.showinfo("Evidencias de Asignación", "Funcionalidad para gestionar Evidencias de Asignación aún no implementada.")



