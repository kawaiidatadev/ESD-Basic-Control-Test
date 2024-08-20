import tkinter as tk
from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths
from strings_consultas_db import registrar_nueva_bata_esd
from submains_asignaciones.usuario_a_asignar import mostrar_usuarios_disponibles
from strings_consultas_db import obtener_tamanos_unicos, obtener_tipos_unicos


def pulseras_asignaciones(asignaciones_window, root):
    pulseras_asignaciones = tk.Toplevel(root)
    asignaciones_window.withdraw()
    configurar_ventana(pulseras_asignaciones, "Asignación de pulseras ESD")

    # Función para salir del programa
    def salir_programa():
        pulseras_asignaciones.destroy()
        asignaciones_window.deiconify()

    # Crear el botón "Salir"
    btn_salir = tk.Button(pulseras_asignaciones, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white",
                          height=2, width=15)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Crear el botón "Registrar Nueva Pulsera"
    btn_registrar_pulsera = tk.Button(pulseras_asignaciones, text="Registrar Nueva Pulsera",
                                      command=registrar_nueva_bata_esd,
                                      font=("Arial", 14), bg="blue", fg="white", height=2, width=20)
    btn_registrar_pulsera.place(relx=0.5, rely=0.3, anchor='center')

    # Crear el botón "Asignar una Pulsera"
    btn_asignar_pulsera = tk.Button(pulseras_asignaciones, text="Asignar una Pulsera",
                                    command=mostrar_usuarios_disponibles,
                                    font=("Arial", 14), bg="green", fg="white", height=2, width=20)
    btn_asignar_pulsera.place(relx=0.5, rely=0.5, anchor='center')

    # Crear el botón "Desasignar una Pulsera"
    btn_desasignar_pulsera = tk.Button(pulseras_asignaciones, text="Desasignar una Pulsera",
                                       command=lambda: print("Desasignar Pulsera"),
                                       font=("Arial", 14), bg="orange", fg="white", height=2, width=20)
    btn_desasignar_pulsera.place(relx=0.5, rely=0.7, anchor='center')
