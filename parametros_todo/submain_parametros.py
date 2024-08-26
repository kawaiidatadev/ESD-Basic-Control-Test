from common import *
from settings.conf_ventana import configurar_ventana
from parametros_todo.registro_parametros import registrar_parametro

# Función para abrir la ventana de parámetros
def parametros_medicion(root):
    ventana_parametros = tk.Toplevel()  # Crear una nueva ventana

    # Configuracion de la ventana de parámetros
    configurar_ventana(ventana_parametros, "Parámetros de Medición")

    # Crear botones
    buttons = [
        ("Registrar", lambda: registrar_parametro(ventana_parametros)),
        ("Editar", print('Editar')),
        ("Consultar", print('Consultar')),
        ("Eliminar", print('Eliminar'))
    ]

    for text, command in buttons:
        btn = tk.Button(ventana_parametros, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2, width=40)
        btn.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        ventana_parametros.quit()  # Cierra la ventana de parámetros
        ventana_parametros.destroy()  # Destruye el objeto
        root.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_parametros, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ocultar la ventana principal al abrir la ventana de parámetros
    root.withdraw()  # Oculta la ventana principal

    # Ejecutar la ventana parámetros
    ventana_parametros.protocol("WM_DELETE_WINDOW", salir_programa)  # Asegúrate de cerrar correctamente
    ventana_parametros.mainloop()
