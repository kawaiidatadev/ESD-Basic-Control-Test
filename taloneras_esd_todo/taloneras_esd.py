from common import *
from settings.conf_ventana import configurar_ventana
from taloneras_esd_todo.registrar_talonera import registrar_talonera
from taloneras_esd_todo.asignar_talonera import asignaciones_taloneras


def taloneras_asignaciones(asignaciones_window, root):
    print("Hola mundo")
    taloneras_asignaciones = tk.Toplevel(root)
    asignaciones_window.withdraw()
    configurar_ventana(taloneras_asignaciones, "Asignación de taloneras ESD")

    # Función para salir del programa
    def salir_programa():
        taloneras_asignaciones.destroy()
        asignaciones_window.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(taloneras_asignaciones, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white", height=2, width=15)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Función para registrar nueva talonera
    def registrar_talonera_esd():
        registrar_talonera(taloneras_asignaciones, root)

    # Actualiza el botón en `taloneras_esd.py`
    btn_registrar = tk.Button(taloneras_asignaciones, text="Registrar Nueva Talonera", command=registrar_talonera_esd,
                              font=("Arial", 12), bg="green", fg="white", height=2, width=20)

    # Función para asignar talonera
    # Función para asignar talonera
    def asignar_talonera():
        asignaciones_taloneras(taloneras_asignaciones, root)

    # Función para desasignar talonera
    def desasignar_talonera():
        print("Desasignar talonera")
        # Aquí puedes agregar la lógica para desasignar una talonera


    btn_asignar = tk.Button(taloneras_asignaciones, text="Asignar Talonera", command=asignar_talonera,
                           font=("Arial", 12), bg="blue", fg="white", height=2, width=20)
    btn_desasignar = tk.Button(taloneras_asignaciones, text="Desasignar Talonera", command=desasignar_talonera,
                              font=("Arial", 12), bg="orange", fg="white", height=2, width=20)

    # Colocar los botones en la ventana
    btn_registrar.pack(pady=10)  # Espacio entre botones
    btn_asignar.pack(pady=10)
    btn_desasignar.pack(pady=10)
