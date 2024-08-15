from common import *
from settings.conf_ventana import configurar_ventana
from submains_level_2.registrar_usuario import *
from submains_level_2.editar_usuario import *
from submains_level_2.consulta_usuarios_db import *
from submains_level_2.eliminar_usuario import *

# Función para abrir la ventana de Personal ESD
def personal_esd(root):
    ventana_personal_esd = tk.Toplevel(root)  # Crear una nueva ventana hija de root

    # Configuracion de la ventana de Personal ESD
    configurar_ventana(ventana_personal_esd, "Personal ESD")

    # Crear botones
    buttons = [
        ("Registrar", lambda: registrar_usuario(root, ventana_personal_esd)),
        ("Editar", lambda: editar_usuario(root, ventana_personal_esd)),
        ("Consultar", lambda: consultar_usuario(root, ventana_personal_esd)),
        ("Eliminar", lambda: eliminar_usuario(root))
    ]

    for text, command in buttons:
        btn = tk.Button(ventana_personal_esd, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2, width=40)
        btn.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        ventana_personal_esd.quit()  # Cierra la ventana de Personal ESD
        ventana_personal_esd.destroy()  # Destruye el objeto
        root.deiconify()  # Muestra nuevamente la ventana principal

    # Crear el botón "Salir"
    btn_salir = tk.Button(ventana_personal_esd, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white",
                          height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ocultar la ventana principal al abrir la ventana de Personal ESD
    root.withdraw()  # Oculta la ventana principal

    # Ejecutar la ventana de Personal ESD
    ventana_personal_esd.protocol("WM_DELETE_WINDOW", salir_programa)  # Asegúrate de cerrar correctamente
    ventana_personal_esd.mainloop()