from common import *
from settings.conf_ventana import configurar_ventana
from settings.__init__ import *  # Importar los paths
from submains_asignaciones.registrar_bata import registrar_nueva_bata
from  submains_asignaciones.asignar_bata import asignar_bata

def batas_asignaciones(asignaciones_window, root):
    ventana_batas_esd = tk.Toplevel(root)  # Crear una nueva ventana hija de root
    # Configuracion de la ventana de Personal ESD
    configurar_ventana(ventana_batas_esd, "Asignaciones de Batas ESD")

    # Crear botones
    buttons = [
        ("Registrar Nueva Bata", lambda: registrar_nueva_bata(ventana_batas_esd, root)),
        ("Asignar una Bata", lambda: asignar_bata(ventana_batas_esd, root)),
        ("Desasignar una Bata", print('Bata3'))
    ]

    for text, command in buttons:
        btn = tk.Button(ventana_batas_esd, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2,
                        width=40)
        btn.pack(pady=10)


    # Función para salir del programa
    def salir_programa():
        ventana_batas_esd.destroy()  # Destruye el objeto
        asignaciones_window.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_batas_esd, text="Salir", command=salir_programa, font=("Arial", 14), bg="red",
                          fg="white",
                          height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ocultar la ventana principal al abrir la ventana de Personal ESD
    asignaciones_window.withdraw()  # Oculta la ventana principal

    # Ejecutar la ventana de Personal ESD
    ventana_batas_esd.protocol("WM_DELETE_WINDOW", salir_programa)  # Asegúrate de cerrar correctamente
    ventana_batas_esd.mainloop()