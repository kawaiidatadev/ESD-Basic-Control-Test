from common.__init__ import *  # Importa todas las librerías comunes.
from settings.__init__ import *  # Importa todos los paths y funciones que manejan documentos.
from db_exist import verify_db  # Importa la función para crear la base de datos si no existe.
from submains.submain_parametros import *  # Importa la funcion del submenu de primer nivel de parametros
from submains.submain_personal_esd import *  # Importa la funcion del submenu de primer nivel de personal esd
from settings.conf_ventana import configurar_ventana  # Importa una funcion de cofiguracion global de ventanas.

#Verificamos la base de datos, si no existe la crea.
verify_db()

# Ventana del Menú Principal
root = tk.Tk()
configurar_ventana(root, "Menú Principal")

# Obtener el nombre de usuario de Windows
user_name = os.getlogin()  # O usa os.environ['USERNAME'] si getlogin no funciona

# Crear un label de bienvenida
welcome_label = tk.Label(root, text=f"¡Bienvenido, {user_name}!", font=("Arial", 16), fg="blue")
welcome_label.place(relx=1.0, y=20, anchor='ne')  # Posición relativa en la esquina superior derecha

# Cargar imagen
image = Image.open(default_image_path)
image = image.resize((200, 200), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Crear el botón de imagen
label_img = tk.Label(root, image=photo, borderwidth=0)
label_img.pack(pady=10)
label_img.bind("<Button-1>", lambda e: manejar_clic_imagen(e, label_img))

# Crear botones
buttons = [
    ("Parámetros de Medición", lambda: parametros_medicion(root)),
    ("Reporte Central", reporte_central),
    ("Actividades", actividades),
    ("Control de Asignaciones de Equipos", control_asignaciones),
    ("Personal ESD", lambda: personal_esd(root))
]

for text, command in buttons:
    btn = tk.Button(root, text=text, command=command, font=("Arial", 14), bg="sky blue", height=2, width=40)
    btn.pack(pady=10)

# Función para salir del programa
def salir_programa():
    # Cerrar la conexión a la base de datos si está abierta
    if 'connection' in globals():
        connection.close()  # Cierra la conexión a la base de datos
    root.quit()  # Cierra todas las ventanas de Tkinter
    root.destroy()  # Destruye el objeto root
    sys.exit(0)  # Sale del programa de manera segura

# Crear el botón "Salir"
btn_salir = tk.Button(root, text="Salir", command=salir_programa, font=("Arial", 14), bg="red", fg="white", height=2, width=10)
btn_salir.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Posiciona el botón en la esquina inferior derecha

# Ejecutar la ventana principal
root.mainloop()