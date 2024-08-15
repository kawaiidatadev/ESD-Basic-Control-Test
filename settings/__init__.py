from common import *

# Path of data base sqlite
db_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\database.sqlite'

#SQL de creacion de tablas
sql_file = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Archivos db\create_db_sqlite.sql'

# Default ESD image path
default_image_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\ESD incono PNG.png'

# Defaul ICON
inon_path = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\girlrecort.ico'

# Default document PDF "ANSI S20.20" default
document_path = r'\\10.0.0.9\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Documentos\Manuales\97_ELE_0_ANSI-ESD-S20.20-2014.pdf'

imagen_fondo_registro_batas = r'\\mercury\Mtto_Prod\00_Departamento_Mantenimiento\ESD\Software\Recurses\registro_batas.png'

def poner_imagen_de_fondo(ventana, path_imagen):
    # Cargar la imagen de fondo
    imagen_fondo = Image.open(path_imagen)
    imagen_fondo = imagen_fondo.resize((ventana.winfo_width(), ventana.winfo_height()))
    fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear un label para la imagen de fondo
    label_fondo = tk.Label(ventana, image=fondo)
    label_fondo.image = fondo  # Necesario para evitar que el garbage collector elimine la imagen
    label_fondo.place(relwidth=1, relheight=1)  # Hacer que el label ocupe toda la ventana

def cambiar_imagen(label):
    new_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if new_image_path:
        image = Image.open(new_image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

# Función para abrir el documento PDF
def abrir_documento():
    if os.path.exists(document_path):
        subprocess.Popen([document_path], shell=True)
    else:
        messagebox.showerror("Error", "El documento no se encuentra en la ruta especificada.")


# Función para abrir ventanas nuevas y ocultar el menú principal
def abrir_ventana(nombre_ventana, root):
    nueva_ventana = tk.Toplevel(root)
    nueva_ventana.title(nombre_ventana)
    nueva_ventana.state('zoomed')

    # Evento para cuando la ventana secundaria se cierra
    nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(nueva_ventana, root))

    root.withdraw()  # Ocultar el menú principal mientras la ventana secundaria está abierta

def cerrar_ventana(nueva_ventana, root):
    nueva_ventana.destroy()  # Cierra la ventana secundaria
    root.deiconify()  # Muestra nuevamente el menú principal
    root.state('zoomed')


# Función para manejar clics en la imagen
def manejar_clic_imagen(event, label):
    if event.state & 0x0001:  # Shift key is pressed
        cambiar_imagen(label)
    else:
        abrir_documento()
