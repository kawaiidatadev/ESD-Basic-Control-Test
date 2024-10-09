from common.__init__ import *
from db_exist import verify_db  # Importa la función para crear la base de datos si no existe.
from parametros_todo.submain_parametros import *  # Importa la funcion del submenu de primer nivel de parametros
from submains.submain_personal_esd import *  # Importa la funcion del submenu de primer nivel de personal esd
from submains.submain_asignaciones import *
from actividades_todo.sub_ventana1 import ven1
from reporte_grande.reporte_central_anual import reporte_grande

# Variable global de la versión del programa
VERSION = "Sofware ESD Basic ß version: 1.0.0 \n" \
          "Linkedin: Luis Manuel Macias Patiño ¦ " \
          "Github: kawaiidatadev"

def main():
    # Verificamos la base de datos, si no existe la crea.
    verify_db()

    # Ventana del Menú Principal
    root = tk.Tk()
    configurar_ventana(root, "Menú Principal")

    # Obtener el nombre de usuario de Windows
    user_name = os.getlogin()  # O usa os.environ['USERNAME'] si getlogin no funciona

    # Crear un label de bienvenida
    welcome_label = tk.Label(root, text=f"¡Bienvenido, {user_name}!", font=("Arial", 16), fg="blue")
    welcome_label.place(relx=1.0, y=20, anchor='ne')  # Posición relativa en la esquina superior derecha

    poner_imagen_de_fondo(root, menu_azusa, ancho=500, alto=300, x=-50, y=5, resize=False)

    # Cargar imagen
    image = Image.open(default_image_path)
    image = image.resize((200, 200), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Crear el botón de imagen
    label_img = tk.Label(root, image=photo, borderwidth=0)
    label_img.pack(pady=10)
    label_img.bind("<Button-1>", lambda e: manejar_clic_imagen(e, label_img))


    # Crear un label para mostrar la versión en la esquina inferior izquierda
    version_label = tk.Label(root, text=f"{VERSION}", font=("Arial", 10), fg="gray")
    version_label.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)  # Posicionar en la esquina inferior izquierda

    # Crear botones
    buttons = [
        ("Parámetros de Medición", lambda: parametros_medicion(root)),
        ("Reporte Central", lambda: reporte_grande()),
        ("Actividades", lambda: ven1(root)),
        ("Control de Asignaciones de Equipos", lambda: control_asignaciones(root)),
        ("Personal ESD", lambda: personal_esd(root))
    ]

    for text, command in buttons:
        btn = tk.Button(root, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2, width=40)
        btn.pack(pady=10)

    # Función para salir del programa
    def salir_programa():
        # Cerrar la conexión a la base de datos si está abierta
        if 'connection' in globals() and connection:
            connection.close()  # Cierra la conexión a la base de datos

        # Cerrar todas las ventanas de Tkinter
        if 'root' in globals() and isinstance(root, tk.Tk):
            root.quit()  # Cierra todas las ventanas de Tkinter
            root.destroy()  # Destruye el objeto root

        # Salir del programa de manera segura
        sys.exit(0)  # Sale del programa de manera segura

    # Crear el botón "Salir"
    btn_salir = tk.Button(root, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white", height=2, width=10)
    btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

    # Ejecutar la ventana principal
    root.mainloop()

# Asegurarse de que el código solo se ejecute si el script es el principal
if __name__ == "__main__":
    main()
